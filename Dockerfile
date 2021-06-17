# Python image to use.
FROM python:3.9

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the working directory to /app
WORKDIR /app

RUN pip install FastAPI gunicorn uvicorn --no-cache-dir

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# Copy the rest of the working directory contents into the container at /app
COPY ./sql_app /app/sql_app


EXPOSE 80

# Run the web service on container startup.
CMD gunicorn sql_app.main:app -b 0.0.0.0:80 -k uvicorn.workers.UvicornWorker --workers 4

