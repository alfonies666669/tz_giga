import allure

from tools.giga_client import chat_completion_raw


@allure.tag("positive")
@allure.title("System-промпт первым в messages")
def test_positive_chat_completions_with_system_prompt(access_token):
    """system первым, должно пройти без ошибок."""
    payload = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": "Ты — лаконичный бот, отвечай одним словом.",
            },
            {
                "role": "user",
                "content": "Как дела?",
            },
        ],
        "stream": False,
    }

    resp = chat_completion_raw(payload, access_token)
    assert resp.status_code == 200

    body = resp.json()
    assert "choices" in body and body["choices"]

    msg = body["choices"][0].get("message") or {}
    content = msg.get("content", "")

    assert isinstance(content, str)
    assert content.strip(), "Пустой ответ при system-промпте"


@allure.tag("positive")
@allure.title("max_tokens ограничивает длину ответа")
def test_positive_chat_completions_respects_max_tokens(access_token):
    """Проверяем, что max_tokens ограничивает длину ответа."""
    max_tokens = 10
    payload = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": "Расскажи о себе как можно подробнее.",
            }
        ],
        "max_tokens": max_tokens,
        "stream": False,
    }

    resp = chat_completion_raw(payload, access_token)
    assert resp.status_code == 200

    body = resp.json()
    usage = body.get("usage") or {}
    completion_tokens = usage.get("completion_tokens")

    assert completion_tokens is not None, "Нет completion_tokens в usage"
    assert (
        completion_tokens <= max_tokens
    ), f"completion_tokens={completion_tokens} > max_tokens={max_tokens}"


@allure.tag("negative")
@allure.title("Неверная model -> 404")
def test_negative_chat_completions_invalid_model_returns_404(access_token):
    """Ломаем модель, ждём 404 и понятное сообщение."""
    payload = {
        "model": "Totally-Non-Existing-Model-XYZ",
        "messages": [
            {
                "role": "user",
                "content": "Тест запроса с неверной моделью",
            }
        ],
        "stream": False,
    }

    resp = chat_completion_raw(payload, access_token)

    assert resp.status_code == 404
    body = resp.json()
    assert body.get("status") == 404
    assert "model" in body.get("message", "").lower()


@allure.tag("negative")
@allure.title("system не первым -> 422")
def test_negative_chat_completions_system_prompt_not_first_returns_422(access_token):
    """system не первым, ждём 422 и текст про system message first."""
    payload = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": "Сначала пользователь.",
            },
            {
                "role": "system",
                "content": "А потом системный промпт, что нельзя.",
            },
        ],
        "stream": False,
    }

    resp = chat_completion_raw(payload, access_token)

    assert resp.status_code == 422
    body = resp.json()
    assert body.get("status") == 422

    msg = body.get("message", "")
    assert "system message must be the first message" in msg
