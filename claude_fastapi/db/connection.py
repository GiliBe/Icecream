# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./ice_cream_shop.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



# postgress
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.pool import QueuePool

# # PostgreSQL Database URL
# # Format: postgresql://username:password@host:port/database_name
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/ice_cream_shop"

# # Create engine with connection pooling
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     poolclass=QueuePool,
#     pool_size=5,  # Maximum number of connections in the pool
#     max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
#     pool_timeout=30,  # Timeout in seconds for getting a connection from the pool
#     pool_recycle=1800,  # Recycle connections after 30 minutes
# )

# # Create session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create base class for declarative models
# Base = declarative_base()

# # Database initialization function
# def init_db():
#     # Import models here to avoid circular imports
#     from models import Base
#     Base.metadata.create_all(bind=engine)

# CREATE DATABASE ice_cream_shop;
# Update the SQLALCHEMY_DATABASE_URL with your PostgreSQL credentials:


# Replace postgres with your database username
# Replace your_password with your database password
# Replace localhost with your database host if not running locally
# Replace 5432 with your PostgreSQL port if different
# The database name is set to ice_cream_shop


# Initialize your database tables by calling init_db() when starting your application:

# The new configuration includes:

# Connection pooling for better performance
# Pool size configuration
# Connection timeouts
# Connection recycling
# Proper PostgreSQL connection string format

# Benefits of using PostgreSQL over SQLite:

# Better concurrent access handling
# More robust ACID compliance
# Better scalability
# More advanced features (full-text search, JSON support, etc.)
# Better for production deployment

