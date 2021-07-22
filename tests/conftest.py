import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def students_factory():
    def factory(**kwargs):
        return baker.make('Student', **kwargs)
    return factory


@pytest.fixture
def courses_factory():
    def factory(**kwargs):
        return baker.make('Course', **kwargs)
    return factory

