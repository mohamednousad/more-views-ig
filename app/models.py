from pydantic import BaseModel

class VehicleValuationRequest(BaseModel):
    make: str
    model: str
    year: int
    mileage: int

class VideoViewRequest(BaseModel):
    url: str
    view_count: int = 10
