# Посетители (клиенты)

Методы раздела `chat/client`: данные посетителя, блокировка, прикрепление к операторам, посещённые страницы, список и поиск посетителей, Offline-вопросы, счётчик посетителей онлайн.

Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: `{"success": true, "result": ...}`, ошибка: `{"success": false, "error": {"code", "descr"}}` (подробнее — [01-overview.md](01-overview.md)).

| Метод | Назначение |
|---|---|
| `/chat/client/getInfo` | Получение информации о посетителе |
| `/chat/client/setInfo` | Изменение данных посетителя |
| `/chat/client/toggleBan` | Управление блокировкой посетителя |
| `/chat/client/setAttachedOperators` | Прикрепление к операторам |
| `/chat/client/getVisitedPages` | Получение списка посещенных страниц |
| `/chat/client/getList` | Получение списка посетителей за период |
| `/chat/client/search` | Поиск посетителей |
| `/chat/client/markAsHaveNoAnswer` | Пометить как Offline-вопрос |
| `/chat/client/finishHaveNoAnswer` | Завершить Offline-вопрос |
| `/chat/client/onlineCount` | Получить количество посетителей на сайте |

## POST /chat/client/getInfo — Получение информации о посетителе

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1getInfo/post -->

Данный метод позволит получить информацию о посетителе.

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/getInfo`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `client.id` | string |  | Уникальный идентификатор из Cookies<br>**Устарело**<br>Пример: `"ha832rjaafle4"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/getInfo' \
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
  "result": {
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
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatClientGetInfoResult) |
| `result.searchId` | integer | Уникальный идентификатор посетителя для поиска<br>Пример: `1234` |
| `result.login` | string | Уникальный логин посетителя (используется в Jabber)<br>Пример: `"123_user_at_june"` |
| `result.clientId` | string | Идентификатор из Cookie посетителя<br>Пример: `"123e2rwfjas"` |
| `result.name` | string | ФИО или стандартное имя посетителя<br>Пример: `"Ivan"` |
| `result.lastName` | string | Фамилия<br>Пример: `"Иванов"` |
| `result.firstName` | string | Имя<br>Пример: `"Иван"` |
| `result.secondName` | string | Отчество<br>Пример: `"Иванович"` |
| `result.phone` | string | Номер телефона<br>Пример: `"790012345678"` |
| `result.email` | string | Email<br>Пример: `"example@gmail.com"` |
| `result.country` | string | Страна<br>Пример: `"Russia"` |
| `result.city` | string | Город<br>Пример: `"Moscow"` |
| `result.firstVisit` | object | Первый визит |
| `result.firstVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.firstVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.firstVisit.page` | object | Страница |
| `result.firstVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result.firstVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result.lastVisit` | object | Последний визит |
| `result.lastVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.lastVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.lastVisit.lastDateTime` | string | Дата окончания визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.lastVisit.lastDateTimeUTC` | string | Дата окончания визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.lastVisit.page` | object | Страница |
| `result.lastVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result.lastVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result.ip` | string | IP-адрес<br>Пример: `"85.123.22.41"` |
| `result.flag` | string | Флаг<br>Значения: `red`, `orange`, `green`, `blue`, `purple`, `yellow`, `asphalt` |
| `result.useragent` | string | Useragent браузера<br>Пример: `"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54"` |
| `result.target` | array<string> | Целевой посетитель |
| `result.isBanned` | boolean | Пользователь заблокирован |
| `result.questionCategory` | string | Категория вопроса<br>Пример: `"Common questions"` |
| `result.referer` | string | Источник перехода<br>Пример: `"https://google.com"` |
| `result.searchKeyword` | string | Поисковый запрос<br>Пример: `"home flowers"` |
| `result.visitsCount` | integer | Количество визитов<br>Пример: `3` |
| `result.isOnline` | boolean | Посетитель в сети |
| `result.source` | object | Источник диалога |
| `result.source.type` | object | Тип источника |
| `result.source.type.id` | string | Идентификатор<br>Пример: `"vk"` |
| `result.source.type.name` | string | Название<br>Пример: `"VKontakte"` |
| `result.source.id` | string | ID источника диалога<br>Пример: `"ab4-3fddd45-24dss"` |
| `result.source.name` | string | Название источника диалога<br>Пример: `"Название сообщества"` |
| `result.source.link` | string | Ссылка на источник диалога<br>Пример: `"https://vk.com/club0000123"` |
| `result.source.data` | object | Другие данные об источнике |
| `result.customData` | object | Другие данные об посетителе |
| `result.utm` | object | UTM-метки |
| `result.utm.utm_source` | string |  |
| `result.utm.utm_medium` | string |  |
| `result.utm.utm_campaign` | string |  |
| `result.utm.utm_term` | string |  |
| `result.utm.utm_content` | string |  |
| `result.utm.utm_referrer` | string |  |
| `result.tags` | array<string> | Тэги клиента |
| `result.applicationLink` | string | Ссылка на приложение оператора для открытия диалога |
| `result.infoLink` | string | Ссылка на информацию о клиенте |
| `result.roistatVisitId` | string | Значение Cookie roistat_visit<br>Пример: `"1000001"` |
| `result.yandexMetrika` | object | Данные Яндекс.Метрики |
| `result.yandexMetrika.clientId` | string | clientId из Яндекс.Метрики<br>Пример: `"abcdef"` |
| `result.googleAnalytics` | object | Данные Google Analytics |
| `result.googleAnalytics.trackingId` | string | trackingId из Google Analytics<br>Пример: `"abcdef"` |
| `result.googleAnalytics.clientId` | string | clientId из Google Analytics<br>Пример: `"abcdef"` |

