from __future__ import annotations

from sqlalchemy import Boolean, BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, TYPE_CHECKING
from bot.database import Base

if TYPE_CHECKING:
    from .filial import Filial


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    group_name: Mapped[str] = mapped_column(String(255))
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    has_filials: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    filials: Mapped[List["Filial"]] = relationship(
        "Filial",
        back_populates="group",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Group {self.group_name} ({self.group_id})>"