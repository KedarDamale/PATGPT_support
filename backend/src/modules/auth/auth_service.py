#--------------------------------------------------------------------------#
# registering user
#--------------------------------------------------------------------------#

from src.modules.auth.auth_validation_schema import UserCreate
from src.db.engine import get_db
from sqlalchemy.orm import Session
from src.logger.log import logger
from src.modules.auth.auth_model import User
from src.modules.auth.auth_helpers import hash_password
from src.config.env_config import settings
from fastapi import Depends, HTTPException

def register(user_create:UserCreate, db:Session=Depends(get_db)):
    logger.info(f"Signing up: {user_create.email}")
    user_in_db=db.query(User).filter(User.email==user_create.email).first()
    #if username is required then add that in model and validated if it is present just like email validation
    if user_in_db:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        new_user=User(
            email=user_create.email,
            hashed_password=hash_password(user_create.password),
            role=settings.DEFAULT_ROLE
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

#--------------------------------------------------------------------------#
# logging in user
#--------------------------------------------------------------------------#

from src.db.engine import get_db
from sqlalchemy.orm import Session
from src.logger.log import logger
from src.modules.auth.auth_validation_schema import LoginRequest
from src.modules.auth.auth_helpers import verify_password,encode_token

def login(user_login:LoginRequest, db:Session=Depends(get_db)):
    logger.info(f"Logging in: {user_login.email}")
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    else:
        if not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid password")
        else:
            access_token=encode_token({"sub": user.email, "role": user.role},"access")
            refresh_token=encode_token({"sub": user.email},"refresh")
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
            
#--------------------------------------------------------------------------#
# Deleting user can be done by Admin only
#--------------------------------------------------------------------------#

def delete_user(user_email:str,db:Session):
    logger.info(f"Deleting user: {user_email}")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        return {"message": "User not found"}
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

#--------------------------------------------------------------------------#
# creating new access and refresh tokens 
# after access token expires
#--------------------------------------------------------------------------#
from src.db.engine import get_db
from sqlalchemy.orm import Session
from src.logger.log import logger
from src.modules.auth.auth_helpers import decode_token

def create_new_pair_of_tokens(refresh_token: str, db: Session = Depends(get_db)):
    payload=decode_token(refresh_token)
    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    
    email=payload.get("sub")
    token_type=payload.get("type")
    
    if not email and token_type != "refresh":
        raise HTTPException(status_code=400,detail="Invalid refresh token")
    
    else:
        user=db.query(User).filter(User.email==email).first()
        if not user:
            raise HTTPException(status_code=400,detail="User not found")
        else:
            new_access_token=encode_token({"sub": user.email, "role": user.role},"access")
            new_refresh_token=encode_token({"sub": user.email},"refresh")
            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }