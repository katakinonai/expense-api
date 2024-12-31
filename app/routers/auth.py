from typing import Optional, Dict, Union

from fastapi import APIRouter, Request
from fastapi.security import OAuth2PasswordBearer

from app.db.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserResponse
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
router = APIRouter()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode: Dict = data.copy()
    expire: datetime = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(
    token: str, db: Session = Depends(get_db)
) -> Union[User, HTTPException]:
    credentials_exception: HTTPException = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: Dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        user: Optional[User] = db.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError as exc:
        # Reraise the original JWTError exception and link it to the custom exception
        raise credentials_exception from exc


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Union[User, HTTPException]:
    return verify_token(token, db)


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)) -> User:
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user: User = User(
        username=user.username,
        email=str(user.email),
        password_hash=get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)) -> Dict[str, str]:
    form_data = await request.form()
    if form_data:
        username = form_data.get("username")
        password = form_data.get("password")
    else:
        login_request = await request.json()
        username = login_request.get("email")
        password = login_request.get("password")

    user: Optional[User] = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(str(password), str(user.password_hash)):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token: str = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
