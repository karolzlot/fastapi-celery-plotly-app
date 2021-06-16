from .celery import app
from celery.signals import worker_ready


@app.task
def db_init():
    from . import models
    from .database import SessionLocal, engine

    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, 'schools_stats_entries') or not engine.dialect.has_table(connection, 'charts'):  # If table don't exist, Create.
            models.Base.metadata.create_all(bind=engine)

            from .db_init import db_init
            db_init()

@app.task
def save_chart(filters_dict,id):
    from . import models, schemas
    import pandas as pd

    filters = schemas.SchoolsStatsQuerySchema.parse_obj(filters_dict)

    from .crud import get_schools_filters_objects
    filters_objects = get_schools_filters_objects(filters)

    from .database import SessionLocal
    with SessionLocal() as db:

        

        query = db.query(models.SchoolsStatsEntry).filter(*filters_objects)
        df = pd.read_sql(query.statement, query.session.bind)

        df2 = df.groupby(['District'])[['MATH_Level_1', 'MATH_Level_2', 'MATH_L3_and_L4']].sum().reset_index()
        df2['MATH_indicator']=(df2['MATH_Level_1']+df2['MATH_Level_2']*2+df2['MATH_L3_and_L4']*3)/(df2['MATH_Level_1']+df2['MATH_Level_2']+df2['MATH_L3_and_L4'])

        import json
        import plotly.express as px

        # read the neighborhood population data into a DataFrame and load the GeoJSON data
        nycmap = json.load(open("School Districts.geojson"))

        # call Plotly Express choropleth function to visualize data
        fig = px.choropleth_mapbox(df2,
                                geojson=nycmap,
                                locations="District",
                                featureidkey="properties.school_dist",
                                color="MATH_indicator",
                                color_continuous_scale="viridis",
                                mapbox_style="carto-positron",
                                zoom=9, center={"lat": 40.7, "lon": -73.9},
                                opacity=0.7,
                                #    labels="District",
                                title="District",
                                hover_name="District"
                                )
        path=f"/saved_charts/fig{str(id)}.png"

        


        fig.write_image(path)
        
        q = db.query(models.Chart).filter(models.Chart.id==id).one().path=path
        db.commit()




    pass

