from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from pydantic import EmailStr, constr

app = FastAPI()

# for better error handling practices...
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

def handle_db_errors(func):
    @wraps(func)  # Add this to preserve the function signature
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error: " + str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    return wrapper



# Database configuration
DATABASE_URL = "mysql+mysqlconnector://root:KingNo.01!Ml@localhost:3306/finance_manager"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Table schemas
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)

# Pydantic model for input validation
class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    category: str
    date: str

class UserCreate(BaseModel):
    name: constr(min_length=1)
    email: EmailStr

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def error_response(status_code: int, message: str):
    raise HTTPException(status_code=status_code, detail={"error": message})


@app.get("/")
def read_root():
    return {"message": "Welcome to the Personal Finance Manager"}


# 1. Create a new user
@app.post("/users", status_code=201)
@handle_db_errors
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check for duplicate email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create and insert the user
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully", "data": db_user}

# 2. Get all users
@app.get("/users", status_code=200)
@handle_db_errors
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}

# 3. Delete a transaction by ID
@app.delete("/transactions/{transaction_id}", status_code=200)
@handle_db_errors
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return {"message": f"Transaction {transaction_id} deleted successfully"}

@app.post("/transactions")
@handle_db_errors
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        db_transaction = Transaction(**transaction.dict())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return {"message": "Transaction added successfully", "data": transaction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions")
@handle_db_errors
def read_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

@app.get("/transactions/{transaction_id}", status_code=200)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction with ID {transaction_id} not found")
    return transaction

@app.delete("/users/{user_id}", status_code=200)
@handle_db_errors
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return error_response(404, f"User with ID {user_id} not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}
