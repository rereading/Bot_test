from __future__ import annotations

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import TYPE_CHECKING
from bot.database import Base

if TYPE_CHECKING:
    from .group import Group


class Filial(Base):
    __tablename__ = "filials"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    pyrus_field_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    group: Mapped["Group"] = relationship("Group", back_populates="filials")
    
    def __repr__(self) -> str:
        return f"<Filial {self.name}>"