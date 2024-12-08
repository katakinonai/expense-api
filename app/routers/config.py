import os

SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
