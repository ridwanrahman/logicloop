from ninja import Schema
from datetime import datetime
from typing import Optional, List
from pydantic import Field


class UserSchema(Schema):
    user_id: int = Field(alias='id')  # Use alias for the database field
    username: str
    email: str
    first_name: str
    last_name: str
    bio: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_username: Optional[str] = None
    total_points: int
    problems_solved: int

class UserProfileSchema(Schema):
    user_id: int
    preferred_language: str
    skill_level: str
    location: Optional[str] = None
    website: Optional[str] = None
    is_public: bool
    created_at: datetime
    updated_at: datetime
