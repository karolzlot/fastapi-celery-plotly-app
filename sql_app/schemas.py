from typing import List, Optional


from pydantic import BaseModel



class SchoolsStatsQuerySchema(BaseModel):


    category: Optional[str]='All Students'
    female_pct_more_than: Optional[float]
    female_pct_less_than: Optional[float]
    male_pct_more_than: Optional[float]
    male_pct_less_than: Optional[float]
    black_pct_more_than: Optional[float]
    black_pct_less_than: Optional[float]
    asian_pct_more_than: Optional[float]
    asian_pct_less_than: Optional[float]
    white_pct_more_than: Optional[float]
    white_pct_less_than: Optional[float]
    other_pct_more_than: Optional[float]
    other_pct_less_than: Optional[float]


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