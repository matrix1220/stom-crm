
from fastapi import FastAPI, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User
from schemas import UserCreate, UserOut, Token
from utils import hash_password, verify_password, create_access_token
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (use with caution in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User registration
@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password and create the user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# User login
@app.post("/login", response_model=Token)
def login(credentials: dict = Body(...), db: Session = Depends(get_db)):  # Change this line
    username = credentials.get("username")
    password = credentials.get("password")
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route
@app.get("/users/me", response_model=UserOut)
def read_users_me(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_admin_user(x_token: str = Header(...)):  # Requires admin token in header
    try:
        payload = jwt.decode(x_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")  # Assuming "sub" holds username
        # Check if username has admin privileges (replace with your admin check logic)
        if username != "admin": # Replace with suitable admin verification from db if needed.
            raise HTTPException(status_code=403, detail="Not authorized")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/admin/create_user", response_model=UserOut, dependencies=[Depends(get_admin_user)])
def create_user_admin(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists (same logic as your register route)
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and create user (same logic as your register route)
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user