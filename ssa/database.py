from sqlalchemy.orm import sessionmaker, declarative_base 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


#SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./ssadb.db"
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://ssa_user:password@localhost/ssadb"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=False, echo=False) #connect_args={"check_same_thread": False} 
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
