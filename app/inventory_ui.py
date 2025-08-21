# This file contains the UI routes for the inventory items
import uuid
from fastapi import APIRouter, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
import models
from db_conn import engine, get_session


inventory_ui = APIRouter()

templates = Jinja2Templates(directory="templates")


# Get all inventory for the web page
@inventory_ui.get("/inventory", response_class=HTMLResponse, include_in_schema=False)
async def read_item(request: Request, session: Session = Depends(get_session)):
    inventory = session.exec(select(models.Inventory)).all()
    return templates.TemplateResponse(
        "inventory.html", {"request": request, "inventory": inventory}
    )


@inventory_ui.get("/inventory/add", include_in_schema=False)
def get_inventory_ui(request: Request, session: Session = Depends(get_session)):
    inventory = session.exec(select(models.Inventory)).all()
    return templates.TemplateResponse(
        "table_row.html", {"request": request, "inventory": inventory}
    )


@inventory_ui.get("/inventory/{item_id}/edit", include_in_schema=False)
async def edit_inventory_item(
    request: Request, item_id: uuid.UUID, session: Session = Depends(get_session)
):
    inventory_item = session.get(models.Inventory, item_id)
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse(
        "edit_inventory_form.html",
        {"request": request, "inventory_item": inventory_item},
    )


@inventory_ui.post("/inventory/add", include_in_schema=False)
async def add_inventory_ui(
    request: Request,
    name: str = Form(...),
    ip_address: str = Form(...),
    location: str = Form(...),
    device_type: str = Form(...),
    make: str = Form(...),
    model: str = Form(...),
    os_version: str = Form(...),
    end_of_support: str = Form(...),
    session: Session = Depends(get_session),
):
    existing_inventory = session.exec(
        select(models.Inventory).where(models.Inventory.name == name)
    ).first()
    if existing_inventory:
        return Response(content="Name already exists", status_code=400)

    inventory = models.Inventory(
        name=name,
        ip_address=ip_address,
        location=location,
        device_type=device_type,
        make=make,
        model=model,
        os_version=os_version,
        end_of_support=end_of_support,
    )
    session.add(inventory)
    session.commit()
    session.refresh(inventory)

    return Response(status_code=204, headers={"HX-Redirect": "/inventory"})


@inventory_ui.delete("/inventory/{item_id}", include_in_schema=False)
async def delete_inventory_ui(item_id: uuid.UUID):
    with Session(engine) as session:
        inventory_item = session.get(models.Inventory, item_id)
        if not inventory_item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(inventory_item)
        session.commit()
    return Response(status_code=204, headers={"HX-Redirect": "/inventory"})


@inventory_ui.patch(
    "/inventory/{item_id}",
    response_model=models.InventoryItems,
    include_in_schema=False,
)
async def update_inventory_item(
    item_id: uuid.UUID,
    name: str = Form(...),
    ip_address: str = Form(...),
    location: str = Form(...),
    device_type: str = Form(...),
    make: str = Form(...),
    model: str = Form(...),
    os_version: str = Form(...),
    end_of_support: str = Form(...),
    session: Session = Depends(get_session),
):
    inventory_item = session.get(models.Inventory, item_id)
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update the inventory item with the provided data
    inventory_item.name = name
    inventory_item.ip_address = ip_address
    inventory_item.location = location
    inventory_item.device_type = device_type
    inventory_item.make = make
    inventory_item.model = model
    inventory_item.os_version = os_version
    inventory_item.end_of_support = end_of_support

    session.add(inventory_item)
    session.commit()
    session.refresh(inventory_item)
    print(f"Updated item: {inventory_item}")
    return Response(
        content="<script>window.location.reload();</script>", media_type="text/html"
    )
