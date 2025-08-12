from fastapi import APIRouter, Query
from app.routes.dto.PostGreetDTO import PostGreetDTO

router = APIRouter(prefix="/greeting", tags=["greeting"])

@router.get("")
def greeting(name: str = Query("World", min_length=1, max_length=50)):
    return {"message": f"Hello, {name}!"}

@router.post("")
def post_greet(dto: PostGreetDTO):
    return {"message": f"Hello, {dto.name}!"}