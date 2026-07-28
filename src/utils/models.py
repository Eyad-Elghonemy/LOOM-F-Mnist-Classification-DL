from pydantic import BaseModel


class PredictionRespond(BaseModel):
    
    class_index: int
    class_name: str
    confidence: float
    