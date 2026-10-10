# Операторы

Методы раздела `chat/operator`: список операторов, авторизация и сессии, статусы, создание, редактирование, удаление и включение операторов, управление отделами.

Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: `{"success": true, "result": ...}`, ошибка: `{"success": false, "error": {"code", "descr"}}` (подробнее — [01-overview.md](01-overview.md)).

| Метод | Назначение |
|---|---|
| `/chat/operator/getList` | Получение списка операторов |
| `/chat/operator/login` | Авторизация оператора |
| `/chat/operator/setStatus` | Изменение статуса оператора |
| `/chat/operator/setCustomStatus` | Изменение своего (кастомного) статуса оператора |
| `/chat/operator/logout` | Разрыв сессии оператора |
| `/chat/operator/create` | Создание оператора |
| `/chat/operator/edit` | Редактирование оператора |
| `/chat/operator/delete` | Удаление оператора |
| `/chat/operator/toggle` | Включение\отключение оператора |
| `/chat/operator/addToGroup` | Добавление оператора в отдел |
| `/chat/operator/deleteFromGroup` | Удаление оператора из отдела |

## POST /chat/operator/getList — Получение списка операторов

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1getList/post -->

Данный метод позволит получить список операторов на вашем сайте.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/getList`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `includeDisabledOperators` | boolean |  | Включить в ответ отключенных на этом сайте операторов<br>По умолчанию: `false`<br>Пример: `true` |
| `getPseudonyms` | boolean |  | Возвращать псевдонимы в качестве имени (если указаны)<br>По умолчанию: `true`<br>Пример: `true` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/getList' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "includeDisabledOperators": true,
  "getPseudonyms": true
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "operators": [
      {
        "id": "12fwaihos",
        "login": "my_operator",
        "name": "Ivan",
        "realName": "Ivan",
        "statusId": 0,
        "isUnavailableBecauseOfLimits": true,
        "isWorkingNow": true,
        "isVisibleForClients": true,
        "integrations": [
          {
            "platformId": "telegram",
            "authPrimaryId": "de03131dcab80bafe15f07352a6697d0"
          }
        ],
        "groups": [
          "string"
        ]
      }
    ],
    "status": [
      {
        "id": 1,
        "name": "В сети"
      },
      {
        "id": -1,
        "name": "Невидимый"
      },
      {
        "id": 0,
        "name": "Отошёл"
      }
    ],
    "customStatus": [
      {
        "id": 1,
        "name": "В сети"
      },
      {
        "id": -1,
        "name": "Невидимый"
      },
      {
        "id": 0,
        "name": "Отошёл"
      }
    ],
    "groups": [
      {
        "id": "123wawh46we3",
        "descr": "Tech support",
        "operators": [
          "my_login"
        ]
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatGetOperatorsListResult) |
| `result.operators` | array<object> | Операторы<br>Структура: [Оператор (ChatGetOperatorsListOperator)](11-models.md#оператор-chatgetoperatorslistoperator) |
| `result.status` | array<object> | Список возможных статусов |
| `result.status[].id` | integer | Идентификатор |
| `result.status[].name` | string | Описание |
| `result.customStatus` | array<object> | Список возможных своих (кастомных) статусов |
| `result.customStatus[].id` | string | Идентификатор |
| `result.customStatus[].name` | string | Описание |
| `result.groups` | array<object> | Список отделов операторов |
| `result.groups[].id` | string | Идентификатор<br>Пример: `"123wawh46we3"` |
| `result.groups[].descr` | string | Название<br>Пример: `"Tech support"` |
| `result.groups[].operators` | array<string> | Список логинов операторов |

## POST /chat/operator/login — Авторизация оператора

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1login/post -->

С помощью данного метода можно авторизовать оператора на сервере. При этом будет создана активная сессия, которая будет завершена только при вызове метода `chat/operator/logout`

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/login`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `operatorLogin` | string | да | Логин оператора<br>Пример: `"my_operator"` |
| `descr` | string |  | Описание авторизации<br>Пример: `"Auth from my server"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/login' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "operatorLogin": "my_operator",
  "descr": "Auth from my server"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "sessionId": "da39a3ee5e6b4b0d3255bfef95601890afd80709"
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatOperatorLoginResult) |
| `result.sessionId` | string | Уникальный идентификатор сессии<br>Пример: `"da39a3ee5e6b4b0d3255bfef95601890afd80709"` |

## POST /chat/operator/setStatus — Изменение статуса оператора

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1setStatus/post -->

Изменение статуса оператора.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/setStatus`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `operatorLogin` | string | да | Логин<br>Пример: `"my_operator"` |
| `status` | integer | да | Статус<br>`1` - В сети<br>`-1` - Невидимый<br>`0` - Отошёл |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/setStatus' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "operatorLogin": "my_operator",
  "status": 0
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/operator/setCustomStatus — Изменение своего (кастомного) статуса оператора

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1setCustomStatus/post -->

