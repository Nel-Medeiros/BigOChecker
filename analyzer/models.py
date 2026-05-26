from pydantic import BaseModel


class FunctionResult(BaseModel):
    name: str
    time_complexity: str
    space_complexity: str
    explanation: str
