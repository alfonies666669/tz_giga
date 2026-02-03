# GigaChat API tests (chat/completions)

### Настройка

1. Скопировать `.env.example` в `.env` и подставить свой ключ:

```bash
cp .env.example .env
# отредактировать .env:
# GIGACHAT_AUTH_KEY=... (Basic <base64(ClientID:ClientSecret)>)
# GIGACHAT_SCOPE=GIGACHAT_API_PERS
```

2. Установить зависимости:

```bash
pip install requirements.txt
```

3. Запуск тестов:

```bash
pytest
```