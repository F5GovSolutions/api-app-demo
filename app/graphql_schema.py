import strawberry
from typing import List, Optional
import uuid
from datetime import date
from sqlmodel import Session, select
from db_conn import get_session, engine
import models


@strawberry.type
class InventoryType:
    id: uuid.UUID
    name: Optional[str] = None
    ip_address: Optional[str] = strawberry.field(name="ipAddress")
    location: Optional[str] = None
    state: Optional[str] = None
    device_type: Optional[str] = strawberry.field(name="deviceType")
    make: Optional[str] = None
    model: Optional[str] = None
    os_version: Optional[str] = strawberry.field(name="osVersion")
    end_of_support: Optional[date] = strawberry.field(name="endOfSupport")


@strawberry.input
class InventoryInput:
    name: Optional[str] = None
    ip_address: Optional[str] = strawberry.field(name="ipAddress")
    location: Optional[str] = None
    state: Optional[str] = None
    device_type: Optional[str] = strawberry.field(name="deviceType")
    make: Optional[str] = None
    model: Optional[str] = None
    os_version: Optional[str] = strawberry.field(name="osVersion")
    end_of_support: Optional[date] = strawberry.field(name="endOfSupport")


@strawberry.input
class InventoryUpdateInput:
    id: uuid.UUID
    name: Optional[str] = strawberry.UNSET
    ip_address: Optional[str] = strawberry.field(
        name="ipAddress", default=strawberry.UNSET
    )
    location: Optional[str] = strawberry.UNSET
    state: Optional[str] = strawberry.UNSET
    device_type: Optional[str] = strawberry.field(
        name="deviceType", default=strawberry.UNSET
    )
    make: Optional[str] = strawberry.UNSET
    model: Optional[str] = strawberry.UNSET
    os_version: Optional[str] = strawberry.field(
        name="osVersion", default=strawberry.UNSET
    )
    end_of_support: Optional[date] = strawberry.field(
        name="endOfSupport", default=strawberry.UNSET
    )


@strawberry.type
class Query:
    @strawberry.field
    def inventory_items(self) -> List[InventoryType]:
        session = next(get_session())
        try:
            inventory_items = session.exec(select(models.Inventory)).all()
            return [
                InventoryType(
                    id=item.id,
                    name=item.name,
                    ip_address=item.ip_address,
                    location=item.location,
                    state=item.state,
                    device_type=item.device_type,
                    make=item.make,
                    model=item.model,
                    os_version=item.os_version,
                    end_of_support=item.end_of_support,
                )
                for item in inventory_items
            ]
        finally:
            session.close()

    @strawberry.field
    def inventory_item(self, id: uuid.UUID) -> Optional[InventoryType]:
        session = next(get_session())
        try:
            inventory = session.get(models.Inventory, id)
            if inventory:
                return InventoryType(
                    id=inventory.id,
                    name=inventory.name,
                    ip_address=inventory.ip_address,
                    location=inventory.location,
                    state=inventory.state,
                    device_type=inventory.device_type,
                    make=inventory.make,
                    model=inventory.model,
                    os_version=inventory.os_version,
                    end_of_support=inventory.end_of_support,
                )
            return None
        finally:
            session.close()

    @strawberry.field
    def inventory_by_location(self, location: str) -> List[InventoryType]:
        session = next(get_session())
        try:
            inventory_items = session.exec(
                select(models.Inventory).where(models.Inventory.location == location)
            ).all()
            return [
                InventoryType(
                    id=item.id,
                    name=item.name,
                    ip_address=item.ip_address,
                    location=item.location,
                    state=item.state,
                    device_type=item.device_type,
                    make=item.make,
                    model=item.model,
                    os_version=item.os_version,
                    end_of_support=item.end_of_support,
                )
                for item in inventory_items
            ]
        finally:
            session.close()

    @strawberry.field
    def inventory_by_make(self, make: str) -> List[InventoryType]:
        session = next(get_session())
        try:
            inventory_items = session.exec(
                select(models.Inventory).where(models.Inventory.make == make)
            ).all()
            return [
                InventoryType(
                    id=item.id,
                    name=item.name,
                    ip_address=item.ip_address,
                    location=item.location,
                    state=item.state,
                    device_type=item.device_type,
                    make=item.make,
                    model=item.model,
                    os_version=item.os_version,
                    end_of_support=item.end_of_support,
                )
                for item in inventory_items
            ]
        finally:
            session.close()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_inventory_item(self, inventory: InventoryInput) -> InventoryType:
        session = next(get_session())
        try:
            # Check if name already exists
            if inventory.name:
                existing = session.exec(
                    select(models.Inventory).where(
                        models.Inventory.name == inventory.name
                    )
                ).first()
                if existing:
                    raise Exception(f"Name '{inventory.name}' already exists")

            db_inventory = models.Inventory(
                name=inventory.name,
                ip_address=inventory.ip_address,
                location=inventory.location,
                state=inventory.state,
                device_type=inventory.device_type,
                make=inventory.make,
                model=inventory.model,
                os_version=inventory.os_version,
                end_of_support=inventory.end_of_support,
            )
            session.add(db_inventory)
            session.commit()
            session.refresh(db_inventory)

            return InventoryType(
                id=db_inventory.id,
                name=db_inventory.name,
                ip_address=db_inventory.ip_address,
                location=db_inventory.location,
                state=db_inventory.state,
                device_type=db_inventory.device_type,
                make=db_inventory.make,
                model=db_inventory.model,
                os_version=db_inventory.os_version,
                end_of_support=db_inventory.end_of_support,
            )
        finally:
            session.close()


