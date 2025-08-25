from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from typing import List

from .schemas import UserSchema

User = get_user_model()
router = Router()

@router.get("/", response=List[UserSchema])
@paginate(PageNumberPagination, page_size=20)
def list_users(request):
    """
    List all users with pagination.
    """
    return User.objects.all()
