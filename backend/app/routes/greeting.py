from fastapi import APIRouter

router = APIRouter(prefix="/greeting", tags=["greeting"])

@router.get("")
def greeting(name: str = "World"):
    return {"message": f"Hello, {name}!"}