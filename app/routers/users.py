from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/users", tags=["Users"])

pwdcontext = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "durvesh1107"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hashpassword(password: str) -> str:
    return pwdcontext.hash(password)

def verifypassword(plainpassword: str, hashedpassword: str) -> bool:
    return pwdcontext.verify(plainpassword, hashedpassword)

def getdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(getdb)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hashpassword(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        role=user.role,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def loginuser(credentials: schemas.UserLogin, db: Session = Depends(getdb)):
    dbuser = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not dbuser:
        raise HTTPException(status_code=404, detail="User not found")

    if not verifypassword(credentials.password, dbuser.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token(
        data={
            "sub": dbuser.email,
            "user_id": dbuser.id,
            "role": dbuser.role
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/", response_model=list[schemas.UserResponse])
def getusers(db: Session = Depends(getdb)):
    return db.query(models.User).all()


@router.get("/{userid}",response_model=schemas.UserResponse)
def getuser(userid: int, db: Session = Depends(getdb)):
    return db.query(models.User).filter(models.User.id == userid).first()

@router.delete("/{userid}")
def deleteuser(userid: int, db: Session = Depends(getdb)):
    user = db.query(models.User).filter(models.User.id == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

