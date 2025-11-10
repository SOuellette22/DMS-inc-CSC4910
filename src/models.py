from src.app import db
from datetime import datetime

class Admin(db.Model):
    __tablename__ = 'admin_info'

    email = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return f"<Admin {self.email}>"

class AIModels(db.Model):
    __tablename__ = 'trained_models'

    model_name = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    admin_email = db.Column(db.String(255), db.ForeignKey('admin_info.email'), nullable=False)
    updated_by = db.Column(db.String(255), db.ForeignKey('admin_info.email'), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<AIModel {self.model_name} by {self.admin_email}>"