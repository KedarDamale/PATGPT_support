from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from .memory_model import UserMemory
from threading import Lock


class MemoryStore:
    """
    Two-layer store:
      - Layer 1: in-process dict  { user_id: { key: value } }  → fast, no DB hit
      - Layer 2: DB table         UserMemories                  → survives restarts

    On first access per user, DB is loaded into RAM (warm-up).
    Every write goes to both layers atomically.
    """

    _cache: dict[int, dict[str, str]] = {}   # { user_id: { key: value } }
    _lock = Lock()                            # thread-safe cache mutations
    _warmed: set[int] = set()                 # tracks which user_ids are loaded

    # ── Internal ──────────────────────────────────────────────

    @classmethod
    def _warm(cls, db: Session, user_id: int):
        """Load DB rows into RAM once per user per server lifetime."""
        if user_id in cls._warmed:
            return
        with cls._lock:
            if user_id in cls._warmed:   # double-checked locking
                return
            rows = db.query(UserMemory).filter_by(user_id=user_id).all()
            cls._cache[user_id] = {row.key: row.value for row in rows}
            cls._warmed.add(user_id)

    # ── Public API ────────────────────────────────────────────

    @classmethod
    def save(cls, db: Session, user_id: int, key: str, value: str):
        cls._warm(db, user_id)
        key = key.lower().strip()
        value = value.strip()

        # Layer 1 — RAM
        with cls._lock:
            cls._cache.setdefault(user_id, {})[key] = value

        # Layer 2 — DB (upsert)
        stmt = (
            sqlite_insert(UserMemory)
            .values(user_id=user_id, key=key, value=value)
            .on_conflict_do_update(
                index_elements=["user_id", "key"],
                set_={"value": value},
            )
        )
        db.execute(stmt)
        db.commit()

    @classmethod
    def get_all(cls, db: Session, user_id: int) -> dict[str, str]:
        cls._warm(db, user_id)
        with cls._lock:
            return dict(cls._cache.get(user_id, {}))   # return a copy

    @classmethod
    def delete(cls, db: Session, user_id: int, key: str) -> bool:
        cls._warm(db, user_id)
        key = key.lower().strip()

        # Layer 1 — RAM
        with cls._lock:
            existed = key in cls._cache.get(user_id, {})
            cls._cache.get(user_id, {}).pop(key, None)

        # Layer 2 — DB
        db.query(UserMemory).filter_by(user_id=user_id, key=key).delete()
        db.commit()

        return existed

    @classmethod
    def invalidate_user(cls, user_id: int):
        """
        Call this if you ever update UserMemory rows directly via SQL
        outside of this store, to force a re-warm on next access.
        """
        with cls._lock:
            cls._cache.pop(user_id, None)
            cls._warmed.discard(user_id)