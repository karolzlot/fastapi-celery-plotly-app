from enum import Enum

class StudentCategoryEnum(str, Enum):
    all = 'All Students'
    outside_residence = 'Attend school outside district of residence'
    english_learners = 'English Language Learners'
    poverty = 'Poverty'
    temporary_housing = 'Reside in temporary housing'
    disability = 'Students with Disabilities'