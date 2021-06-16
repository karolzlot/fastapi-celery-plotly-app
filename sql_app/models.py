from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, Text, Float
from sqlalchemy.orm import relationship

import enum
from sqlalchemy import Integer, Enum

from .database import Base

from .schemas import StudentCategoryEnum


# class StudentCategoryEnum(str, Enum):
#     all = 'All Students'
#     outside_residence = 'Attend school outside district of residence'
#     english_learners = 'English Language Learners'
#     poverty = 'Poverty'
#     temporary_housing = 'Reside in temporary housing'
#     disability = 'Students with Disabilities'


class SchoolsStatsEntry(Base):
    __tablename__ = 'schools_stats_entries'
    id = Column(Integer, primary_key=True)

    DBN = Column(Text)
    District = Column(Integer)
    # Category = Column(Text)
    Category = Column(Enum(StudentCategoryEnum))

    Female_pct = Column(Float(53))
    Male_pct = Column(Float(53))

    Asian_pct = Column(Float(53))
    Black_pct = Column(Float(53))
    Hispanic_pct = Column(Float(53))
    Other_pct = Column(Float(53))
    White_pct = Column(Float(53))

    ELA_Level_1 = Column(Integer)
    ELA_Level_2 = Column(Integer)
    ELA_L3_and_L4 = Column(Integer)

    MATH_Level_1 = Column(Integer)
    MATH_Level_2 = Column(Integer)
    MATH_L3_and_L4 = Column(Integer)



class Chart(Base):
    __tablename__ = 'charts'
    id = Column(BigInteger, primary_key=True)
    path = Column(Text)





