from pydantic import BaseModel, constr


class TaskCreate(BaseModel):
    title: constr(min_length=1, max_length=100)  # type: ignore
    description: constr(min_length=1, max_length=1000)  # type: ignore
