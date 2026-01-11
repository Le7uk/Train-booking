from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from ..config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Хешує пароль"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевіряє чи пароль співпадає з хешем"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Створює JWT токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    print(f"🔑 Creating token with payload: {to_encode}")  # DEBUG
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"✅ Token created: {token}")  # DEBUG
    
    return token