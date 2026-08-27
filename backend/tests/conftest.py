import pytest

from app import create_app


@pytest.fixture
def app():
    flask_app = create_app()
    with flask_app.app_context():
        yield flask_app
