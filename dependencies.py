from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from databases.connection import SessionLocal, engine
from models import Base

# create the database tables
Base.metadata.create_all(bind=engine)


# dependency database function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
