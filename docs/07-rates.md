# Отзывы

Методы раздела `chat/rates`: список отзывов (оценок) посетителей и агрегированный отчёт.

Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: `{"success": true, "result": ...}`, ошибка: `{"success": false, "error": {"code", "descr"}}` (подробнее — [01-overview.md](01-overview.md)).

| Метод | Назначение |
|---|---|
| `/chat/rates/getList` | Получение списка отзывов |
| `/chat/rates/getSummary` | Агрегированный отчёт |

## POST /chat/rates/getList — Получение списка отзывов

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatrates/paths/~1chat~1rates~1getList/post -->

Данный метод позволит получить список отзывов за интересующий вас период.

`POST https://lcab.talk-me.ru/json/v1.0/chat/rates/getList`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `dateRange` | object |  | Период |
| `dateRange.start` | string | да | Начало диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-01 00:00:00"` |
| `dateRange.stop` | string | да | Конец диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-07 23:59:59"` |
| `isApproved` | boolean |  | Отзыв одобрен?<br>Передайте `true`, чтобы получить только одобренные отзывы, `false` - не одобренные, `null` - все |
| `withDialogs` | boolean |  | Получать диалог, в котором оставлен отзыв? |
| `page` | integer |  | Номер страницы<br>По умолчанию: `0`<br>min: 0 |
| `limit` | integer |  | Количество записей на страницу<br>По умолчанию: `30`<br>min: 1<br>max: 500 |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/rates/getList' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "count": 65,
    "limit": 30,
    "items": [
      {
        "id": 0,
        "client": {
          "searchId": 1234,
          "login": "123_user_at_june",
          "clientId": "123e2rwfjas",
          "name": "Ivan",
          "isBanned": true,
          "isOnline": true,
          "source": {
            "type": {
              "id": "vk",
              "name": "VKontakte"
            },
            "id": "ab4-3fddd45-24dss",
            "name": "Название сообщества",
            "link": "https://vk.com/club0000123",
            "data": {
              "id": "21312312"
            }
          },
          "tags": [
            "string"
          ],
          "applicationLink": "string",
          "infoLink": "string"
        },
        "rate": "good",
        "dateTime": "2026-10-01 12:00:00",
        "isRead": true,
        "isApproved": true,
        "attachments": [
          {
            "url": "https://server.com/download?id=123",
            "fileSize": 123,
            "fileName": "example.jpg",
            "type": {
              "id": "file",
              "descr": "string",
              "icon": "string"
            }
          }
        ]
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatGetRateListResult) |
| `result.count` | integer | Количество объектов<br>Пример: `65` |
| `result.limit` | integer | Количество на страницу<br>Пример: `30` |
| `result.items` | array<object> | Список объектов |
| `result.items[].id` | integer | Уникальный идентификатор отзыва |
| `result.items[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.items[].operator` | object | Оператор<br>Структура: [Оператор (ChatGetOperatorsListOperator)](11-models.md#оператор-chatgetoperatorslistoperator) |
| `result.items[].virtualOperator` | string | Логин виртуального оператора |
| `result.items[].rate` | string | Оценка<br>Значения: `good`, `bad`, `1/5`, `2/5`, `3/5`, `4/5`, `5/5` |
| `result.items[].text` | string | Текст отзыва |
| `result.items[].dateTime` | string | Дата/время отправки отзыва<br>Формат YYYY-MM-DD HH:MM:SS<br>Пример: `"2026-10-01 12:00:00"` |
| `result.items[].isRead` | boolean | Отзыв прочтен администраторами? |
| `result.items[].isApproved` | boolean | Отзыв одобрен? |
| `result.items[].adminComment` | string | Комментарий администрации |
| `result.items[].attachments` | array<object> | Файлы-вложения<br>Структура: [Вложение (OnlineMessageAttachment)](11-models.md#вложение-onlinemessageattachment) |
| `result.items[].dialogId` | integer | id диалога |

## POST /chat/rates/getSummary — Агрегированный отчёт

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatrates/paths/~1chat~1rates~1getSummary/post -->

Данный метод позволит получить количество отзывов и среднюю оценку

`POST https://lcab.talk-me.ru/json/v1.0/chat/rates/getSummary`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `dateRange` | object |  | Период |
| `dateRange.start` | string | да | Начало диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-01 00:00:00"` |
| `dateRange.stop` | string | да | Конец диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-07 23:59:59"` |
| `isApproved` | boolean |  | Отзыв одобрен?<br>Передайте `true`, чтобы получить только одобренные отзывы, `false` - не одобренные, `null` - все |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/rates/getSummary' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "total": {
      "counts": {
        "all": 0,
        "good": 0,
        "bad": 0
      }
    },
    "byOperator": [
      {
        "login": "my_login",
        "result": {
          "counts": {
            "all": 0,
            "good": 0,
            "bad": 0
          }
        }
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatReviewsGetSummaryResult) |
| `result.total` | object | Элемент отчёта по отзывам |
| `result.total.average` | integer | Средняя оценка в процентах<br>min: 0<br>max: 100 |
| `result.total.counts` | object | Количество отзывов |
| `result.total.counts.all` | integer | Всего отзывов |
| `result.total.counts.good` | integer | Хорошие отзывы |
| `result.total.counts.bad` | integer | Плохие отзывы |
| `result.byOperator` | array<object> | Результаты, разбитые по операторам |
| `result.byOperator[].login` | string | Логин оператора |
| `result.byOperator[].result` | object | Элемент отчёта по отзывам |
| `result.byOperator[].result.average` | integer | Средняя оценка в процентах<br>min: 0<br>max: 100 |
| `result.byOperator[].result.counts` | object | Количество отзывов |
| `result.byOperator[].result.counts.all` | integer | Всего отзывов |
| `result.byOperator[].result.counts.good` | integer | Хорошие отзывы |
| `result.byOperator[].result.counts.bad` | integer | Плохие отзывы |
