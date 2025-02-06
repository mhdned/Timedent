from sqlalchemy.orm import Session

from models import User
from schemas.auth import AuthAdminInfo, AuthCreateClientData


class AuthCRUD:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_admin_by_email(self, email: str) -> AuthAdminInfo:
        return (
            self.session.query(User)
            .filter(User.email == email and User.is_admin == True)
            .first()
        )

    def create_client(self, client_data: AuthCreateClientData):
        client = User(
            username=client_data.username,
            email=client_data.email,
            password=client_data.password,
        )
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)

        return client

    def find_client_by_email(self, email: str) -> AuthAdminInfo:
        return self.session.query(User).filter(User.email == email).first()
