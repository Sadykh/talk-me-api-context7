# Лицензии

Методы раздела `chat/license`: покупка лицензии для сайта и список действующих лицензий.

Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: `{"success": true, "result": ...}`, ошибка: `{"success": false, "error": {"code", "descr"}}` (подробнее — [01-overview.md](01-overview.md)).

| Метод | Назначение |
|---|---|
| `/chat/license/create` | Создание лицензии |
| `/chat/license/get` | Список лицензий |

## POST /chat/license/create — Создание лицензии

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatlicense/paths/~1chat~1license~1create/post -->

С помощью данного метода вы можете создать новую лицензию для сайта

`POST https://lcab.talk-me.ru/json/v1.0/chat/license/create`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `typeId` | string | да | Тип лицензии<br>`period` - За период<br>`pack` - За обращения<br>Пример: `"period"` |
| `batchId` | integer | да | Идентификатор пакета<br>Расшифровка значений: [Пакеты лицензий (batchId)](12-dictionaries.md#пакеты-лицензий-batchid)<br>Пример: `31` |
| `operatorCount` | integer | да | Количество операторов<br>Пример: `3` |
| `validate` | boolean |  | Проверка возможности создания лицензии<br>Если передать true, то лицензия не будет создана, и деньги не будут списаны.<br>По умолчанию: `false` |
| `prolongAuto` | boolean |  | Автоматическое продление<br>По умолчанию: `true`<br>Пример: `true` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/license/create' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "typeId": "period",
  "batchId": 31,
  "operatorCount": 3,
  "prolongAuto": true
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "id": "string"
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatCreateLicenseResult) |
| `result.id` | string | Уникальный идентификатор |

## POST /chat/license/get — Список лицензий

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatlicense/paths/~1chat~1license~1get/post -->

С помощью данного метода вы можете получить действующую и будущие лицензии для сайта

`POST https://lcab.talk-me.ru/json/v1.0/chat/license/get`

**Параметры запроса**

Метод не принимает параметров — передайте пустой JSON-объект `{}`.

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/license/get' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "licenseList": [
      {
        "id": "string",
        "typeId": "period",
        "batchId": 31,
        "operatorCount": 3,
        "prolongAuto": true,
        "price": {
          "sum": 500.3,
          "currencyId": "rub"
        }
      }
    ],
    "isTestPeriodAvailable": true
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatGetLicenseResult) |
| `result.licenseList` | array<object> | Лицензии |
| `result.licenseList[].id` | string | Уникальный идентификатор лицензии |
| `result.licenseList[].typeId` | string | Тип лицензии<br>`period` - За период<br>`pack` - За обращения<br>Пример: `"period"` |
| `result.licenseList[].batchId` | integer | Идентификатор пакета<br>Расшифровка значений: [Пакеты лицензий (batchId)](12-dictionaries.md#пакеты-лицензий-batchid)<br>Пример: `31` |
| `result.licenseList[].operatorCount` | integer | Количество операторов<br>Пример: `3` |
| `result.licenseList[].dateTimeStart` | string | Дата начала действия лицензии<br>Формат YYYY-MM-DD HH:MM:SS<br>Пример: `"2026-10-01 12:00:00"` |
| `result.licenseList[].dateTimeStop` | string | Дата окончания действия лицензии<br>Формат YYYY-MM-DD HH:MM:SS<br>Пример: `"2026-10-01 12:00:00"` |
| `result.licenseList[].prolongAuto` | boolean | Автоматическое продление<br>По умолчанию: `true`<br>Пример: `true` |
| `result.licenseList[].price` | object | Стоимость лицензии |
| `result.licenseList[].price.sum` | number | Сумма<br>Пример: `500.3` |
| `result.licenseList[].price.currencyId` | string | Валюта<br>Значения: `rub`, `eur`, `usd`, `uah`, `byn`, `kzt`<br>По умолчанию: `"rub"` |
| `result.isTestPeriodAvailable` | boolean | Доступна ли тестовая лицензия для этого сайта<br>`true` в тот момент, когда вы добавляете первый сайт, и тестовая лицензия ещё не была активирована |
