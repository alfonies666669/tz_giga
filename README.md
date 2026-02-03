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

## CI + Allure (GitHub Actions)

- В Actions использован workflow `.github/workflows/tests-allure.yml`.
- Секрет с ключом GigaChat: `Settings → Secrets → Actions → GIGACHAT_AUTH_KEY`.

Запуск:

1. Зайти на вкладку **Actions** в репозитории.
2. Выбрать workflow `tests-and-allure`.
3. Нажать **Run workflow**.
4. После окончания прогонки в разделе **Deployments → github-pages** будет ссылка на Allure-отчёт.