# Сообщения и диалоги

Методы раздела `chat/message`: чтение истории, отправка сообщений клиенту и оператору, начало чата в мессенджерах, редактирование и удаление сообщений, статусы, реакции, перевод посетителя на другого оператора и завершение диалога.

Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: `{"success": true, "result": ...}`, ошибка: `{"success": false, "error": {"code", "descr"}}` (подробнее — [01-overview.md](01-overview.md)).

| Метод | Назначение |
|---|---|
| `/chat/message/getList` | Получение списка сообщений за период |
| `/chat/message/getUnreadedMessageCount` | Получение количества непрочитанных сообщений |
| `/chat/message/getClientMessageList` | Список сообщений по одному клиенту |
| `/chat/message/getDialog` | Получение диалога по ID |
| `/chat/message/getClientDialogs` | Получение диалогов клиента |
| `/chat/message/updateDialog` | Обновление диалога |
| `/chat/message/sendToOperator` | Отправка сообщения оператору |
| `/chat/message/sendToClient` | Отправка сообщения клиенту |
| `/chat/message/startChat` | Начать чат |
| `/chat/message/getStartChatChannels` | Получение доступных каналов для "Начать чат" |
| `/chat/message/setSuggestedAnswerToClient` | Предложить ответ оператору |
| `/chat/message/sendTypingToClient` | Имитация набора сообщения |
| `/chat/message/editMessage` | Редактирование сообщения |
| `/chat/message/deleteMessage` | Удаление сообщения |
| `/chat/message/editMessageSentToClient` | Редактирование сообщения, отправленного клиенту (устарел) |
| `/chat/message/deleteMessageToClientMethod` | Удаление сообщения, отправленного клиенту (устарел) |
| `/chat/message/deleteDialogsWithClient` | Удаление всей переписки с клиентом |
| `/chat/message/setStatus` | Изменение статуса сообщения |
| `/chat/message/setReaction` | Изменение реакции на сообщение |
| `/chat/message/forward` | Перенаправление посетителя |
| `/chat/message/closeDialog` | Завершение диалога |
| `/chat/message/getDialogStatusList` | Список статусов диалога |

## POST /chat/message/getList — Получение списка сообщений за период

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1getList/post -->

