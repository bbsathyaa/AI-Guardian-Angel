from fastapi import APIRouter


router = APIRouter()


@router.get("/ready")
async def ready():
return {"ready": True}


@router.get("/live")
async def live():
return {"live": True}
