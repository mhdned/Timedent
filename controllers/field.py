from sqlalchemy.orm import Session

from models import Field
from schemas.field import FieldData, FieldFormData
from utils.database import to_dict


class FieldCRUD:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_fields(self) -> list[FieldData]:
        fields = self.session.query(Field).all()
        fields_list = [to_dict(field) for field in fields]
        return fields_list

    def find_field_by_id(self, field_id: int) -> FieldData:
        return self.session.query(Field).filter(Field.id == field_id).first()

    def create_field(self, field_data: FieldFormData):
        new_field = Field(title=field_data.title)

        self.session.add(new_field)
        self.session.commit()
        self.session.refresh(new_field)

        return new_field

    def delete_field(self, field_id: int) -> bool:
        find_field = self.session.query(Field).filter(Field.id == field_id).first()

        if not find_field:
            return False
        else:
            self.session.delete(find_field)
            self.session.commit()
        return True

    def update_field_by_id(self, id: int, field_data: FieldFormData) -> FieldData:
        field = self.session.query(Field).filter(Field.id == id).one_or_none()
        new_data = {
            "title": (field_data.title if field_data.title is not None else field.title)
        }
        for key, value in new_data.items():
            setattr(field, key, value)
        self.session.commit()

        return field
