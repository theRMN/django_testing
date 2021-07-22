import pytest
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from students.models import Course


@pytest.mark.django_db
def test_get_first_course(api_client, courses_factory):
    courses_factory(_quantity=10)
    obj = Course.objects.first()
    url = reverse('courses-detail', kwargs={'pk': obj.id})
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert response.data['name'] == obj.name


@pytest.mark.django_db
def test_get_course_list(api_client, courses_factory):
    courses_factory(_quantity=3)
    url = reverse('courses-list')
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.django_db
def test_get_course_id(api_client):
    Course.objects.bulk_create([
        Course(id=4, name='test_1'),
        Course(id=5, name='test_2'),
        Course(id=8, name='test_3'),
    ])
    url = "%s?id=5" % reverse('courses-list')
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert response.data[0]['id'] == 5


@pytest.mark.django_db
def test_get_course_name(api_client):
    Course.objects.bulk_create([
        Course(name='test_1'),
        Course(name='test_2'),
        Course(name='test_3'),
    ])
    url = "%s?name=test_2" % reverse('courses-list')
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert response.data[0]['name'] == 'test_2'


@pytest.mark.django_db
def test_course_create(api_client):
    url = reverse('courses-list')
    payload = {
        'name': '1st'
    }
    response = api_client.post(url, data=payload)

    assert response.data['id']
    assert response.data['name'] == '1st'
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_course_update(api_client, courses_factory):
    courses_factory(_quantity=1)
    obj = Course.objects.first()
    url = reverse('courses-detail', kwargs={'pk': obj.id})
    payload = {
                'name': '1st'
            }
    response = api_client.patch(url, data=payload)

    assert response.status_code == HTTP_200_OK
    assert response.data['name'] == '1st'


@pytest.mark.django_db
def test_course_delete(api_client):
    obj = Course.objects.create(name='test_6')
    url = reverse('courses-detail', kwargs={'pk': obj.id})
    response = api_client.delete(url)

    assert response.status_code == HTTP_204_NO_CONTENT
