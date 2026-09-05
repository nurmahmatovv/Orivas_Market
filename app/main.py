from fastapi import FastAPI

from app.core.config import settings

from app.routers import auth_router, category_router, listing_router, location_router
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
)

app.include_router(auth_router.router)
app.include_router(location_router.router)
app.include_router(listing_router.router)


# ...
app.include_router(category_router.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}