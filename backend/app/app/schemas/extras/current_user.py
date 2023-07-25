from pydantic import BaseModel, ConfigDict, Field
from pydantic.dataclasses import dataclass

config = ConfigDict(validate_assignment=True)


@dataclass(config=config)
class CurrentUser(BaseModel):
    id: str = Field(None, description="User ID")
