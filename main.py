from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routers import employee, asset, mapping, dashboard

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db() #initialize db
    yield

#starting the fastapi server
app = FastAPI(title="Employee Asset Mapping", lifespan=lifespan)

#routing each route
app.include_router(employee.router, prefix="/employee", tags=["Employee APIs"])
app.include_router(asset.router, prefix="/asset", tags=["Asset APIs"])
app.include_router(mapping.router, prefix="/mapping", tags=["Mapping APIs"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard APIs"])