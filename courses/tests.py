import requests
import time
import pytest
import random


@pytest.fixture
def last_course_id():
    headers = {'Authorization': 'Token 4c53a889892b34fa807a80049487c6e34ab3cc9b'}
    url_base_courses = 'http://127.0.0.1:8000/api/v2/courses/'
    courses = requests.get(url=url_base_courses, headers=headers)
    last_course_id = courses.json()['results'][-1]['id']
    return last_course_id


@pytest.fixture
def last_evaluation_id():
    headers = {'Authorization': 'Token 4c53a889892b34fa807a80049487c6e34ab3cc9b'}
    evaluations = requests.get(url='http://127.0.0.1:8000/api/v2/evaluations/', headers=headers)
    last_evaluation_id = evaluations.json()['results'][-1]['id']
    return last_evaluation_id


class TestCourses:
    headers = {'Authorization': 'Token 4c53a889892b34fa807a80049487c6e34ab3cc9b'}
    url_base_courses = 'http://127.0.0.1:8000/api/v2/courses/'
    course_id = None

    def test_get_courses(self):
        response = requests.get(url=self.url_base_courses, headers=self.headers)

        assert response.status_code == 200

    def test_post_course(self):
        now = time.time()
        new_course = {
            "title": f"MongoDB Course for Beginners {now}",
            "url": f"http://deskocean.com/mongodb-b-course-{now}"
        }

        response = requests.post(url=self.url_base_courses, headers=self.headers, data=new_course)

        assert response.status_code == 201
        assert response.json()['title'] == new_course['title']

    def test_get_course(self, last_course_id):
        response = requests.get(url=f'{self.url_base_courses}{last_course_id}/', headers=self.headers)

        assert response.status_code == 200

    def test_put_course(self, last_course_id):
        now = time.time()
        course_updated = {
            "title": f"MongoDB Course for Beginners{now}",
            "url": f"http://deskocean.com/mongodb-b-course{now}"
        }

        response = requests.put(url=f'{self.url_base_courses}{last_course_id}/', headers=self.headers, data=course_updated)
        assert response.status_code == 200
        assert response.json()['title'] == course_updated['title']

    def test_delete_course(self, last_course_id):
        response = requests.delete(url=f'{self.url_base_courses}{last_course_id}/', headers=self.headers)
        assert response.status_code == 204 and len(response.text) == 0


class TestEvaluations:
    headers = {'Authorization': 'Token 4c53a889892b34fa807a80049487c6e34ab3cc9b'}
    url_base_evaluations = 'http://127.0.0.1:8000/api/v2/evaluations/'

    def test_get_evaluations(self):
        response = requests.get(url=self.url_base_evaluations, headers=self.headers)

        assert response.status_code == 200

    def test_post_evaluation(self, last_course_id):
        new_evaluation = {
            "course": last_course_id,
            "name": "Daniel",
            "email": "daniel@gmail.com",
            "comment": "It was good.",
            "evaluation": random.randint(0, 5)
        }

        response = requests.post(url=self.url_base_evaluations, headers=self.headers, data=new_evaluation)

        assert response.status_code == 201
        assert response.json()['name'] == new_evaluation['name']

    def test_get_evaluation(self, last_evaluation_id):
        response = requests.get(url=f'{self.url_base_evaluations}{last_evaluation_id}/', headers=self.headers)

        assert response.status_code == 200

    def test_put_evaluation(self, last_evaluation_id, last_course_id):

        evaluation_updated = {
            "course": last_course_id,
            "name": "Daniel",
            "email": "daniel@gmail.com",
            "comment": "It was good.",
            "active": True,
            "evaluation": 4.0
        }

        response = requests.put(url=f'{self.url_base_evaluations}{last_evaluation_id}/',
                                headers=self.headers,
                                data=evaluation_updated)

        print(response.text)
        assert response.status_code == 200
        assert response.json()['name'] == evaluation_updated['name']

    def test_delete_course(self, last_evaluation_id):
        response = requests.delete(url=f'{self.url_base_evaluations}{last_evaluation_id}/',
                                   headers=self.headers)
        print(response)
        assert response.status_code == 204 and len(response.text) == 0
