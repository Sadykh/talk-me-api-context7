# Talk-Me Online Chat REST API — документация для Context7

Документация REST API онлайн-чата Talk-Me (`json/v1.0`) в формате Markdown, подготовленная для индексации в [Context7](https://context7.com).

Источники (снимок от 2026-10-10):

- https://lcab.talk-me.ru/cabinet/json-doc/online — документация (ReDoc);
- https://lcab.talk-me.ru/cabinet/json-doc/cabinetRestApi/v1.0/online/specification.json — OpenAPI 3.0.1.

Права на исходную документацию принадлежат её правообладателю.

## Содержимое

| Файл | Раздел |
|---|---|
| [docs/01-overview.md](docs/01-overview.md) | Общая информация: URL, авторизация `X-Token`, формат ответа, ошибки, соглашения, примеры на curl/PHP/Python/JS, типовые сценарии |
| [docs/02-messages.md](docs/02-messages.md) | Сообщения и диалоги (22 метода) |
| [docs/03-operators.md](docs/03-operators.md) | Операторы (11 методов) |
| [docs/04-clients.md](docs/04-clients.md) | Посетители (10 методов) |
| [docs/05-bots.md](docs/05-bots.md) | Боты |
| [docs/06-reports.md](docs/06-reports.md) | Отчёты |
| [docs/07-rates.md](docs/07-rates.md) | Отзывы |
| [docs/08-webhooks.md](docs/08-webhooks.md) | Webhooks |
| [docs/09-licenses.md](docs/09-licenses.md) | Лицензии |
| [docs/10-knowledge-base.md](docs/10-knowledge-base.md) | База знаний |
| [docs/11-models.md](docs/11-models.md) | Общие модели ответов |
| [docs/12-dictionaries.md](docs/12-dictionaries.md) | Справочники значений |

Каждый метод описан по одной схеме: заголовок `POST /path — назначение`, описание, таблица параметров запроса, пример `curl`, пример ответа и таблица полей ответа.

## Postman-коллекция

[postman/talk-me-online-chat.postman_collection.json](postman/talk-me-online-chat.postman_collection.json) — все 62 метода в 9 папках по разделам API (формат Postman Collection v2.1).

1. В Postman: **File → Import** и выберите файл коллекции.
2. Откройте коллекцию → вкладка **Variables** и задайте `token` — API-токен онлайн-чата из личного кабинета. Переменная `baseUrl` уже равна `https://lcab.talk-me.ru/json/v1.0`.
3. Заголовок `X-Token` подставляется автоматически (авторизация API Key на уровне коллекции).

В телах запросов только обязательные поля; необязательные описаны в документации запроса (панель справа). У каждого запроса сохранены примеры ответов, а тест коллекции проверяет HTTP 200 и `success == true`. Для `chat/license/create` в тело добавлено `"validate": true`: лицензия не создаётся и деньги не списываются. Уберите этот флаг, чтобы купить лицензию на самом деле.

Значения вроде `ha832rjaafle4`, `my_login`, `kb_id` — примеры; замените их реальными идентификаторами из своего аккаунта.

## Обновление

`docs/01-overview.md` написан вручную. Остальные файлы документации и Postman-коллекция генерируются из спецификации:

```bash
curl -sSL -o /tmp/talkme-online.json https://lcab.talk-me.ru/cabinet/json-doc/cabinetRestApi/v1.0/online/specification.json
```

```bash
python3 scripts/build_docs.py /tmp/talkme-online.json
```

```bash
python3 scripts/build_postman.py /tmp/talkme-online.json
```

## Отличия от оригинала

- Вложенные схемы развёрнуты в плоские таблицы с путями полей (`message.buttons[].actions[].type`).
- Примеры запросов содержат обязательные поля и поля, для которых в спецификации есть пример; пустые строковые заглушки заменены правдоподобными значениями (`my_login`, `79001234567`).
- Примеры ответов в методах показывают только обязательные поля; полные структуры крупных объектов — в `11-models.md`.
- Повторяющиеся длинные списки значений (каналы, типы сообщений) вынесены в `12-dictionaries.md`.
- Regex-шаблоны дат длиннее 60 символов опущены — формат указан текстом.
- Для устаревших методов указан актуальный аналог (по совпадению назначения и схемы запроса).
