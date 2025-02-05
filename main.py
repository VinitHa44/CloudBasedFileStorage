from fastapi import FastAPI
from app.config.database import lifespan
from app.routes.auth_routes import auth_router
from app.routes.product_routes import product_router

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(product_router)
