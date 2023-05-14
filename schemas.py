from pydantic import BaseModel
from typing import Optional, List

class MovieCountMonth(BaseModel):
    month_name: str
    quantity: int

    class Config:
        orm_mode = True

class MovieCountDayOfWeek(BaseModel):
    day_of_week: str
    quantity: int

    class Config:
        orm_mode = True

class MovieCountCountry(BaseModel):
    country: str
    quantity: int

    class Config:
        orm_mode = True

class Franchise(BaseModel):
    belongs_to_collection: str
    quantity: int
    total_revenue: float
    average_revenue: Optional[float]

    class Config:
        orm_mode = True

class Producer(BaseModel):
    production_companies: str
    total_revenue: float = 0.0
    quantity: int = 0

    class Config:
        orm_mode = True

class Return(BaseModel):
    movie: str
    investment: float
    profit: float
    returns: float
    year: int