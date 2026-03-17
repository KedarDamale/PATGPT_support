#-----------------------------------------------------------------------------------------#
#Password hashing utility from pwdlib by using argon2
#we are not using bcrypt as it is susceptible to GPU attacks and cracking
#-----------------------------------------------------------------------------------------#

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from typing import List
from fastapi import Depends, HTTPException, status

ph = PasswordHash(hashers=[Argon2Hasher()])

def hash_password(password:str) -> str:
    return ph.hash(password)

def verify_password(password:str, hashed_password:str) -> bool:
    return ph.verify(password, hashed_password)

#-----------------------------------------------------------------------------------------#
#JWT token utilities
#decoding token 
#access and refresh token genration and verfication
#-----------------------------------------------------------------------------------------#

from src.config.env_config import settings
from typing import Literal
from datetime import datetime, timedelta, timezone
import jwt

#this method creates access token and refresh token
def encode_token(payload:dict,token_type:Literal["access", "refresh"] = "access") ->str: 
    try:
        #copying payload as we need to add another fields to payload
        to_encode_payload=payload.copy()

        #caluculating expire timedelta
        if token_type=="access":
            expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        elif token_type=="refresh":
            expire_time = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        else:
            raise ValueError("Invalid token type")

        #encoding time delta in payload
        to_encode_payload.update({"exp": expire_time,"type": token_type})
        
        return jwt.encode(to_encode_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    except jwt.PyJWTError as e:
        raise RuntimeError(f"Error encoding token: {e}")


#this method decodes tokens
def decode_token(token:str)->dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError as e:
        raise RuntimeError(f"Error decoding token: {e}")


#-----------------------------------------------------------------------------------------#
#Role checker class for RBAC and its get_current_user dependency
#dependencies:getdb, decode token 
#-----------------------------------------------------------------------------------------#

from src.config.env_config import settings
from src.db.engine import get_db 
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
from sqlalchemy.orm import Session
from src.modules.auth.auth_model import User


def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):

    exception:HTTPException=HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    try:
        payload = decode_token(token)
        if payload is None:
            raise exception
        email: str = payload.get("sub")
        token_type: str = payload.get("type")

        if email is None or token_type != "access":
            raise exception

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise exception
        return user

    except:
        raise exception

class RoleChecker:
    def __init__(self,allowed_roles:List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough permissions to access this resource"
            )
        return user
