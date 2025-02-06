from sqlalchemy.orm import Session

from models import Log


class LogCRUD:

    def __init__(self, session: Session) -> None:
        self.session = session

    async def read_all(self):
        return self.session.query(Log).all()
