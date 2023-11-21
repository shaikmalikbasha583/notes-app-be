from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.main.config.db_config import Base


class BaseMixin(object):
    __mapper_args__ = {"always_refresh": True}

    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1)
    created_by: Mapped[int] = mapped_column(default=0)
    updated_by: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)


class User(BaseMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(unique=True)
