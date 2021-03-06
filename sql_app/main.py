from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from . import crud, schemas
from .celery_tasks import save_chart
from .database import SessionLocal

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.post("/school_entries/", response_model=schemas.SchoolsStatsResponse)
def get_schools_entries_and_create_chart(filters: schemas.SchoolsStatsQuerySchema, db: Session = Depends(get_db)):

    items = crud.get_schools(db,filters)

    if items:
        id = crud.add_chart(db)

        save_chart.delay(filters.dict(),id)

        url='/charts/'+str(id)
        return schemas.SchoolsStatsResponse(url=url, SchoolsStatsEntries=items)
    else:
        return schemas.SchoolsStatsResponse(url='', SchoolsStatsEntries=items)


@app.get("/charts/{chart_id}")
def get_chart_by_id(chart_id: int, db: Session = Depends(get_db)):
    chart = crud.get_chart(db, chart_id=chart_id)

    try:
        return FileResponse(chart.path)
    except:
        raise HTTPException(status_code=404, detail="Chart not found")

    