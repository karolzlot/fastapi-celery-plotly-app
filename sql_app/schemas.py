from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class StudentCategoryEnum(str, Enum):
    all = 'All Students'
    outside_residence = 'Attend school outside district of residence'
    english_learners = 'English Language Learners'
    poverty = 'Poverty'
    temporary_housing = 'Reside in temporary housing'
    disability = 'Students with Disabilities'



class SchoolsStatsQuerySchema(BaseModel):
    category: StudentCategoryEnum=StudentCategoryEnum.all
    female_pct_more_than: Optional[float]=0.0
    female_pct_less_than: Optional[float]=1.0
    male_pct_more_than: Optional[float]=0.0
    male_pct_less_than: Optional[float]=1.0
    black_pct_more_than: Optional[float]=0.0
    black_pct_less_than: Optional[float]=1.0
    asian_pct_more_than: Optional[float]=0.0
    asian_pct_less_than: Optional[float]=1.0
    white_pct_more_than: Optional[float]=0.0
    white_pct_less_than: Optional[float]=1.0
    other_pct_more_than: Optional[float]=0.0
    other_pct_less_than: Optional[float]=1.0

    class Config:
        orm_mode = True



class SchoolsStatsEntrySchema(BaseModel):
    id:int

    DBN: str
    District: int
    Category: str

    Female_pct: float
    Male_pct: float

    Asian_pct: float
    Black_pct: float
    Hispanic_pct: float
    Other_pct: float
    White_pct: float

    ELA_Level_1: int
    ELA_Level_2: int
    ELA_L3_and_L4: int

    MATH_Level_1: int
    MATH_Level_2: int
    MATH_L3_and_L4: int

    class Config:
        orm_mode = True



class SchoolsStatsResponse(BaseModel):
    url: Optional[str]
    SchoolsStatsEntries: List[SchoolsStatsEntrySchema]

    class Config:
        orm_mode = True