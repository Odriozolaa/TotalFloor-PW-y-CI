import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=False)
else:
    engine = create_engine(
        "sqlite:///./local.db", echo=False, connect_args={"check_same_thread": False}
    )


def get_session():
    with Session(engine) as session:
        yield session