@strawberry.mutation
def update_inventory_item(
    self, info: strawberry.Info, inventory: InventoryUpdateInput
) -> Optional[InventoryType]:
    from sqlalchemy import text

    with Session(engine) as session:
        # First check if the item exists
        db_inventory = session.get(models.Inventory, inventory.id)
        if not db_inventory:
            raise Exception(f"Inventory item with id {inventory.id} not found")

        # Build update dictionary with only provided fields
        update_data = {}
        if inventory.name is not strawberry.UNSET:
            update_data["name"] = inventory.name
        if inventory.ip_address is not strawberry.UNSET:
            update_data["ip_address"] = inventory.ip_address
        if inventory.location is not strawberry.UNSET:
            update_data["location"] = inventory.location
        if inventory.state is not strawberry.UNSET:
            update_data["state"] = inventory.state
        if inventory.device_type is not strawberry.UNSET:
            update_data["device_type"] = inventory.device_type
        if inventory.make is not strawberry.UNSET:
            update_data["make"] = inventory.make
        if inventory.model is not strawberry.UNSET:
            update_data["model"] = inventory.model
        if inventory.os_version is not strawberry.UNSET:
            update_data["os_version"] = inventory.os_version
        if inventory.end_of_support is not strawberry.UNSET:
            update_data["end_of_support"] = inventory.end_of_support

        # Only proceed if there's something to update
        if not update_data:
            raise Exception("No fields provided for update")

        # Build dynamic SQL update statement
        set_clauses = []
        params = {}
        for field_name, field_value in update_data.items():
            set_clauses.append(f"{field_name} = :{field_name}")
            params[field_name] = field_value

        params["item_id"] = str(inventory.id)

        # Execute raw SQL to avoid SQLAlchemy's object tracking issues
        sql = f"UPDATE inventory SET {', '.join(set_clauses)} WHERE id = :item_id"
        session.execute(text(sql), params)
        session.commit()

        # Fetch the updated record
        updated_inventory = session.get(models.Inventory, inventory.id)
        session.refresh(updated_inventory)

        return InventoryType(
            id=updated_inventory.id,
            name=updated_inventory.name,
            ip_address=updated_inventory.ip_address,
            location=updated_inventory.location,
            state=updated_inventory.state,
            device_type=updated_inventory.device_type,
            make=updated_inventory.make,
            model=updated_inventory.model,
            os_version=updated_inventory.os_version,
            end_of_support=updated_inventory.end_of_support,
        )

    @strawberry.mutation
    def delete_inventory_item(self, id: uuid.UUID) -> bool:
        session = next(get_session())
        try:
            inventory = session.get(models.Inventory, id)
            if not inventory:
                raise Exception(f"Inventory item with id {id} not found")

            session.delete(inventory)
            session.commit()
            return True
        finally:
            session.close()


schema = strawberry.Schema(query=Query, mutation=Mutation)