Изменение своего (кастомного) статуса оператора.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/setCustomStatus`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `operatorLogin` | string | да | Логин<br>Пример: `"my_operator"` |
| `status` | string | да | id кастомного статуса |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/setCustomStatus' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "operatorLogin": "my_operator",
  "status": "string"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/operator/logout — Разрыв сессии оператора

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1logout/post -->

С помощью данного метода можно разорвать одну или все сессии оператора на сервере.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/logout`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `operatorLogin` | string | да | Логин оператора<br>Пример: `"my_operator"` |
| `sessionId` | string |  | Уникальный идентификатор сессии<br>Если не передать, будут разорваны все сессии<br>Пример: `"da39a3ee5e6b4b0d3255bfef95601890afd80709"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/logout' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "operatorLogin": "my_operator",
  "sessionId": "da39a3ee5e6b4b0d3255bfef95601890afd80709"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/operator/create — Создание оператора

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1create/post -->

Создание оператора.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/create`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `login` | string | да | Логин<br>Шаблон: `^[\da-z_\-]+$`<br>Пример: `"my_operator"` |
| `password` | string | да | Пароль<br>Пример: `"foobar"` |
| `name` | string | да | Имя<br>Пример: `"Ivan"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/create' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "my_operator",
  "password": "foobar",
  "name": "Ivan"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "id": "b80bb7740288fda1f201890375a60c8f"
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatOperatorCreateResult) |
| `result.id` | string | Уникальный идентификатор оператора<br>Пример: `"b80bb7740288fda1f201890375a60c8f"` |

## POST /chat/operator/edit — Редактирование оператора

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1edit/post -->

Редактирование оператора.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/edit`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `id` | string | да | Уникальный идентификатор оператора<br>Пример: `"b80bb7740288fda1f201890375a60c8f"` |
| `password` | string |  | Пароль<br>Пример: `"foobar"` |
| `name` | string |  | Имя<br>Пример: `"Ivan"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/edit' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "b80bb7740288fda1f201890375a60c8f",
  "password": "foobar",
  "name": "Ivan"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/operator/delete — Удаление оператора

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1delete/post -->

Удаление оператора.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/delete`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `id` | string | да | Уникальный идентификатор оператора<br>Пример: `"b80bb7740288fda1f201890375a60c8f"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/delete' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "b80bb7740288fda1f201890375a60c8f"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/operator/toggle — Включение\отключение оператора

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1toggle/post -->

Включение\отключение оператора.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/toggle`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `id` | string | да | Уникальный идентификатор оператора<br>Пример: `"b80bb7740288fda1f201890375a60c8f"` |
| `enabled` | boolean | да | Состояние оператора<br>`true` - оператор включен на сайте<br>`false` - оператор отключен |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/toggle' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "b80bb7740288fda1f201890375a60c8f",
  "enabled": true
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/operator/addToGroup — Добавление оператора в отдел

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1addToGroup/post -->

Добавление оператора в отдел.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/addToGroup`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `operatorId` | string | да | Уникальный идентификатор оператора<br>Пример: `"9461b85cd6e98dd8d070bbb7d9a3ad51"` |
| `groupId` | string | да | Уникальный идентификатор отдела<br>Пример: `"47db2588331bbe530c80dd001fc60aed"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/addToGroup' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "operatorId": "9461b85cd6e98dd8d070bbb7d9a3ad51",
  "groupId": "47db2588331bbe530c80dd001fc60aed"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/operator/deleteFromGroup — Удаление оператора из отдела

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatoperator/paths/~1chat~1operator~1deleteFromGroup/post -->

Удаление оператора из отдела.

`POST https://lcab.talk-me.ru/json/v1.0/chat/operator/deleteFromGroup`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `operatorId` | string | да | Уникальный идентификатор оператора<br>Пример: `"9461b85cd6e98dd8d070bbb7d9a3ad51"` |
| `groupId` | string | да | Уникальный идентификатор отдела<br>Пример: `"47db2588331bbe530c80dd001fc60aed"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/deleteFromGroup' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "operatorId": "9461b85cd6e98dd8d070bbb7d9a3ad51",
  "groupId": "47db2588331bbe530c80dd001fc60aed"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```
