from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import strawberry
from strawberry.fastapi import GraphQLRouter
import db_conn
from inventory_api import inventory_api
from inventory_ui import inventory_ui
from contextlib import asynccontextmanager
from graphql_schema import schema


templates = Jinja2Templates(directory="templates")


# Create Database Tables on Startup
# ToDO - This is not the best way to create tables
# look at using Alembic for migrations
@asynccontextmanager
async def lifespan(app: FastAPI):
    db_conn.create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Network Inventory API",
    description="Network Inventory API documentation with REST and GraphQL endpoints.",
    version="1.0.0",
)
# GraphQL router
graphql_app = GraphQLRouter(schema)

# Mount static files and include routers
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(inventory_api)
app.include_router(inventory_ui)
app.include_router(graphql_app, prefix="/graphql")


# Home Page
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
