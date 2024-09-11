import os 

class Config:
        SECRET_KEY=os.environ.get("SECRET_KEY") or "your_secret_key_here"
        SQLALCHEMY_DATABASE_URI= os.environ.get("DATABASE_URI") or "sqlite://diary.db"
        SQLALCHEMY_TRACK_MODIFICATION=False 
        SESSION_COOKIE_SECURE=True
        SESSION_COOKIE_HTTPONLY=True
        SESSION_COOKIE_SAMESITE='Lax'

class DevelopmentConfig(Config):
        DEBUG=True
        
        
        
        
class ProductionConfig(Config):
        DEBUG=False