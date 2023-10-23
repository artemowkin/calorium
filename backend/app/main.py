from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .project.settings import settings
from .products.routes import router as products_router
from .auth.routes import router as auth_router
from .eating.routes import router as eatings_router
from .project.db import Base, engine


app = FastAPI(
    docs_url='/api/v1/docs' if settings.run_mode != 'prod' else None,
    redoc_url='/api/v1/redoc' if settings.run_mode != 'prod' else None,
    openapi_url='/api/v1/openapi' if settings.run_mode != 'prod' else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(products_router, prefix='/api/v1/products', tags=['products'])

app.include_router(auth_router, prefix='/api/v1/auth', tags=['auth'])

app.include_router(eatings_router, prefix='/api/v1/eatings', tags=['eatings'])

@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

