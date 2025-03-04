from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.main.config.db_config import Base
from app.main.utils.common_utils import get_timestamp_in_utc

DB_SCHEMA: str = "notes"


class BaseMixin(object):
    __mapper_args__ = {"always_refresh": True}
    # __table_args__ = {"schema": DB_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1)
    created_by: Mapped[int] = mapped_column(default=0)
    updated_by: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=get_timestamp_in_utc)
    updated_at: Mapped[datetime] = mapped_column(
        default=get_timestamp_in_utc,
        onupdate=get_timestamp_in_utc,
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)


class User(BaseMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(unique=True)

    ## Relationship Attributes
    notes: Mapped[List["Note"]] = relationship(back_populates="user", lazy="selectin")


class DummyTable(BaseMixin, Base):
    __tablename__ = "dummy_table"

    description: Mapped[str] = mapped_column(nullable=True)


class Note(BaseMixin, Base):
    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="PENDING")
    target_date: Mapped[datetime] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="notes", lazy="selectin")