## POST /chat/client/setInfo — Изменение данных посетителя

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1setInfo/post -->

Данный метод позволит программно изменять данные посетителя

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/setInfo`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент |
| `client.lastName` | string |  | Фамилия<br>Пример: `"Иванов"` |
| `client.firstName` | string |  | Имя<br>Пример: `"Иван"` |
| `client.secondName` | string |  | Отчество<br>Пример: `"Иванович"` |
| `client.phone` | string |  | Номер телефона<br>Пример: `"+7-900-000-0000"` |
| `client.email` | string |  | email<br>Пример: `"ivan@gmail.com"` |
| `client.customData` | object |  | Другие данные об посетителе |
| `client.tags` | array<string> |  | Тэги |
| `client.questionCategory` | string |  | Категория вопроса<br>Пример: `"Common questions"` |
| `client.flag` | string |  | Флаг<br>Значения: `none`, `red`, `orange`, `green`, `blue`, `purple`, `yellow`, `asphalt` |
| `client.name` | string |  | ФИО посетителя<br>**Устарело**<br>Пример: `"Ivan"` |
| `client.id` | string | условно | Уникальный идентификатор из Cookies<br>minLength: 1<br>maxLength: 32<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer | условно | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `updateMultiContacts` | boolean |  | Обновлять мульти-контакты<br>Если передать `true`, то будет обновлен не только переданный посетитель, но и его мульти-контакты<br>По умолчанию: `false` |

**Пояснения к полям**

`client`:

Нужно передать один из вариантов идентификации — Клиент по clientId: `client.id`; Клиент по searchId: `client.searchId`.


**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/setInfo' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "client": {
    "lastName": "Иванов",
    "firstName": "Иван",
    "secondName": "Иванович",
    "phone": "+7-900-000-0000",
    "email": "ivan@gmail.com",
    "customData": {
      "foo": "bar",
      "key": "value"
    },
    "questionCategory": "Common questions",
    "id": "ha832rjaafle4"
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

## POST /chat/client/toggleBan — Управление блокировкой посетителя

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1toggleBan/post -->

Данный метод позволит заблокировать или разблокировать посетителя

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/toggleBan`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `isBanned` | boolean | да | Посетитель заблокирован?<br>Передайте `true`, чтобы заблокировать или `false` для разблокировки |
| `banDuration` | integer |  | Продолжительность блокировки в секундах<br>min: 1 |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/toggleBan' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "client": {
    "clientId": "ha832rjaafle4",
    "searchId": 12345
  },
  "isBanned": true
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/client/setAttachedOperators — Прикрепление к операторам

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1setAttachedOperators/post -->

