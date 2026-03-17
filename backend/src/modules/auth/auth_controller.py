#-----------------------------------------------------------------------------------------#
# Creating routers for authentication 
#-----------------------------------------------------------------------------------------#
from fastapi import APIRouter,Depends
router=APIRouter(prefix="/auth",tags=["Auth,Authentication,Authorization"])
from src.modules.auth.auth_service import register as register_service, login as login_service, create_new_pair_of_tokens
from src.modules.auth.auth_validation_schema import Token, UserOut, UserCreate, LoginRequest, RefreshRequest
from src.db.engine import get_db
from sqlalchemy.orm import Session
from src.logger.log import logger
from src.modules.auth.auth_helpers import RoleChecker
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login",response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Login request received for {form_data.username}")
    user_login = LoginRequest(email=form_data.username, password=form_data.password)
    return login_service(user_login, db)
    
@router.post("/register",response_model=UserOut)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Register request received for {user_create.email}")
    return register_service(user_create, db)

@router.post("/refresh",response_model=Token)
def refresh(refresh_data: RefreshRequest, db: Session = Depends(get_db)):
    logger.info("Refresh token request received")
    return create_new_pair_of_tokens(refresh_data.refresh_token, db)

@router.get("/access/user",response_model=UserOut)
def access_user(role=Depends(RoleChecker(["user","admin"]))):
    return role

@router.get("/access/admin",response_model=UserOut)
def access_admin(role=Depends(RoleChecker(["admin"]))):
    return role #returns entire user model yet after it will be changed to just email and role

