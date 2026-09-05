from fastapi import FastAPI

from app.core.config import settings


from app.routers import admin_router, auth_router, category_router, favorite_router, listing_router, listing_image_router, location_router

# ...

# ...
from fastapi.staticfiles import StaticFiles

# app = FastAPI(...) qatoridan keyin:

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
)
app.mount("/static/uploads", StaticFiles(directory="static/uploads"), name="uploads")
app.include_router(auth_router.router)
app.include_router(location_router.router)
app.include_router(listing_router.router)
app.include_router(favorite_router.router)
app.include_router(listing_image_router.router)

# ...
app.include_router(admin_router.router)
# ...
app.include_router(category_router.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}