from model.BaseModel import BaseModel
from db import db


class Amenity(BaseModel):
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def __str__(self):
        return f"[Amenity] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
