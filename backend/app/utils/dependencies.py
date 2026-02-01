from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..config import SECRET_KEY, ALGORITHM
from ..database import get_db
from ..models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    
    print(f"Received token: {token}")  
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")  
        
        user_id: int = payload.get("sub")
        print(f"User ID: {user_id}")  
        
        if user_id is None:
            print("No user_id in payload")
            raise HTTPException(status_code=401, detail="Invalid token")
    
    except JWTError as e:
        print(f"JWT Error: {e}")  
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        print("User not found in DB")
        raise HTTPException(status_code=401, detail="User not found")
    
    print(f"User authenticated: {user.email}")
    return user