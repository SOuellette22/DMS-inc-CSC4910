from app import db
from datetime import datetime

class Admin(db.Model):
    __tablename__ = 'admin_info'

    email = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return f"<Admin {self.email}>"