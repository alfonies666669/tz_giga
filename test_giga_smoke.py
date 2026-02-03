import pytest

from tools.giga_client import chat_completion, get_access_token


@pytest.fixture(scope="session")
def access_token():
    try:
        return get_access_token()
    except Exception as e:
        pytest.skip(f"GigaChat auth is not configured: {e}")


def test_chat_completions_smoke(access_token):
    response = chat_completion("Скажи 'привет' на 2 языках", access_token)
    assert "choices" in response
    assert isinstance(response["choices"], list)
    assert response["choices"], "choices пуст!"

    first_choice = response["choices"][0]
    message = first_choice.get("message") or {}
    content = message.get("content")

    assert isinstance(content, str)
    assert content.strip(), "Пустой контент из модели!"
