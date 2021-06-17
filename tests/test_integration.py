import json
import os
from time import sleep

import pytest
import requests
from requests.exceptions import ConnectionError

headers = {'accept': 'application/json',
        'Content-Type': 'application/json'}


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "", "docker-compose.yml")


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("app", 80)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url+'/docs')
    )
    return url


def test_status_code_docs(http_service):
    status = 200
    response = requests.get(http_service + "/docs/")
    assert response.status_code == status



def test_rest1_all_students(http_service):
    status1 = 404
    for i in range(10): # wait up to 10s for server to be ready
        response1 = requests.get(http_service + "/charts/1") 
        if response1.status_code != 500: 
            break
        sleep(1)

    sleep(5)  # needed, because if too early chart won't be created despite status code 200
    status2 = 200
    data = {
        "category": "All Students"
        }

    response2 = requests.post(http_service + "/schools/",data=json.dumps(data), headers=headers) 

    number_of_entries= len(response2.json()["SchoolsStatsEntries"])
    # print(number_of_entries)

    status3 = 200
    for i in range(100): # wait up to 10s for chart to be ready
        response3 = requests.get(http_service + "/charts/1") 
        if response3.status_code != 404: 
            break
        sleep(0.1)

    assert response1.status_code == status1
    assert response2.status_code == status2
    assert response3.status_code == status3


def test_rest2_all_filters(http_service):
    status1 = 404
    for i in range(10): # wait up to 10s for server to be ready
        response1 = requests.get(http_service + "/charts/2") 
        if response1.status_code != 500: 
            break
        sleep(1)

    status2 = 200
    data = {
        "category": "Students with Disabilities",
        "female_pct_at_least": 0.01,
        "female_pct_at_most": 0.99,
        "male_pct_at_least": 0.01,
        "male_pct_at_most": 0.99,
        "black_pct_at_least": 0.01,
        "black_pct_at_most": 0.99,
        "asian_pct_at_least": 0.01,
        "asian_pct_at_most": 0.99,
        "white_pct_at_least": 0.01,
        "white_pct_at_most": 0.99,
        "other_pct_at_least": 0.01,
        "other_pct_at_most": 0.99
        }
    response2 = requests.post(http_service + "/schools/",data=json.dumps(data), headers=headers) 

    status3 = 200
    for i in range(100): # wait up to 10s for chart to be ready
        response3 = requests.get(http_service + "/charts/2") 
        if response3.status_code != 404: 
            break
        sleep(0.1)

    assert response1.status_code == status1
    assert response2.status_code == status2
    assert response3.status_code == status3


def test_rest3_empty_response(http_service):
    status = 200
    data = {
        "category": "Attend school outside district of residence",
        "other_pct_at_least": 0.55,
        "other_pct_at_most": 0.45
        }

    response = requests.post(http_service + "/schools/",data=json.dumps(data), headers=headers) 

    expected_response={
        "url": "",
        "SchoolsStatsEntries": []
        }

    assert response.json() == expected_response
    assert response.status_code == status


def test_rest4_all_zeros(http_service):

    status = 200
    data = {
        "category": "All Students",
        "female_pct_at_least": 0,
        "female_pct_at_most": 0,
        "male_pct_at_least": 0,
        "male_pct_at_most": 0,
        "black_pct_at_least": 0,
        "black_pct_at_most": 0,
        "asian_pct_at_least": 0,
        "asian_pct_at_most": 0,
        "white_pct_at_least": 0,
        "white_pct_at_most": 0,
        "other_pct_at_least": 0,
        "other_pct_at_most": 0
        }

    response = requests.post(http_service + "/schools/",data=json.dumps(data), headers=headers) 

    expected_response={
        "url": "",
        "SchoolsStatsEntries": []
        }

    assert response.json() == expected_response
    assert response.status_code == status

