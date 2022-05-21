from sqlalchemy.orm import sessionmaker, declarative_base 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


#SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./ssadb.db"
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://ssa_user:Budinosauro11@localhost/ssadb"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True) #connect_args={"check_same_thread": False} 
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()