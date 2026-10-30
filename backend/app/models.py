from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# The schema is owned by the dbmate migrations in db/migrations - keep models in sync with them
class ExampleItem(Base):
    __tablename__ = "example_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
