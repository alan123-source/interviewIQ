from sqlalchemy import Column,Integer,String,DateTime,func,Boolean

from app.database.db import Base

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(
        String,
        unique=True,
        nullable=False
    )

    image=Column(
        String,
        nullable=True
    )

    password_hash=Column(String,nullable=False
    )

    created_at=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    is_active=Column(
        Boolean,
        nullable=False,
        default=True
    )

    updated_at=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True
    )

    resumes=relationship(
        "Resume",
        back_populates="user",
        cascade="all,delete-orphan"
    )