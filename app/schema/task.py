from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Task(BaseModel):
    id : int = Field(...,gt=1,description="Id of the task")
    name : str = Field(...,description="Name of the task")
    description : str 
    created_at : datetime
    priority : str =Field("Low",descrition ="Priority of the task High/Low/Medium")
    is_completed : bool = False

class TaskUpdate(BaseModel):
    name : Optional[str] = Field(None,description="Name of the task")
    description : Optional[str] = None
    priority : Optional[str] =Field(None,descrition ="Priority of the task High/Low/Medium")
    is_completed : Optional[bool] = None
