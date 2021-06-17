from sqlalchemy.orm import Session

from . import models, schemas


def get_schools(db: Session, filters: schemas.SchoolsStatsQuerySchema):

    filters_objects = get_schools_filters_objects(filters)

    return db.query(models.SchoolsStatsEntry).filter(*filters_objects).all()



def add_chart(db: Session):

    new_chart = models.Chart()
    db.add(new_chart)   
    db.commit()
    db.refresh(new_chart)

    return new_chart.id



def get_schools_filters_objects(filters: schemas.SchoolsStatsQuerySchema):

    filters_objects=[]

    filters_objects.append(models.SchoolsStatsEntry.Category == filters.category)

    if filters.female_pct_at_least is not None:
        filters_objects.append(models.SchoolsStatsEntry.Female_pct >= filters.female_pct_at_least)
    if filters.female_pct_at_most is not None:
        filters_objects.append(models.SchoolsStatsEntry.Female_pct <= filters.female_pct_at_most)

    if filters.male_pct_at_least is not None:
        filters_objects.append(models.SchoolsStatsEntry.Male_pct >= filters.male_pct_at_least)
    if filters.male_pct_at_most is not None:
        filters_objects.append(models.SchoolsStatsEntry.Male_pct <= filters.male_pct_at_most)

    if filters.black_pct_at_least is not None:
        filters_objects.append(models.SchoolsStatsEntry.Black_pct >= filters.black_pct_at_least)
    if filters.black_pct_at_most is not None:
        filters_objects.append(models.SchoolsStatsEntry.Black_pct <= filters.black_pct_at_most)

    if filters.asian_pct_at_least is not None:
        filters_objects.append(models.SchoolsStatsEntry.Asian_pct >= filters.asian_pct_at_least)
    if filters.asian_pct_at_most is not None:
        filters_objects.append(models.SchoolsStatsEntry.Asian_pct <= filters.asian_pct_at_most)

    if filters.white_pct_at_least is not None:
        filters_objects.append(models.SchoolsStatsEntry.White_pct >= filters.white_pct_at_least)
    if filters.white_pct_at_most is not None:
        filters_objects.append(models.SchoolsStatsEntry.White_pct <= filters.white_pct_at_most)

    if filters.other_pct_at_least is not None:
        filters_objects.append(models.SchoolsStatsEntry.Other_pct >= filters.other_pct_at_least)
    if filters.other_pct_at_most is not None:
        filters_objects.append(models.SchoolsStatsEntry.Other_pct <= filters.other_pct_at_most)

    return filters_objects


def get_chart(db: Session, chart_id: int): 
    
    return db.query(models.Chart).filter(models.Chart.id == chart_id).first()

