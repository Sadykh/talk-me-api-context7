# Боты

Методы раздела `chat/bot`: запуск и остановка сценария чат-бота для посетителя.

Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: `{"success": true, "result": ...}`, ошибка: `{"success": false, "error": {"code", "descr"}}` (подробнее — [01-overview.md](01-overview.md)).

| Метод | Назначение |
|---|---|
| `/chat/bot/startBot` | Запустить бота |
| `/chat/bot/stopBot` | Остановить бота |

## POST /chat/bot/startBot — Запустить бота

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatbot/paths/~1chat~1bot~1startBot/post -->

Данный метод позволит запустить бота для клиента

`POST https://lcab.talk-me.ru/json/v1.0/chat/bot/startBot`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `client.id` | string |  | Уникальный идентификатор из Cookies<br>**Устарело**<br>Пример: `"ha832rjaafle4"` |
| `botSchemeId` | string | да | id сценария бота |
| `operatorLogin` | string |  | Логин оператора, от имени которого запускается бот |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/bot/startBot' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "client": {
    "clientId": "ha832rjaafle4",
    "searchId": 12345
  },
  "botSchemeId": "string"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/bot/stopBot — Остановить бота

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatbot/paths/~1chat~1bot~1stopBot/post -->

Данный метод позволит остановить запущенного в данный момент бота

`POST https://lcab.talk-me.ru/json/v1.0/chat/bot/stopBot`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `client.id` | string |  | Уникальный идентификатор из Cookies<br>**Устарело**<br>Пример: `"ha832rjaafle4"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/bot/stopBot' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "client": {
    "clientId": "ha832rjaafle4",
    "searchId": 12345
  }
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```
