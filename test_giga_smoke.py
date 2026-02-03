import allure

from tools.giga_client import chat_completion


@allure.tag("positive", "smoke")
@allure.title("Smoke: запрос к /chat/completions")
def test_positive_chat_completions_smoke(access_token):
    """Проверяем что вообще что-то приходит"""
    response = chat_completion("Скажи 'привет' на 2 языках", access_token)

    assert "choices" in response
    assert isinstance(response["choices"], list)
    assert response["choices"], "choices пуст!"

    first_choice = response["choices"][0]
    message = first_choice.get("message") or {}
    content = message.get("content")

    assert isinstance(content, str)
    assert content.strip(), "Пустой контент из модели!"

    assert response.get("object") == "chat.completion"
    assert isinstance(response.get("created"), int)
    assert isinstance(response.get("model"), str)
