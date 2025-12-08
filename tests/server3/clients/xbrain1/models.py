from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Float, DateTime, ForeignKey, JSON, func
import database

class User(database.Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    # password etc. not needed on car

    machines: Mapped[list["Machine"]] = relationship(back_populates="user")

class MachineType(database.Base):
    __tablename__ = "machine_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    machines: Mapped[list["Machine"]] = relationship(back_populates="machine_type")

class Machine(database.Base):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    small_description: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)

    motor_left_speed: Mapped[int] = mapped_column(Integer, default=0)
    motor_right_speed: Mapped[int] = mapped_column(Integer, default=0)
    lights_on: Mapped[bool] = mapped_column(Boolean, default=False)
    fog_lights_on: Mapped[bool] = mapped_column(Boolean, default=False)
    happiness: Mapped[int] = mapped_column(Integer, default=50)
    hunger: Mapped[int] = mapped_column(Integer, default=0)
    is_auto_driving: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    machine_type_id: Mapped[int | None] = mapped_column(ForeignKey("machine_types.id"), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="machines")
    machine_type: Mapped["MachineType"] = relationship(back_populates="machines")
    nodes: Mapped[list["Node"]] = relationship(back_populates="machine")

class Node(database.Base):
    __tablename__ = "nodes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"))
    name: Mapped[str] = mapped_column(String)
    node_type: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="offline")
    configuration: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    machine: Mapped["Machine"] = relationship(back_populates="nodes")
