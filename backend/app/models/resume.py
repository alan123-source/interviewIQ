from app.database.db import Base
from sqlalchemy import Column,Integer,String,Text,ForeignKey,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

class Resume(Base):
    __tablename__="resumes"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(
        Integer,
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    original_filename=Column(
        String(255),
        nullable=False
    )

    file_path=Column(
        String(500),
        nullable=False
    )

    extracted_text=Column(
        Text,
        nullable=False
    )

    ai_analysis=Column(
        JSONB,
        nullable=True
    )

    status=Column(
        String(20),
        nullable=False,
        default="completed"
    )

    created_at=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False

    )

    updated_at=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user=relationship(
        "User",
        back_populates="resumes",
    )