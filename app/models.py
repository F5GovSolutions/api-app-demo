from sqlmodel import Field, Session, SQLModel
import uuid
from datetime import date
from typing import Optional


# Define the SQLModel
# Fields - name, ip_address, location, device_type, make, model, os version, end_of_support
class InventoryBase(SQLModel):
    name: str | None = Field(default=None, index=True)
    ip_address: str | None = Field(default=None)
    location: str | None = Field(default=None)
    state: str | None = Field(default=None)
    device_type: str | None = Field(index=True)
    make: str | None = Field(index=True)
    model: str | None = Field(index=True)
    os_version: str | None = Field(default=None)
    end_of_support: date | None = Field(default=None)


class Inventory(InventoryBase, table=True):
    # id: int | None = Field(default=None, primary_key=True)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class InventoryItems(InventoryBase):
    # id: int
    id: uuid.UUID


class InventoryUpdate(SQLModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None
    state: Optional[str] = None
    device_type: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    os_version: Optional[str] = None
    end_of_support: Optional[date] = None
