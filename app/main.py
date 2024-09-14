from fastapi import FastAPI, Request
from .api import products, users, orders, cart
from .utils.logging import configure_logging
import structlog

configure_logging()

app = FastAPI()

logger = structlog.get_logger()

app.include_router(products.router)
app.include_router(users.router)
# app.include_router(orders.router)
app.include_router(cart.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Request received", method=request.method, url=request.url.path)
    
    response = await call_next(request)
    
    logger.info("Request completed", method=request.method, url=request.url.path, status_code=response.status_code)
    
    return response

@app.get("/")
async def root():
    logger.info("Handling request in the root endpoint")
    return {"message": "Welcome to the RediBuy E-commerce API"}