Данный метод позволит программно прикрепить посетителя к нужным операторам.
Это сработает только когда в настройках сайта включена опция `Разрешить прикреплять посетителя к оператору навсегда`

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/setAttachedOperators`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `client.id` | string |  | Уникальный идентификатор из Cookies<br>**Устарело**<br>Пример: `"ha832rjaafle4"` |
| `operators` | array<string> | да | Логины операторов<br>Передайте пустой массив, чтобы открепить посетителя от операторов |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/setAttachedOperators' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "client": {
    "clientId": "ha832rjaafle4",
    "searchId": 12345
  },
  "operators": [
    "string"
  ]
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/client/getVisitedPages — Получение списка посещенных страниц

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1getVisitedPages/post -->

Данный метод позволит получить список посещенных посетителем страниц.

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/getVisitedPages`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `client.id` | string |  | Уникальный идентификатор из Cookies<br>**Устарело**<br>Пример: `"ha832rjaafle4"` |
| `page` | integer |  | Номер страницы<br>По умолчанию: `0`<br>min: 0 |
| `limit` | integer |  | Количество записей на страницу<br>По умолчанию: `30`<br>min: 1<br>max: 500 |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/getVisitedPages' \
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
  "result": {
    "count": 65,
    "limit": 30,
    "items": [
      {
        "url": "http://mysite.com",
        "title": "MySite title",
        "dateTimeOpen": "2026-10-01 12:00:00"
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatClientGetVisitedPagesResult) |
| `result.count` | integer | Количество объектов<br>Пример: `65` |
| `result.limit` | integer | Количество на страницу<br>Пример: `30` |
| `result.items` | array<object> | Список объектов |
| `result.items[].url` | string | Адрес страницы<br>Пример: `"http://mysite.com"` |
| `result.items[].title` | string | Название страницы<br>Пример: `"MySite title"` |
| `result.items[].dateTimeOpen` | string | Дата открытия страницы<br>Формат YYYY-MM-DD HH:MM:SS<br>Пример: `"2026-10-01 12:00:00"` |
| `result.items[].dateTimeClose` | string | Дата закрытия страницы<br>Формат YYYY-MM-DD HH:MM:SS<br>Пример: `"2026-10-01 12:00:00"` |

## POST /chat/client/getList — Получение списка посетителей за период

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1getList/post -->

Данный метод позволит получить список посетителей за интересующий вас период.

Обращаем ваше внимание, что если человек не писал в чат, то он будет удален из отчётов спустя неделю с момента последнего захода.

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/getList`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `page` | integer |  | Номер страницы<br>По умолчанию: `0`<br>min: 0 |
| `limit` | integer |  | Количество записей на страницу<br>По умолчанию: `30`<br>min: 1<br>max: 500 |
| `lastActivityDateTimeRange` | object | да | Время последней активности клиента (максимум 7 дней) |
| `lastActivityDateTimeRange.start` | string | да | Начало диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-01 00:00:00"` |
| `lastActivityDateTimeRange.stop` | string | да | Конец диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-07 23:59:59"` |
| `isOnline` | boolean |  | Текущий статус посетителя<br>`true` - online, `false` - offline |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/getList' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "lastActivityDateTimeRange": {
    "start": "2026-10-01 00:00:00",
    "stop": "2026-10-07 23:59:59"
  }
}'
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
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatGetClientListResult) |
| `result.count` | integer | Количество объектов<br>Пример: `65` |
| `result.limit` | integer | Количество на страницу<br>Пример: `30` |
| `result.items` | array<object> | Список объектов |
| `result.items[].searchId` | integer | Уникальный идентификатор посетителя для поиска<br>Пример: `1234` |
| `result.items[].login` | string | Уникальный логин посетителя (используется в Jabber)<br>Пример: `"123_user_at_june"` |
| `result.items[].clientId` | string | Идентификатор из Cookie посетителя<br>Пример: `"123e2rwfjas"` |
| `result.items[].name` | string | ФИО или стандартное имя посетителя<br>Пример: `"Ivan"` |
| `result.items[].lastName` | string | Фамилия<br>Пример: `"Иванов"` |
| `result.items[].firstName` | string | Имя<br>Пример: `"Иван"` |
| `result.items[].secondName` | string | Отчество<br>Пример: `"Иванович"` |
| `result.items[].phone` | string | Номер телефона<br>Пример: `"790012345678"` |
| `result.items[].email` | string | Email<br>Пример: `"example@gmail.com"` |
| `result.items[].country` | string | Страна<br>Пример: `"Russia"` |
| `result.items[].city` | string | Город<br>Пример: `"Moscow"` |
| `result.items[].firstVisit` | object | Первый визит |
| `result.items[].firstVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.items[].firstVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.items[].firstVisit.page` | object | Страница |
| `result.items[].firstVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result.items[].firstVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result.items[].lastVisit` | object | Последний визит |
| `result.items[].lastVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.items[].lastVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.items[].lastVisit.lastDateTime` | string | Дата окончания визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.items[].lastVisit.lastDateTimeUTC` | string | Дата окончания визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.items[].lastVisit.page` | object | Страница |
| `result.items[].lastVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result.items[].lastVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result.items[].ip` | string | IP-адрес<br>Пример: `"85.123.22.41"` |
| `result.items[].flag` | string | Флаг<br>Значения: `red`, `orange`, `green`, `blue`, `purple`, `yellow`, `asphalt` |
| `result.items[].useragent` | string | Useragent браузера<br>Пример: `"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54"` |
| `result.items[].target` | array<string> | Целевой посетитель |
| `result.items[].isBanned` | boolean | Пользователь заблокирован |
| `result.items[].questionCategory` | string | Категория вопроса<br>Пример: `"Common questions"` |
| `result.items[].referer` | string | Источник перехода<br>Пример: `"https://google.com"` |
| `result.items[].searchKeyword` | string | Поисковый запрос<br>Пример: `"home flowers"` |
| `result.items[].visitsCount` | integer | Количество визитов<br>Пример: `3` |
| `result.items[].isOnline` | boolean | Посетитель в сети |
| `result.items[].source` | object | Источник диалога |
| `result.items[].source.type` | object | Тип источника |
| `result.items[].source.type.id` | string | Идентификатор<br>Пример: `"vk"` |
| `result.items[].source.type.name` | string | Название<br>Пример: `"VKontakte"` |
| `result.items[].source.id` | string | ID источника диалога<br>Пример: `"ab4-3fddd45-24dss"` |
| `result.items[].source.name` | string | Название источника диалога<br>Пример: `"Название сообщества"` |
| `result.items[].source.link` | string | Ссылка на источник диалога<br>Пример: `"https://vk.com/club0000123"` |
| `result.items[].source.data` | object | Другие данные об источнике |
| `result.items[].customData` | object | Другие данные об посетителе |
| `result.items[].utm` | object | UTM-метки |
| `result.items[].utm.utm_source` | string |  |
| `result.items[].utm.utm_medium` | string |  |
| `result.items[].utm.utm_campaign` | string |  |
| `result.items[].utm.utm_term` | string |  |
| `result.items[].utm.utm_content` | string |  |
| `result.items[].utm.utm_referrer` | string |  |
| `result.items[].tags` | array<string> | Тэги клиента |
| `result.items[].applicationLink` | string | Ссылка на приложение оператора для открытия диалога |
| `result.items[].infoLink` | string | Ссылка на информацию о клиенте |
| `result.items[].roistatVisitId` | string | Значение Cookie roistat_visit<br>Пример: `"1000001"` |
| `result.items[].yandexMetrika` | object | Данные Яндекс.Метрики |
| `result.items[].yandexMetrika.clientId` | string | clientId из Яндекс.Метрики<br>Пример: `"abcdef"` |
| `result.items[].googleAnalytics` | object | Данные Google Analytics |
| `result.items[].googleAnalytics.trackingId` | string | trackingId из Google Analytics<br>Пример: `"abcdef"` |
| `result.items[].googleAnalytics.clientId` | string | clientId из Google Analytics<br>Пример: `"abcdef"` |

