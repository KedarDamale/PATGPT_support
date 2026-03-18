from langchain_core.tools import tool
from sqlalchemy.orm import Session


def make_memory_tools(db: Session, user_id: int):
    from src.modules.memory.memory_service import MemoryStore

    @tool
    def save_user_memory(key: str, value: str) -> str:
        """
        Save something important the user mentioned about themselves.
        Memories are global — they persist across all conversations.
        Call this whenever the user reveals a preference, habit, name,
        goal, or any personal detail worth remembering long-term.

        Examples:
        - "my name is Kedar"            → key="name",               value="Kedar"
        - "I prefer short answers"      → key="response_style",     value="concise"
        - "I work in AI engineering"    → key="profession",         value="AI engineer"
        - "I hate long explanations"    → key="response_style",     value="keep answers short"
        - "I moved to Pune"             → key="city",               value="Pune"

        If the key already exists, the old value is overwritten.
        """
        MemoryStore.save(db, user_id, key, value)
        return f"Remembered: {key} = {value}"

    @tool
    def get_user_memories() -> str:
        """
        Retrieve everything remembered about this user across all conversations.
        Call this at the start of a new conversation to personalise your responses.
        """
        memories = MemoryStore.get_all(db, user_id)
        if not memories:
            return "No memories saved for this user yet."
        return "\n".join(f"- {k}: {v}" for k, v in memories.items())

    @tool
    def delete_user_memory(key: str) -> str:
        """
        Delete a specific memory by key.
        Call this when the user says something like 'forget that' or 'that's no longer true'.
        """
        deleted = MemoryStore.delete(db, user_id, key)
        return f"Forgot '{key}'." if deleted else f"No memory found for '{key}'."

    return [save_user_memory, get_user_memories, delete_user_memory]


