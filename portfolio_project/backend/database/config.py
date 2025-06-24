"""
SQLAlchemy Database Configuration for TiDB Cloud
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
class DatabaseConfig:
    def __init__(self):
        # TiDB Cloud connection parameters
        self.host = os.getenv('TIDB_HOST', 'localhost')
        self.port = os.getenv('TIDB_PORT', '4000')
        self.user = os.getenv('TIDB_USER', 'root')
        self.password = os.getenv('TIDB_PASSWORD', '')
        self.database = os.getenv('TIDB_DATABASE', 'portfolio_db')
        
        # SSL Configuration for TiDB Cloud
        self.ssl_ca = os.getenv('TIDB_SSL_CA', '')
        self.ssl_disabled = os.getenv('TIDB_SSL_DISABLED', 'false').lower() == 'true'
        
        # Connection pool settings
        self.pool_size = int(os.getenv('DB_POOL_SIZE', '10'))
        self.max_overflow = int(os.getenv('DB_MAX_OVERFLOW', '20'))
        self.pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', '30'))
        self.pool_recycle = int(os.getenv('DB_POOL_RECYCLE', '3600'))
        
    def get_database_url(self):
        """Generate database URL for SQLAlchemy"""
        if self.ssl_disabled:
            # For local development or when SSL is disabled
            return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            # For TiDB Cloud with SSL - use ssl=true for TiDB Cloud
            ssl_args = "?ssl=true&ssl_verify_cert=false&ssl_verify_identity=false"
            
            return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}{ssl_args}"

# Initialize database configuration
db_config = DatabaseConfig()

# Create SQLAlchemy engine
engine = create_engine(
    db_config.get_database_url(),
    pool_size=db_config.pool_size,
    max_overflow=db_config.max_overflow,
    pool_timeout=db_config.pool_timeout,
    pool_recycle=db_config.pool_recycle,
    echo=os.getenv('DB_ECHO', 'false').lower() == 'true',  # Set to True for SQL logging
    pool_pre_ping=True,  # Verify connections before use
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Dependency function to get database session
    Use this in your API endpoints or services
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database connection test function
def test_connection():
    """Test database connection"""
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

# Initialize database (create tables)
def init_db():
    """Initialize database - create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        return False