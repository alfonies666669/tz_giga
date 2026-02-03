import pytest

from tools.giga_client import get_access_token


@pytest.fixture(scope="session")
def access_token():
    try:
        return get_access_token()
    except Exception as e:
        pytest.skip(f"GigaChat auth is not configured: {e}")
