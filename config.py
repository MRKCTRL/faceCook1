import os 

class Config:
        SECRET_KEY=os.envron.get("SECRET_KEY") or "your_secret_key_here"
        SQLALCHEMY_DATABASE_URI= os.environ.get("DATABASE_URI") or "sqlite://diary.db"
        SQLALCHEMY_TRACK_MODIFICATION=False