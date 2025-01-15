"""
Database models for users and tasks.

Classes:
    - User: Represents a user.
    - Task: Represents a task.
"""
import uuid
from datetime import datetime

from sqlalchemy import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.extensions import db


class User(db.Model):
    """
    User model.
    """
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    tasks: Mapped[list['Task']] = relationship('Task', back_populates='user')

    def __repr__(self):
        return f'<User {self.email}>'


class Task(db.Model):
    """
    Task model.
    """
    __tablename__ = 'tasks'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='tasks')

    def __repr__(self):
        return f'<Task {self.title}>'

    def as_dict(self):
        """
        Convert Task object to a dictionary.

        :return: dict: Task attributes as key-value pairs.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at,
            'user_id': self.user_id,
        }
