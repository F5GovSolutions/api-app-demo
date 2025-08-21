from sqlmodel import Field, Session, SQLModel
import uuid


# Define the SQLModel
# Fields - name, ip_address, location, device_type, make, model, os version, end_of_support
class InventoryBase(SQLModel):
    name: str | None = Field(default=None, index=True)
    ip_address: str | None = Field(default=None)
    location: str | None = Field(default=None)
    device_type: str | None = Field(index=True)
    make: str | None = Field(index=True)
    model: str | None = Field(index=True)
    os_version: str | None = Field(default=None)
    end_of_support: str | None = Field(default=None)


class Inventory(InventoryBase, table=True):
    # id: int | None = Field(default=None, primary_key=True)
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class InventoryItems(InventoryBase):
    # id: int
    id: uuid.UUID


class InventoryUpdate(InventoryBase):
    name: str | None = Field(default=None, index=True)
    ip_address: str | None = Field(default=None)
    location: str | None = Field(default=None)
    device_type: str | None = Field(index=True)
    make: str | None = Field(index=True)
    model: str | None = Field(index=True)
    os_version: str | None = Field(default=None)
    end_of_support: str | None = Field(default=None)
