from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.params import File
from fastapi_limiter.depends import RateLimiter

from api.instances import auth_service, user_service
from schemas.users import UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def get_current_user_info(current_user: UserOut = Depends(auth_service.get_current_user)):
    return current_user


@router.post("/me/avatar", response_model=UserOut)
def change_avatar(file: UploadFile = File(...), current_user: UserOut = Depends(auth_service.get_current_user)):
    updated_user = user_service.change_avatar(current_user.id, file)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
