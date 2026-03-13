from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models import Base, Config

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./livekit_admin.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

    # Initialize default values if not exists
    db = SessionLocal()
    try:
        if not db.query(Config).filter(Config.key == "system_prompt").first():
            db.add(
                Config(key="system_prompt", value="You are a helpful voice assistant.")
            )

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
