from sqlalchemy.orm import Session

from models import User
from schemas.user import UserInfo, UserUpdateForm
from utils.database import to_dict


class UserCRUD:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_users(self) -> list[dict]:
        users = self.session.query(User).filter().all()
        users_list = [to_dict(user) for user in users]
        return users_list

    def delete_user(self, user_id: int) -> bool:

        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
        else:
            return False
        return True

    def find_user_by_id(self, id: int) -> UserInfo:
        return self.session.query(User).filter(User.id == id).first()

    def update_user_by_id(self, id: int, user_data: UserUpdateForm) -> UserInfo:
        user = self.session.query(User).filter(User.id == id).one_or_none()

        new_data = {
            "username": (
                user_data.username if user_data.username is not None else user.username
            ),
            "email": (user_data.email if user_data.email is not None else user.email),
            "password": user.password,
        }

        for key, value in new_data.items():
            setattr(user, key, value)
        self.session.commit()
        return user
