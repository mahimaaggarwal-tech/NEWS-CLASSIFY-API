from fastapi import APIRouter, Depends
from app.business.auth_service import AuthService
from app.models.user import UserLogin

router = APIRouter()

@router.post("/login", summary="User login")
def login(user: UserLogin, service: AuthService = Depends()):
    """
    Log in a user and return a JWT token.
    """
    token = service.authenticate(user.username, user.password)
    return {"access_token": token}


@router.post("/logout", summary="User logout")
def logout(service: AuthService = Depends()):
    """
    Log out the current user by invalidating the token.
    """
    service.logout()
    return {"message": "User logged out successfully"}