## POST /chat/client/search — Поиск посетителей

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1search/post -->

Данный метод позволит получить список посетителей по телефону или email

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/search`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `phone` | string |  | Номер телефона |
| `email` | string |  | Email |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/search' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "clients": [
      {
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
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatSearchClientListResult) |
| `result.clients` | array<object> | Список клиентов |
| `result.clients[].searchId` | integer | Уникальный идентификатор посетителя для поиска<br>Пример: `1234` |
| `result.clients[].login` | string | Уникальный логин посетителя (используется в Jabber)<br>Пример: `"123_user_at_june"` |
| `result.clients[].clientId` | string | Идентификатор из Cookie посетителя<br>Пример: `"123e2rwfjas"` |
| `result.clients[].name` | string | ФИО или стандартное имя посетителя<br>Пример: `"Ivan"` |
| `result.clients[].lastName` | string | Фамилия<br>Пример: `"Иванов"` |
| `result.clients[].firstName` | string | Имя<br>Пример: `"Иван"` |
| `result.clients[].secondName` | string | Отчество<br>Пример: `"Иванович"` |
| `result.clients[].phone` | string | Номер телефона<br>Пример: `"790012345678"` |
| `result.clients[].email` | string | Email<br>Пример: `"example@gmail.com"` |
| `result.clients[].country` | string | Страна<br>Пример: `"Russia"` |
| `result.clients[].city` | string | Город<br>Пример: `"Moscow"` |
| `result.clients[].firstVisit` | object | Первый визит |
| `result.clients[].firstVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.clients[].firstVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.clients[].firstVisit.page` | object | Страница |
| `result.clients[].firstVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result.clients[].firstVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result.clients[].lastVisit` | object | Последний визит |
| `result.clients[].lastVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.clients[].lastVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.clients[].lastVisit.lastDateTime` | string | Дата окончания визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.clients[].lastVisit.lastDateTimeUTC` | string | Дата окончания визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.clients[].lastVisit.page` | object | Страница |
| `result.clients[].lastVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result.clients[].lastVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result.clients[].ip` | string | IP-адрес<br>Пример: `"85.123.22.41"` |
| `result.clients[].flag` | string | Флаг<br>Значения: `red`, `orange`, `green`, `blue`, `purple`, `yellow`, `asphalt` |
| `result.clients[].useragent` | string | Useragent браузера<br>Пример: `"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54"` |
| `result.clients[].target` | array<string> | Целевой посетитель |
| `result.clients[].isBanned` | boolean | Пользователь заблокирован |
| `result.clients[].questionCategory` | string | Категория вопроса<br>Пример: `"Common questions"` |
| `result.clients[].referer` | string | Источник перехода<br>Пример: `"https://google.com"` |
| `result.clients[].searchKeyword` | string | Поисковый запрос<br>Пример: `"home flowers"` |
| `result.clients[].visitsCount` | integer | Количество визитов<br>Пример: `3` |
| `result.clients[].isOnline` | boolean | Посетитель в сети |
| `result.clients[].source` | object | Источник диалога |
| `result.clients[].source.type` | object | Тип источника |
| `result.clients[].source.type.id` | string | Идентификатор<br>Пример: `"vk"` |
| `result.clients[].source.type.name` | string | Название<br>Пример: `"VKontakte"` |
| `result.clients[].source.id` | string | ID источника диалога<br>Пример: `"ab4-3fddd45-24dss"` |
| `result.clients[].source.name` | string | Название источника диалога<br>Пример: `"Название сообщества"` |
| `result.clients[].source.link` | string | Ссылка на источник диалога<br>Пример: `"https://vk.com/club0000123"` |
| `result.clients[].source.data` | object | Другие данные об источнике |
| `result.clients[].customData` | object | Другие данные об посетителе |
| `result.clients[].utm` | object | UTM-метки |
| `result.clients[].utm.utm_source` | string |  |
| `result.clients[].utm.utm_medium` | string |  |
| `result.clients[].utm.utm_campaign` | string |  |
| `result.clients[].utm.utm_term` | string |  |
| `result.clients[].utm.utm_content` | string |  |
| `result.clients[].utm.utm_referrer` | string |  |
| `result.clients[].tags` | array<string> | Тэги клиента |
| `result.clients[].applicationLink` | string | Ссылка на приложение оператора для открытия диалога |
| `result.clients[].infoLink` | string | Ссылка на информацию о клиенте |
| `result.clients[].roistatVisitId` | string | Значение Cookie roistat_visit<br>Пример: `"1000001"` |
| `result.clients[].yandexMetrika` | object | Данные Яндекс.Метрики |
| `result.clients[].yandexMetrika.clientId` | string | clientId из Яндекс.Метрики<br>Пример: `"abcdef"` |
| `result.clients[].googleAnalytics` | object | Данные Google Analytics |
| `result.clients[].googleAnalytics.trackingId` | string | trackingId из Google Analytics<br>Пример: `"abcdef"` |
| `result.clients[].googleAnalytics.clientId` | string | clientId из Google Analytics<br>Пример: `"abcdef"` |

## POST /chat/client/markAsHaveNoAnswer — Пометить как Offline-вопрос

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1markAsHaveNoAnswer/post -->

Данный метод позволит пометить диалог с клиентом как Offline-вопрос, который будет виден всем операторам.

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/markAsHaveNoAnswer`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `client.id` | string |  | Уникальный идентификатор из Cookies<br>**Устарело**<br>Пример: `"ha832rjaafle4"` |
| `operator` | object | да | Оператор |
| `operator.login` | string | да | Логин оператора<br>Пример: `"my_login"` |
| `operator.virtual` | boolean |  | Виртуальный оператор<br>Если передать `true`, то не будет осуществляться проверка существования переданного логина оператора |
| `operatorGroupIds` | array<string> |  | ID отделов операторов<br>Передайте, если хотите, чтобы Offline-вопрос был виден только указанным отделам |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/markAsHaveNoAnswer' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "client": {
    "clientId": "ha832rjaafle4",
    "searchId": 12345
  },
  "operator": {
    "login": "my_login"
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

## POST /chat/client/finishHaveNoAnswer — Завершить Offline-вопрос

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1finishHaveNoAnswer/post -->

Завершить Offline-вопрос.

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/finishHaveNoAnswer`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `client.id` | string |  | Уникальный идентификатор из Cookies<br>**Устарело**<br>Пример: `"ha832rjaafle4"` |
| `operator` | object | да | Оператор |
| `operator.login` | string | да | Логин оператора<br>Пример: `"my_login"` |
| `operator.virtual` | boolean |  | Виртуальный оператор<br>Если передать `true`, то не будет осуществляться проверка существования переданного логина оператора |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/finishHaveNoAnswer' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "client": {
    "clientId": "ha832rjaafle4",
    "searchId": 12345
  },
  "operator": {
    "login": "my_login"
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

## POST /chat/client/onlineCount — Получить количество посетителей на сайте

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatclient/paths/~1chat~1client~1onlineCount/post -->

Получить количество посетителей на сайте.

`POST https://lcab.talk-me.ru/json/v1.0/chat/client/onlineCount`

**Параметры запроса**

Метод не принимает параметров — передайте пустой JSON-объект `{}`.

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/client/onlineCount' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "onlineCount": 0
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatClientOnlineCountResult) |
| `result.onlineCount` | integer | Количество посетителей на сайте |