Данный метод позволит получить список чатов за интересующий вас период.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/getList`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `dateRange` | object | да | Период (максимум 14 дней) |
| `dateRange.start` | string | да | Начало диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-01 00:00:00"` |
| `dateRange.stop` | string | да | Конец диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-07 23:59:59"` |
| `dateRange.isLocal` | boolean |  | Время передается в часовом поясе проекта?<br>По умолчанию время считается переданным в московском часовом поясе<br>По умолчанию: `false` |
| `client` | object |  | Посетитель |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `client.clientId` | string |  | Идентификатор из Cookie посетителя<br>Пример: `"qwd182ugiva"` |
| `client.sourceIds` | array<string> |  | Идентификаторы каналов<br>Расшифровка значений: [Идентификаторы каналов](12-dictionaries.md#идентификаторы-каналов) |
| `operator` | object |  | Оператор |
| `operator.login` | string | да | Логин оператора<br>Пример: `"some_login"` |
| `dialogClosed` | boolean |  | Диалог завершён |
| `haveNoAnswer` | boolean |  | Вопрос помечен необработанным |
| `sender` | string |  | Отправитель сообщения<br>`client` - клиент<br>`operator` - оператор<br>Значения: `operator`, `client` |
| `status` | string |  | Статус<br>`undelivered` - не доставлено<br>`unreaded` - не прочитано<br>Значения: `undelivered`, `unreaded` |
| `skipEmailText` | boolean |  | Пропускать текст Email-писем<br>По умолчанию: `false` |
| `messageTags` | array<string> |  | Список тэгов сообщения |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/getList' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "dateRange": {
    "start": "2026-10-01 00:00:00",
    "stop": "2026-10-07 23:59:59"
  }
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": [
    {
      "messages": [
        {
          "operator": "my_operator",
          "operatorName": "Алексей",
          "whoSend": "operator",
          "text": "Hello, world",
          "content": {
            "text": "Здравствуйте! Чем можем помочь?",
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
            ],
            "buttons": [
              {
                "text": "Здравствуйте! Чем можем помочь?"
              }
            ],
            "sticker": {
              "fileName": "string",
              "isStaticImage": true,
              "isTgs": true,
              "url": "https://example.com"
            },
            "knowledgeBaseArticles": [
              {
                "registerId": "string",
                "descr": "string"
              }
            ]
          },
          "dateTime": "2026-10-01 12:00:00",
          "dateTimeOrganization": "2026-10-01 12:00:00",
          "dateTimeUTC": "2026-10-01 12:00:00",
          "isVisibleForClient": true,
          "tags": [
            "string"
          ]
        }
      ],
      "operators": [
        {
          "login": "my_login",
          "name": "Ivan"
        }
      ],
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
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | array<object> | Список клиентов |
| `result[].messages` | array<object> | Массив сообщений<br>Структура: [Сообщение (ChatMessage)](11-models.md#сообщение-chatmessage) |
| `result[].operators` | array<object> | Список операторов, общавшихся с посетителем |
| `result[].operators[].login` | string | Логин оператора<br>Пример: `"my_login"` |
| `result[].operators[].name` | string | Имя оператора<br>Пример: `"Ivan"` |
| `result[].operators[].avatar` | string | Ссылка на аватар<br>Пример: `"http://static.ru/avatar.jpg"` |
| `result[].searchId` | integer | Уникальный идентификатор посетителя для поиска<br>Пример: `1234` |
| `result[].login` | string | Уникальный логин посетителя (используется в Jabber)<br>Пример: `"123_user_at_june"` |
| `result[].clientId` | string | Идентификатор из Cookie посетителя<br>Пример: `"123e2rwfjas"` |
| `result[].name` | string | ФИО или стандартное имя посетителя<br>Пример: `"Ivan"` |
| `result[].lastName` | string | Фамилия<br>Пример: `"Иванов"` |
| `result[].firstName` | string | Имя<br>Пример: `"Иван"` |
| `result[].secondName` | string | Отчество<br>Пример: `"Иванович"` |
| `result[].phone` | string | Номер телефона<br>Пример: `"790012345678"` |
| `result[].email` | string | Email<br>Пример: `"example@gmail.com"` |
| `result[].country` | string | Страна<br>Пример: `"Russia"` |
| `result[].city` | string | Город<br>Пример: `"Moscow"` |
| `result[].firstVisit` | object | Первый визит |
| `result[].firstVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result[].firstVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result[].firstVisit.page` | object | Страница |
| `result[].firstVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result[].firstVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result[].lastVisit` | object | Последний визит |
| `result[].lastVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result[].lastVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result[].lastVisit.lastDateTime` | string | Дата окончания визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result[].lastVisit.lastDateTimeUTC` | string | Дата окончания визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result[].lastVisit.page` | object | Страница |
| `result[].lastVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result[].lastVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result[].ip` | string | IP-адрес<br>Пример: `"85.123.22.41"` |
| `result[].flag` | string | Флаг<br>Значения: `red`, `orange`, `green`, `blue`, `purple`, `yellow`, `asphalt` |
| `result[].useragent` | string | Useragent браузера<br>Пример: `"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54"` |
| `result[].target` | array<string> | Целевой посетитель |
| `result[].isBanned` | boolean | Пользователь заблокирован |
| `result[].questionCategory` | string | Категория вопроса<br>Пример: `"Common questions"` |
| `result[].referer` | string | Источник перехода<br>Пример: `"https://google.com"` |
| `result[].searchKeyword` | string | Поисковый запрос<br>Пример: `"home flowers"` |
| `result[].visitsCount` | integer | Количество визитов<br>Пример: `3` |
| `result[].isOnline` | boolean | Посетитель в сети |
| `result[].source` | object | Источник диалога |
| `result[].source.type` | object | Тип источника |
| `result[].source.type.id` | string | Идентификатор<br>Пример: `"vk"` |
| `result[].source.type.name` | string | Название<br>Пример: `"VKontakte"` |
| `result[].source.id` | string | ID источника диалога<br>Пример: `"ab4-3fddd45-24dss"` |
| `result[].source.name` | string | Название источника диалога<br>Пример: `"Название сообщества"` |
| `result[].source.link` | string | Ссылка на источник диалога<br>Пример: `"https://vk.com/club0000123"` |
| `result[].source.data` | object | Другие данные об источнике |
| `result[].customData` | object | Другие данные об посетителе |
| `result[].utm` | object | UTM-метки |
| `result[].utm.utm_source` | string |  |
| `result[].utm.utm_medium` | string |  |
| `result[].utm.utm_campaign` | string |  |
| `result[].utm.utm_term` | string |  |
| `result[].utm.utm_content` | string |  |
| `result[].utm.utm_referrer` | string |  |
| `result[].tags` | array<string> | Тэги клиента |
| `result[].applicationLink` | string | Ссылка на приложение оператора для открытия диалога |
| `result[].infoLink` | string | Ссылка на информацию о клиенте |
| `result[].roistatVisitId` | string | Значение Cookie roistat_visit<br>Пример: `"1000001"` |
| `result[].yandexMetrika` | object | Данные Яндекс.Метрики |
| `result[].yandexMetrika.clientId` | string | clientId из Яндекс.Метрики<br>Пример: `"abcdef"` |
| `result[].googleAnalytics` | object | Данные Google Analytics |
| `result[].googleAnalytics.trackingId` | string | trackingId из Google Analytics<br>Пример: `"abcdef"` |
| `result[].googleAnalytics.clientId` | string | clientId из Google Analytics<br>Пример: `"abcdef"` |

## POST /chat/message/getUnreadedMessageCount — Получение количества непрочитанных сообщений

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1getUnreadedMessageCount/post -->

Данный метод позволяет получить количество непрочитанных клиентов или оператором сообщений в чате

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/getUnreadedMessageCount`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `operatorLogin` | string |  | Логин оператора<br>Если передать - будет возвращено количество непрочитанных этим оператором сообщений. Если не передавать, то вернется количество для клиента |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/getUnreadedMessageCount' \
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
    "count": 0
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatGetUnreadedMessageCountResult) |
| `result.count` | integer | Количество непрочитанных сообщений |

## POST /chat/message/getClientMessageList — Список сообщений по одному клиенту

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1getClientMessageList/post -->

Данный метод позволит получить историю общения с конкретным клиентом.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/getClientMessageList`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `firstMessageId` | integer |  | ID первого сообщения, с которого вы хотите начать выборку (не включая этот id) |
| `lastMessageId` | integer |  | ID последнего сообщения, на котором вы хотите остановить выборку (не включая этот id) |
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `orderDirection` | string |  | Направление сортировки сообщений<br>`asc` - по возрастанию id<br>`desc` - по убыванию id<br>Значения: `asc`, `desc`<br>По умолчанию: `"asc"` |
| `withAutoActionMessages` | boolean |  | Возвращать также сообщения, отправленные через авто-действия<br>По умолчанию: `false` |
| `page` | integer |  | Номер страницы<br>По умолчанию: `0`<br>min: 0 |
| `limit` | integer |  | Количество записей на страницу<br>По умолчанию: `30`<br>min: 1<br>max: 500 |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/getClientMessageList' \
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
        "operator": "my_operator",
        "operatorName": "Алексей",
        "whoSend": "operator",
        "text": "Hello, world",
        "content": {
          "text": "Здравствуйте! Чем можем помочь?",
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
          ],
          "buttons": [
            {
              "text": "Здравствуйте! Чем можем помочь?"
            }
          ],
          "sticker": {
            "fileName": "string",
            "isStaticImage": true,
            "isTgs": true,
            "url": "https://example.com"
          },
          "knowledgeBaseArticles": [
            {
              "registerId": "string",
              "descr": "string"
            }
          ]
        },
        "dateTime": "2026-10-01 12:00:00",
        "dateTimeOrganization": "2026-10-01 12:00:00",
        "dateTimeUTC": "2026-10-01 12:00:00",
        "isVisibleForClient": true,
        "tags": [
          "string"
        ]
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatMessagesGetClientMessagesListResult) |
| `result.count` | integer | Количество объектов<br>Пример: `65` |
| `result.limit` | integer | Количество на страницу<br>Пример: `30` |
| `result.items` | array<object> | Список объектов<br>Структура: [Сообщение (ChatMessage)](11-models.md#сообщение-chatmessage) |

## POST /chat/message/getDialog — Получение диалога по ID

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1getDialog/post -->

Данный метод позволит получить историю общения в конкретном диалоге.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/getDialog`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `dialogId` | integer | да | ID диалога |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/getDialog' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "dialogId": 0
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "dialog": {
      "dialogId": 0,
      "dialogNumber": 0,
      "dialogStatusId": "string",
      "assigned": {
        "operatorLogins": [
          "string"
        ],
        "groupIds": [
          "string"
        ]
      },
      "isClosed": true,
      "startTime": 1790000000,
      "closeCount": 0,
      "tags": [
        "string"
      ],
      "statistic": {
        "hasOnlineQuestion": true,
        "hasOnlineAnswer": true,
        "isAnsweredInTime": true,
        "hasOfflineQuestion": true,
        "hasOfflineAnswer": true,
        "hasForward": true,
        "hasAutoForward": true,
        "isFirstMessageWasFromOperator": true,
        "isOperatorAnswerWithoutClientQuestion": true,
        "isOperatorAskForRate": true,
        "duration": 0,
        "clientRealMessageCount": 0,
        "clientRealMessageCountForBot": 0,
        "operatorRealMessageCount": 0,
        "operatorRealMessageCountByBot": 0
      },
      "rates": [
        {
          "id": 0,
          "rate": "good",
          "dateTime": "2026-10-01 12:00:00",
          "isRead": true,
          "isApproved": true
        }
      ],
      "botCascadeMessages": [
        {
          "id": "string",
          "schemeId": "string"
        }
      ],
      "lastBotSchemeThatSendMessage": [
        {
          "id": "string",
          "schemeId": "string"
        }
      ],
      "filledFormTabs": [
        {
          "id": "string",
          "descr": "string"
        }
      ]
    },
    "messages": [
      {
        "operator": "my_operator",
        "operatorName": "Алексей",
        "whoSend": "operator",
        "text": "Hello, world",
        "content": {
          "text": "Здравствуйте! Чем можем помочь?",
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
          ],
          "buttons": [
            {
              "text": "Здравствуйте! Чем можем помочь?"
            }
          ],
          "sticker": {
            "fileName": "string",
            "isStaticImage": true,
            "isTgs": true,
            "url": "https://example.com"
          },
          "knowledgeBaseArticles": [
            {
              "registerId": "string",
              "descr": "string"
            }
          ]
        },
        "dateTime": "2026-10-01 12:00:00",
        "dateTimeOrganization": "2026-10-01 12:00:00",
        "dateTimeUTC": "2026-10-01 12:00:00",
        "isVisibleForClient": true,
        "tags": [
          "string"
        ]
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatMessagesGetDialogResult) |
| `result.dialog` | object | Диалог<br>Структура: [Диалог (ChatOperatorDialogsReportDialog)](11-models.md#диалог-chatoperatordialogsreportdialog) |
| `result.messages` | array<object> | Сообщения<br>Структура: [Сообщение (ChatMessage)](11-models.md#сообщение-chatmessage) |

## POST /chat/message/getClientDialogs — Получение диалогов клиента

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1getClientDialogs/post -->

Данный метод позволит получить диалоги с клиентом

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/getClientDialogs`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `returnOnlyNotClosed` | boolean |  | Вернуть только незавершённые диалоги |
| `reverse` | boolean |  | Возвращать диалоги в обратном порядке<br>По умолчанию: `true` |
| `withMessages` | boolean |  | Возвращать список сообщений в диалоге |
| `page` | integer |  | Номер страницы<br>По умолчанию: `0`<br>min: 0 |
| `limit` | integer |  | Количество записей на страницу<br>По умолчанию: `30`<br>min: 1<br>max: 500 |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/getClientDialogs' \
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
        "dialogId": 0,
        "dialogNumber": 0,
        "dialogStatusId": "string",
        "assigned": {
          "operatorLogins": [
            "string"
          ],
          "groupIds": [
            "string"
          ]
        },
        "isClosed": true,
        "startTime": 1790000000,
        "closeCount": 0,
        "tags": [
          "string"
        ],
        "statistic": {
          "hasOnlineQuestion": true,
          "hasOnlineAnswer": true,
          "isAnsweredInTime": true,
          "hasOfflineQuestion": true,
          "hasOfflineAnswer": true,
          "hasForward": true,
          "hasAutoForward": true,
          "isFirstMessageWasFromOperator": true,
          "isOperatorAnswerWithoutClientQuestion": true,
          "isOperatorAskForRate": true,
          "duration": 0,
          "clientRealMessageCount": 0,
          "clientRealMessageCountForBot": 0,
          "operatorRealMessageCount": 0,
          "operatorRealMessageCountByBot": 0
        },
        "rates": [
          {
            "id": 0,
            "rate": "good",
            "dateTime": "2026-10-01 12:00:00",
            "isRead": true,
            "isApproved": true
          }
        ],
        "botCascadeMessages": [
          {
            "id": "string",
            "schemeId": "string"
          }
        ],
        "lastBotSchemeThatSendMessage": [
          {
            "id": "string",
            "schemeId": "string"
          }
        ],
        "filledFormTabs": [
          {
            "id": "string",
            "descr": "string"
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
| `result` | object | Результат работы метода (ChatMessagesGetClientDialogsResult) |
| `result.count` | integer | Количество объектов<br>Пример: `65` |
| `result.limit` | integer | Количество на страницу<br>Пример: `30` |
| `result.items` | array<object> | Список объектов<br>Структура: [Диалог (ChatOperatorDialogsReportDialog)](11-models.md#диалог-chatoperatordialogsreportdialog) |

## POST /chat/message/updateDialog — Обновление диалога

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1updateDialog/post -->

Данный метод позволит изменить данные одного диалога.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/updateDialog`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `dialogId` | integer | да | ID диалога |
| `tags` | array<string> |  | Тэги диалога |
| `questionCategory` | string |  | Категория вопроса |
| `fields` | object |  | Значения полей диалога |
| `statusId` | string |  | id нового статуса диалога |
| `assigned` | object |  | Новые ответственные |
| `assigned.operatorLogins` | array<string> |  | Логины операторов |
| `assigned.groupIds` | array<string> |  | id отделов |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/updateDialog' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "dialogId": 0,
  "tags": [
    "Важный вопрос",
    "Оплата"
  ],
  "fields": {
    "foo": "bar",
    "key": "value"
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

## POST /chat/message/sendToOperator — Отправка сообщения оператору

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1sendToOperator/post -->

Данный метод позволит отправить сообщение в чат от имени посетителя сайта.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/sendToOperator`

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
| `operator` | object |  | Оператор |
| `operator.login` | string |  | Логин оператора<br>Пример: `"my_login"` |
| `operator.groupId` | string |  | Идентификатор отдела<br>Пример: `"grewg43q0123qahlad"` |
| `operator.needBalance` | boolean |  | Включение автоматического выбора оператора |
| `operator.virtual` | boolean |  | Виртуальный оператор<br>Если передать `true`, то не будет осуществляться проверка существования переданного логина оператора |
| `message` | object | да | Сообщение |
| `message.text` | string | да | Текст сообщения<br>minLength: 1<br>Пример: `"Hello, world"` |
| `message.replyToMessageId` | integer |  | id сообщения, на которое дается ответ |
| `message.replyToContent` | object |  | Произвольное сообщение на которое дается ответ. Будет отображено в виде цитаты |
| `message.replyToContent.text` | string | да | Текст сообщения |
| `message.tags` | array<string> |  | Тэги сообщения |
| `message.attachments` | array<string> |  | Идентификаторы прикрепленных файлов<br>[Перейти к документации](https://lcab.talk-me.ru/cabinet/json-doc/fileshare#tag/Fileshareupload) по загруке файлов на наш сервер.<br>*Обратите внимание*, что API методы для загрузки файлов выполняются с `токеном от API личного кабинета`. |
| `message.type` | string |  | Тип сообщения<br>Если не передавать, то будет отправлено обычное сообщение.<br>`comment` - комментарий<br>`notification` - уведомление<br>Значения: `comment`, `notification` |
| `message.tag` | string |  | Ваш дополнительный идентификатор сообщения<br>Желательно, чтобы он был уникальным<br>maxLength: 32<br>Пример: `"1123hh12edffey878"` |
| `dialog` | object |  | Диалог |
| `dialog.tags` | array<string> |  | Тэги диалога |

**Пояснения к полям**

`client`:

Нужно передать один из вариантов идентификации — Клиент по clientId: `client.id`; Клиент по searchId: `client.searchId`.


**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/sendToOperator' \
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
  },
  "message": {
    "text": "Hello, world",
    "tags": [
      "Важный вопрос",
      "Оплата"
    ],
    "attachments": [
      "65ryjkl0asdfyujhcmcbasdf",
      "aytdrtx213eghfwkfkjfjhj"
    ],
    "tag": "1123hh12edffey878"
  }
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "id": 0
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatSendMessageToOperatorResult) |
| `result.id` | integer | Уникальный идентификатор |

## POST /chat/message/sendToClient — Отправка сообщения клиенту

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1sendToClient/post -->

Данный метод позволит отправить сообщение в чат от имени оператора.
Сообщение можно отправить только если последнее сообщение в диалоге было от клиента, или если с момента последнего сообщения от клиента прошло меньше 7 дней

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/sendToClient`

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
| `operator` | object | да | Оператор |
| `operator.login` | string | да | Логин оператора<br>Пример: `"my_login"` |
| `operator.virtual` | boolean |  | Виртуальный оператор<br>Если передать `true`, то не будет осуществляться проверка существования переданного логина оператора |
| `message` | object | да | Сообщение |
| `message.text` | string | да | Текст сообщения<br>Пример: `"Hello, world"` |
| `message.replyToMessageId` | integer |  | id сообщения, на которое дается ответ |
| `message.replyToContent` | object |  | Произвольное сообщение на которое дается ответ. Будет отображено в виде цитаты |
| `message.replyToContent.text` | string | да | Текст сообщения |
| `message.tags` | array<string> |  | Тэги сообщения |
| `message.buttons` | array<object> |  | Кнопки под сообщением |
| `message.buttons[].text` | string | да | Текст кнопки<br>Пример: `"У меня вопрос по оплате"` |
| `message.buttons[].actions` | array<object> | да | Действия |
| `message.buttons[].actions[].type` | string | да | Действие при нажатии на кнопку (см. пояснение ниже)<br>Значения: `sendMessageToOperator`, `startChatBot`, `openWidgetTab`, `closeWidget`, `openUrl`, `sendToAnalytics`, `setTargetClient`, `javascript` |
| `message.buttons[].actions[].params` | object |  | Параметры действия (см. пояснение ниже) |
| `message.disableTextInput` | boolean |  | Блокировать поле ввода сообщения при отправленных кнопках<br>На данный момент это доступно только для виджета онлайн-чата на сайте |
| `message.attachments` | array<string> |  | Идентификаторы прикрепленных файлов<br>[Перейти к документации](https://lcab.talk-me.ru/cabinet/json-doc/fileshare#tag/Fileshareupload) по загруке файлов на наш сервер.<br>*Обратите внимание*, что API методы для загрузки файлов выполняются с `токеном от API личного кабинета`. |
| `message.type` | string |  | Тип сообщения<br>Если не передавать, то будет отправлено обычное сообщение.<br>`comment` - комментарий<br>Значения: `comment` |
| `message.dateTime` | integer |  | UTC таймштамп времени для отложенной отправки<br>Пример: `1790000000` |
| `message.tag` | string |  | Ваш дополнительный идентификатор сообщения<br>Желательно, чтобы он был уникальным<br>maxLength: 32<br>Пример: `"1123hh12edffey878"` |
| `dialog` | object |  | Диалог |
| `dialog.tags` | array<string> |  | Тэги диалога |
| `markAsRead` | boolean |  | Помечать чат прочитанным для ответившего оператора<br>По умолчанию: `true` |
| `countInOperatorStatistic` | boolean |  | Учитывать ответ в статистике операторов<br>По умолчанию: `true` |

**Пояснения к полям**

`client`:

Нужно передать один из вариантов идентификации — Клиент по clientId: `client.id`; Клиент по searchId: `client.searchId`.

`message.buttons[].actions[].type`:

* `sendMessageToOperator` - Отправка сообщения оператору
* `startChatBot` - Запуск чат-бота
* `openWidgetTab` - Открыть вкладку виджета
* `closeWidget` - Закрыть виджет
* `openUrl` - Перейти на другую страницу
* `sendToAnalytics` - Отправить событие в Google Analytics и Яндекс.Метрика
* `setTargetClient` - Пометить как целевого
* `javascript` - Выполнить Javascript код

`message.buttons[].actions[].params`:

Параметры для типа `sendMessageToOperator`:

* `messageRecipient` (*string*) - Получатель сообщения


Параметры для типа `startChatBot`:

* `schemeId` (*string*) - ID сценария


Параметры для типа `openWidgetTab`:

* `tabId` (*string*) - Вкладка виджета


Параметры для типа `openUrl`:

* `url` (*string*) - Адрес страницы
* `newWindow` (*boolean*) - Открывать в новом окне
* `hideButtonsAfterClick` (*boolean*) - Прятать кнопки после открытия ссылки


Параметры для типа `sendToAnalytics`:

* `eventId` (*string*) - Идентификатор события


Параметры для типа `setTargetClient`:

* `reason` (*string*) - Текст уведомления


Параметры для типа `javascript`:

* `script` (*string*) - Javascript код


**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/sendToClient' \
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
  },
  "operator": {
    "login": "my_login"
  },
  "message": {
    "text": "Hello, world",
    "tags": [
      "Важный вопрос",
      "Оплата"
    ],
    "attachments": [
      "65ryjkl0asdfyujhcmcbasdf",
      "aytdrtx213eghfwkfkjfjhj"
    ],
    "dateTime": 1790000000,
    "tag": "1123hh12edffey878"
  }
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "id": 0
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatSendMessageToClientResult) |
| `result.id` | integer | Уникальный идентификатор |

## POST /chat/message/startChat — Начать чат

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1startChat/post -->

С помощью этого метода вы можете первыми написать клиенту в различных каналах связи (Viber, Whatsapp, Email и других) зная его номер телефона или почту.

Доступные каналы могут варьироваться в зависимости от того, что настроено для вашего аккаунта в личном кабинете.

За отправку сообщений может взиматься дополнительная плата по вашему тарифу, в зависимости от выбранного канала.

В некоторых каналах может отправляться только заранее одобренный в качестве сервисного шаблона текст сообщений.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/startChat`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `channelId` | string | да | id канала связи (см. пояснение ниже)<br>Значения: `viber`, `whatsapp`, `mailru`, `pager`, `email`, `startChat_wazzup`, `startChat_greenApi`, `startChat_wammchat` |

**Пояснения к полям**

`channelId`:

`viber` - Viber
`whatsapp` - Whatsapp
`mailru` - VK и OK
`pager` - SMS
`email` - Email
`startChat_wazzup` - Wazzup
`startChat_greenApi` - Green API
`startChat_wammchat` - Wamm.chat


Остальные поля зависят от значения `channelId`:

**`channelId` = `viber`, `whatsapp`, `mailru`, `pager`, `startChat_wazzup`, `startChat_greenApi`, `startChat_wammchat`**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `operatorLogin` | string | да | Логин оператора, от чьего имени идет начало диалога |
| `recipientId` | string | да | Получатель<br>Номер телефона клиента |
| `content` | object | да | Контент сообщения |
| `content.text` | string | да | Текст сообщения |
| `sourceId` | string | да | Имя отправителя |

```json
{
  "channelId": "viber",
  "operatorLogin": "my_login",
  "recipientId": "79001234567",
  "content": {
    "text": "Здравствуйте! Чем можем помочь?"
  },
  "sourceId": "my_sender"
}
```

**`channelId` = `email`**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `operatorLogin` | string | да | Логин оператора, от чьего имени идет начало диалога |
| `recipientId` | string | да | Получатель<br>Адрес электронной почты клиента |
| `content` | object | да | Контент сообщения |
| `content.text` | string | да | Текст сообщения |
| `sourceId` | string | да | Имя отправителя |
| `params` | object |  | Дополнительные параметры сообщения для канала "Email" |
| `params.emailSubject` | string |  | Тема письма |

```json
{
  "channelId": "email",
  "operatorLogin": "my_login",
  "recipientId": "ivan@example.com",
  "content": {
    "text": "Здравствуйте! Чем можем помочь?"
  },
  "sourceId": "my_sender"
}
```

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/startChat' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "channelId": "viber",
  "operatorLogin": "my_login",
  "recipientId": "79001234567",
  "content": {
    "text": "Здравствуйте! Чем можем помочь?"
  },
  "sourceId": "my_sender"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "searchId": 0
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatStartChatResult) |
| `result.searchId` | integer | Идентификатор клиента в нашей системе |

## POST /chat/message/getStartChatChannels — Получение доступных каналов для "Начать чат"

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1getStartChatChannels/post -->

Данный метод позволит получить настроенные каналы для функции "Начать чат"

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/getStartChatChannels`

**Параметры запроса**

Метод не принимает параметров — передайте пустой JSON-объект `{}`.

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/getStartChatChannels' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "channels": [
      {
        "id": "string",
        "descr": "string",
        "sources": [
          {
            "id": "string",
            "descr": "string"
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
| `result` | object | Результат работы метода (ChatStartChatGetChannelsResult) |
| `result.channels` | array<object> | Каналы |
| `result.channels[].id` | string | id канала |
| `result.channels[].descr` | string | Название канала |
| `result.channels[].sources` | array<object> | Доступные имена отправителя |
| `result.channels[].sources[].id` | string | Идентификатор имени отправителя |
| `result.channels[].sources[].descr` | string | Название имени отправителя |

## POST /chat/message/setSuggestedAnswerToClient — Предложить ответ оператору

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1setSuggestedAnswerToClient/post -->

Данный метод позволяет отобразить в приложении для оператора предлагаемый вариант ответа клиенту

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/setSuggestedAnswerToClient`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `message` | object | да | Предлагаемое сообщение |
| `message.text` | string | да | Текст сообщения |
| `replyToMessageId` | integer |  | ID сообщения, на которое предлагается ответ |
| `rate` | object |  | Параметры для оценивания ответа |
| `rate.likeUrl` | string |  | Ссылка для webhook-а о лайке |
| `rate.dislikeUrl` | string |  | Ссылка для webhook-а о дизлайке |
| `rate.isAutoLikeOnUsage` | boolean |  | Автоматически отправлять уведомление о лайке при использовании<br>По умолчанию: `true` |
| `rate.autoLikeOnUsageSimilarityPercent` | integer |  | При каком проценте схожести ответа отправлять авто-уведомление о лайке<br>По умолчанию: `100`<br>min: 0<br>max: 100 |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/setSuggestedAnswerToClient' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "client": {
    "clientId": "ha832rjaafle4",
    "searchId": 12345
  },
  "message": {
    "text": "Здравствуйте! Чем можем помочь?"
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

## POST /chat/message/sendTypingToClient — Имитация набора сообщения

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1sendTypingToClient/post -->

Данный метод позволит отправить запустить имитацию набора сообщения для тех платформ, что поддерживают эту функцию

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/sendTypingToClient`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `operator` | object | да | Оператор |
| `operator.login` | string | да | Логин оператора<br>Пример: `"my_login"` |
| `operator.virtual` | boolean |  | Виртуальный оператор<br>Если передать `true`, то не будет осуществляться проверка существования переданного логина оператора |
| `ttl` | integer |  | Длительность имитации в секундах<br>По умолчанию: `30` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/sendTypingToClient' \
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

## POST /chat/message/editMessage — Редактирование сообщения

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1editMessage/post -->

Данный метод позволит отредактировать сообщение оператора или клиента (если оно было также отправлено через API)
Обратите внимание, что не все каналы позволяют отредактировать отправленное сообщение.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/editMessage`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `message` | object | да | Сообщение |
| `message.id` | integer | да | Идентификатор сообщения, которое нужно отредактировать<br>Пример: `123` |
| `message.text` | string | да | Новый текст сообщения |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/editMessage' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": {
    "id": 123,
    "text": "Здравствуйте! Чем можем помочь?"
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

## POST /chat/message/deleteMessage — Удаление сообщения

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1deleteMessage/post -->

Данный метод позволит удалить сообщение.
Обратите внимание, что не все каналы позволяют удалять сообщения.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/deleteMessage`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `messageId` | integer | да | Идентификатор удаляемого сообщения<br>Пример: `123` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/deleteMessage' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "messageId": 123
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/message/editMessageSentToClient — Редактирование сообщения, отправленного клиенту

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1editMessageSentToClient/post -->

> **Устаревший метод.** Сохраняется для совместимости; в новых интеграциях используйте `/chat/message/editMessage`.

Данный метод позволит отредактировать сообщение оператора.
Обратите внимание, что не все каналы позволяют отредактировать отправленное сообщение.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/editMessageSentToClient`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `message` | object | да | Сообщение |
| `message.id` | integer | да | Идентификатор сообщения, которое нужно отредактировать<br>Пример: `123` |
| `message.text` | string | да | Новый текст сообщения |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/editMessageSentToClient' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": {
    "id": 123,
    "text": "Здравствуйте! Чем можем помочь?"
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

## POST /chat/message/deleteMessageToClientMethod — Удаление сообщения, отправленного клиенту

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1deleteMessageToClientMethod/post -->

> **Устаревший метод.** Сохраняется для совместимости; в новых интеграциях используйте `/chat/message/deleteMessage`.

Данный метод позволит удалить сообщение оператора.
Обратите внимание, что не все каналы позволяют удалить отправленное сообщение.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/deleteMessageToClientMethod`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `messageId` | integer | да | Идентификатор удаляемого сообщения<br>Пример: `123` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/deleteMessageToClientMethod' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "messageId": 123
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/message/deleteDialogsWithClient — Удаление всей переписки с клиентом

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1deleteDialogsWithClient/post -->

Данный метод позволит удалить всю переписку с клиентом.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/deleteDialogsWithClient`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/deleteDialogsWithClient' \
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

## POST /chat/message/setStatus — Изменение статуса сообщения

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1setStatus/post -->

Изменение статуса сообщения.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/setStatus`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `messageId` | integer | да | Идентификатор сообщения<br>Пример: `123` |
| `status` | string | да | Статус сообщения<br>`delivered` - Доставлено<br>`readed` - Просмотрено<br>Значения: `delivered`, `readed` |
| `operatorLogin` | string |  | Логин оператора, который прочитал сообщение<br>Не передавайте, если хотите прочитать сообщение, отправленное оператором за клиента, или сообщение, отправленное клиентом - за всех операторов<br>Пример: `"my_login"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/setStatus' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "messageId": 123,
  "status": "delivered",
  "operatorLogin": "my_login"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/message/setReaction — Изменение реакции на сообщение

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1setReaction/post -->

Изменение реакции на сообщение.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/setReaction`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `messageId` | integer | да | Идентификатор сообщения<br>Пример: `123` |
| `emoji` | string \| null |  | emoji с реакцией на сообщение<br>Не передавайте, если хотите удалить реакцию |
| `operatorLogin` | string |  | Логин оператора, который устанавливает реакцию<br>Не передавайте, если реакция передается от имени клиента<br>Пример: `"my_login"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/setReaction' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "messageId": 123,
  "operatorLogin": "my_login"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/message/forward — Перенаправление посетителя

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1forward/post -->

Перенаправление посетителя.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/forward`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `client` | object | да | Клиент<br>Должен быть передан хотя бы один из двух вариантов идентификаторов |
| `client.clientId` | string |  | Уникальный идентификатор из Cookies<br>minLength: 1<br>Пример: `"ha832rjaafle4"` |
| `client.searchId` | integer |  | Уникальный идентификатор посетителя для поиска<br>Пример: `12345` |
| `from` | object | да | Оператор, который делает переключение |
| `from.login` | string | да | Логин оператора<br>Пример: `"login1"` |
| `to` | object | да | Оператор (или группа), на которого происходит переключение.<br>Необходимо передать либо `login`, либо `groupId`, либо `оба параметра` |
| `to.login` | string |  | Логин оператора<br>Пример: `"login2"` |
| `to.groupId` | string |  | Идентификатор отдела операторов<br>Пример: `"716812a2bc"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/forward' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "client": {
    "clientId": "ha832rjaafle4",
    "searchId": 12345
  },
  "from": {
    "login": "login1"
  },
  "to": {
    "login": "login2",
    "groupId": "716812a2bc"
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

## POST /chat/message/closeDialog — Завершение диалога

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1closeDialog/post -->

Данный метод позволит программно завершить диалог с клиентом.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/closeDialog`

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
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/closeDialog' \
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

## POST /chat/message/getDialogStatusList — Список статусов диалога

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatmessage/paths/~1chat~1message~1getDialogStatusList/post -->

Данный метод позволит получить возможные статусы диалога.

`POST https://lcab.talk-me.ru/json/v1.0/chat/message/getDialogStatusList`

**Параметры запроса**

Метод не принимает параметров — передайте пустой JSON-объект `{}`.

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/getDialogStatusList' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": [
    {
      "id": "string",
      "descr": "string"
    }
  ]
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | array<object> | Статусы диалога |
| `result[].id` | string | Идентификатор статуса |
| `result[].descr` | string | Название статуса |
