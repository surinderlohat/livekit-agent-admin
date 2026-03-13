from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import shutil
from datetime import datetime
from alembic.config import Config as AlembicConfig
from alembic import command
from models import Config

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./.db/livekit_admin.db")

# Ensure directory exists for SQLite
if DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def backup_db():
    """Create a backup of the SQLite database file."""
    if DATABASE_URL.startswith("sqlite:///"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_path):
            backup_dir = os.path.join(os.path.dirname(db_path), "backups")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"livekit_admin_{timestamp}.db.bak")
            shutil.copy2(db_path, backup_path)
            print(f"Database backup created: {backup_path}")


def run_migrations():
    """Run migrations programmatically using Alembic."""
    # Backup before upgrade
    backup_db()

    alembic_cfg = AlembicConfig("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def init_db():
    # Run migrations first
    run_migrations()

    # Initialize default values if not exists
    db = SessionLocal()
    try:
        if not db.query(Config).filter(Config.key == "system_prompt").first():
            db.add(Config(key="system_prompt", value="You are a helpful voice assistant."))

        # Add LiveKit default placeholders if not exists
        if not db.query(Config).filter(Config.key == "livekit_url").first():
            db.add(Config(key="livekit_url", value="http://localhost:7880"))
        if not db.query(Config).filter(Config.key == "livekit_api_key").first():
            db.add(Config(key="livekit_api_key", value="devkey"))
        if not db.query(Config).filter(Config.key == "livekit_api_secret").first():
            db.add(Config(key="livekit_api_secret", value="secret"))

        db.commit()
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
