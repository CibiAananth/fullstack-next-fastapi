from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: str = Field(None, description="User ID")

    class Config:
        validate_assignment = True
