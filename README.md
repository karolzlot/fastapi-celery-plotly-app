# Celery-FastAPI-Plotly demo app

## Description:

This app is based on four docker services managed by docker-compose: PostgreSQL, redis, Celery and main Python-FastAPI webserver service.

When main docker service is started and database is empty, bash script is executed which runs Celery task, which downloads data from New York open data server and puts them in database. Data contains grades of students in New York City.

Then API client can make API request to get students data. Filters can be optionally applied. Additionally link to chart is provided in response. 

Chart is not available immediately. It is generated in separate Celery task and then stored on Docker volume with its path stored in database. 


Tested on Python 3.9.5


## How to run app:
1. Rename `.env.dev.example` to `.env.dev`. This file contains environmental variables.
2. (Recommended) In `.env.dev` file at least change both `POSTGRES_PASSWORD` and `DB_PASS` to new password (the same password for both variables).
3. Run 
```
docker-compose up --build
```
4. Go to app address:
http://localhost:8080/docs


### Filters description for `/school_entries/` endpoint

`category` is enum, as described in `/docs`, takes one of:
```
'All Students'
'Attend school outside district of residence'
'English Language Learners'
'Poverty'
'Reside in temporary housing'
'Students with Disabilities'
```


The rest of filters takes float between 0.00 and 1.00.


Client doesn't need to send any of them, if not sent app will use default values:

```
{
  "category": "All Students",
  "female_pct_at_least": 0,
  "female_pct_at_most": 1,
  "male_pct_at_least": 0,
  "male_pct_at_most": 1,
  "black_pct_at_least": 0,
  "black_pct_at_most": 1,
  "asian_pct_at_least": 0,
  "asian_pct_at_most": 1,
  "white_pct_at_least": 0,
  "white_pct_at_most": 1,
  "other_pct_at_least": 0,
  "other_pct_at_most": 1
}
```

## How to run tests:
1. Create virtual env for this project.
```
python -m venv .venv --prompt coding-challenge
.\.venv\Scripts\python -m pip install -U pip
.\.venv\Scripts\python -m pip install -U wheel
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\pip install pytest pytest-docker requests
source .venv/bin/activate
````
2. Run 
```
pytest -s -v
```



# What can be improved (to-do list):
1. Add unit tests.
2. Change models to use Enum for `category`.
I already changed part of Pydantic `schema`. However when I tried to change SQLAlchemy `models`, pandas didn't want to work properly. So I put this task aside for the time being.
You can see my attempt in branch `switch_type_to_enum`
3. Separate `requirements.txt` for `app` and `celery` microservices.
4. Remove duplicating env vars from .env.dev file 
5. Allow to choose type of exam between MATH and ELA. Currently MATH exam is hardcoded.
6. Add simple html form interface to choose filters easier (to speed up debugging).
7. Allow to choose chart file format also as HTML.
8. Change plotly chart to use `mapbox` to have nicer background and colors.



# Details about project decisions

## Gunicorn
I added `gunicorn` in addition to `uvicorn` to make use of multiple CPU cores. 

## POST vs GET
I chose `POST` request type for `/school_entries/` because it creates chart, so it has side effect.



# Blueprint


![blueprint](./img/blueprint.png)




# Example charts generated by this app:

```
{
  "category": "All Students"
}
```
![chart1](./img/example_all_students.png)


```
{
  "category": "All Students",
  "female_pct_at_least": 0.5
}
```
![chart1](./img/example_at_least_50_pct_females.png)


```
{
  "category": "All Students",
  "black_pct_at_least": 0.6
}
```
![chart2](./img/example_at_least_60_pct_black.png)


```
{
  "category": "All Students",
  "asian_pct_at_least": 0.4
}
```
![chart2](./img/example_at_least_40_pct_asian.png)



```
{
  "category": "Students with Disabilities"
}
```
![chart2](./img/example_students_with_disabilities.png)



```
{
  "category": "English Language Learners"
}
```
![chart2](./img/example_english_language_learners.png)



```
{
  "category": "Poverty"
}
```
![chart2](./img/example_poverty.png)



```
{
  "category": "Reside in temporary housing"
}
```
![chart2](./img/example_reside_in_temporary_housing.png)



```
{
  "category": "Attend school outside district of residence"
}
```
![chart2](./img/example_attend_school_outside_district_of_residence.png)

