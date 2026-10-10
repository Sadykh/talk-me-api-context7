# Модели данных в ответах API

Структуры объектов, которые возвращаются сразу несколькими методами онлайн-чата Talk-Me. В описаниях методов на них стоят ссылки «Структура: …».

## Сообщение (ChatMessage)

| Поле | Тип | Описание |
|---|---|---|
| `id` | integer | Уникальный идентификатор<br>Может быть `null`, если это сообщений из авто-действий.<br>Пример: `123` |
| `operator` | string | Логин оператора<br>Пример: `"my_operator"` |
| `operatorName` | string | Имя оператора<br>Пример: `"Алексей"` |
| `whoSend` | string | Отправитель сообщения<br>`client` - клиент<br>`operator` - оператор<br>Значения: `operator`, `client` |
| `text` | string | Текстовое представление контента<br>Пример: `"Hello, world"` |
| `content` | object | Контент сообщения<br>Структура: [Контент сообщения (OnlineMessageContent)](11-models.md#контент-сообщения-onlinemessagecontent) |
| `dateTime` | string | Дата отправки (Мск)<br>Формат YYYY-MM-DD HH:MM:SS<br>Пример: `"2026-10-01 12:00:00"` |
| `dateTimeOrganization` | string | Дата отправки (по вашему часовому поясу)<br>Формат YYYY-MM-DD HH:MM:SS<br>Пример: `"2026-10-01 12:00:00"` |
| `dateTimeUTC` | string | Дата отправки (UTC)<br>Формат YYYY-MM-DD HH:MM:SS<br>Пример: `"2026-10-01 12:00:00"` |
| `messageType` | string | Тип сообщения<br>Расшифровка значений: [Тип сообщения](12-dictionaries.md#тип-сообщения)<br>Значения: `comment`, `operatorComment`, `futureNotify`, `autoForward`, `autoForwardOffline`, `initiate`, `simulated`, `sms`, `viber`, `whatsapp`, `mailru`, `email`, `messengerAggregator`, `autoMessage`, `supportAPI`, `forward`, `forwardHidden`, `unsubscribe`, `notification`, `rithoricQuestion`, `acceptDialog`, `setActiveDialogStatus`, `closeDialog`, `autoCloseDialog`, `reopenDialog`, `tab`, `tip`, `requestContact`, `cabinetSender`, `operatorRunBot`, `bot`, `integrationStart`, `integrationStop`, `integrationCallSuccess`, `integrationCallFailed`, `webRTCCallStart`, `webRTCCallUpdate`, `webRTCCallError`, `webRTCCallStop` |
| `dialogId` | integer | Идентификатор диалога |
| `status` | string | Статус сообщения<br>`delivered` - Доставлено<br>`readed` - Просмотрено<br>Значения: `delivered`, `readed` |
| `isVisibleForClient` | boolean | Сообщение видно посетителю |
| `integrationPlatformMessageId` | string | ID сообщения из интеграции с мессенджерами |
| `page` | object | Страница |
| `page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `tags` | array<string> | Тэги сообщения |
| `senderOverride` | object | Переназначенный отправитель сообщения<br>Может быть указан в некоторых интеграциях (например, Telegram и Max) в групповых чатах, чтобы было ясно - что именно за пользователь написал в групповой чат |
| `senderOverride.name` | string | Имя |
| `senderOverride.avatar` | string | Ссылка на аватар |
| `replyTo` | object | Сообщение<br>Рекурсивно: та же структура, что у `ChatMessage` |

```json
{
  "id": 123,
  "operator": "my_operator",
  "operatorName": "Алексей",
  "whoSend": "operator",
  "text": "Hello, world",
  "content": {
    "text": "Здравствуйте! Чем можем помочь?",
    "attachments": [
      {
        "id": "acbd18db4cc2f85cedef654fccc4a4d8",
        "url": "https://server.com/download?id=123",
        "fileSize": 123,
        "fileName": "example.jpg",
        "type": {
          "id": "file",
          "descr": "string",
          "icon": "string"
        },
        "isUncompressedImage": true,
        "audioTranscribe": {
          "isWaiting": true,
          "text": "Здравствуйте! Чем можем помочь?",
          "language": "string"
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
      "url": "https://example.com",
      "emoji": "👍"
    },
    "knowledgeBaseArticles": [
      {
        "registerId": "string",
        "articleId": "article_id",
        "groupId": "group_id",
        "descr": "string",
        "url": "https://example.com"
      }
    ]
  },
  "dateTime": "2026-10-01 12:00:00",
  "dateTimeOrganization": "2026-10-01 12:00:00",
  "dateTimeUTC": "2026-10-01 12:00:00",
  "messageType": "comment",
  "dialogId": 0,
  "status": "delivered",
  "isVisibleForClient": true,
  "integrationPlatformMessageId": "string",
  "page": {
    "url": "http://example.com",
    "title": "Example.com - Homepage"
  },
  "tags": [
    "string"
  ],
  "senderOverride": {
    "name": "Иван",
    "avatar": "string"
  },
  "replyTo": {}
}
```

## Контент сообщения (OnlineMessageContent)

| Поле | Тип | Описание |
|---|---|---|
| `text` | string | Текст сообщения |
| `attachments` | array<object> | Файлы-вложения<br>Структура: [Вложение (OnlineMessageAttachment)](11-models.md#вложение-onlinemessageattachment) |
| `buttons` | array<object> | Кнопки |
| `buttons[].text` | string | Текст в кнопке |
| `sticker` | object | Стикер |
| `sticker.fileName` | string | Полное имя файла |
| `sticker.isStaticImage` | boolean | Является простой картинкой |
| `sticker.isTgs` | boolean | Является анимированным стикером телеги (*.tgs) |
| `sticker.url` | string | Ссылка на стикер |
| `sticker.emoji` | string | Альтернативный Emoji |
| `knowledgeBaseArticles` | array<object> | Вложенные статьи из базы знаний |
| `knowledgeBaseArticles[].registerId` | string | id базы знаний |
| `knowledgeBaseArticles[].articleId` | string | id статьи (если передана статья) |
| `knowledgeBaseArticles[].groupId` | string | id группы (если передана группа) |
| `knowledgeBaseArticles[].descr` | string | Название статьи |
| `knowledgeBaseArticles[].url` | string | Ссылка на статью |

```json
{
  "text": "Здравствуйте! Чем можем помочь?",
  "attachments": [
    {
      "id": "acbd18db4cc2f85cedef654fccc4a4d8",
      "url": "https://server.com/download?id=123",
      "fileSize": 123,
      "fileName": "example.jpg",
      "type": {
        "id": "file",
        "descr": "string",
        "icon": "string"
      },
      "isUncompressedImage": true,
      "audioTranscribe": {
        "isWaiting": true,
        "text": "Здравствуйте! Чем можем помочь?",
        "language": "string"
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
    "url": "https://example.com",
    "emoji": "👍"
  },
  "knowledgeBaseArticles": [
    {
      "registerId": "string",
      "articleId": "article_id",
      "groupId": "group_id",
      "descr": "string",
      "url": "https://example.com"
    }
  ]
}
```

## Вложение (OnlineMessageAttachment)

| Поле | Тип | Описание |
|---|---|---|
| `id` | string | ID файла<br>Пример: `"acbd18db4cc2f85cedef654fccc4a4d8"` |
| `url` | string | Адрес файла<br>Пример: `"https://server.com/download?id=123"` |
| `fileSize` | integer | Размер файла в байтах<br>Пример: `123` |
| `fileName` | string | Название файла<br>Пример: `"example.jpg"` |
| `type` | object | Тип файла |
| `type.id` | string | Идентификатор типа<br>Значения: `file`, `image`, `audio`, `video`, `disallowed`, `link` |
| `type.descr` | string | Название |
| `type.icon` | string | Иконка |
| `isUncompressedImage` | boolean | Является несжатым по качеству изображением |
| `audioTranscribe` | object | Аудио-транскрибация |
| `audioTranscribe.isWaiting` | boolean | Ожидает транскрибации |
| `audioTranscribe.text` | string | Текст транскрибации |
| `audioTranscribe.language` | string | Язык транскрибации |

```json
{
  "id": "acbd18db4cc2f85cedef654fccc4a4d8",
  "url": "https://server.com/download?id=123",
  "fileSize": 123,
  "fileName": "example.jpg",
  "type": {
    "id": "file",
    "descr": "string",
    "icon": "string"
  },
  "isUncompressedImage": true,
  "audioTranscribe": {
    "isWaiting": true,
    "text": "Здравствуйте! Чем можем помочь?",
    "language": "string"
  }
}
```

## Диалог (ChatOperatorDialogsReportDialog)

| Поле | Тип | Описание |
|---|---|---|
| `clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `customFields` | object | Значения кастомных полей диалога |
| `messages` | array<object> | Сообщения<br>Выгружается только если передано `withMessages` = `true`<br>Структура: [Сообщение (ChatMessage)](11-models.md#сообщение-chatmessage) |
| `dialogId` | integer | id диалога |
| `dialogNumber` | integer | Порядковый номер диалога для этого клиента |
| `dialogStatusId` | string | Статус диалога |
| `assigned` | object | Ответственные |
| `assigned.operatorLogins` | array<string> | Логины операторов |
| `assigned.groupIds` | array<string> | id отделов |
| `isClosed` | boolean | Диалог завершён? |
| `startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `closedByOperator` | string | Логин оператора, завершившего диалог |
| `closeCount` | integer | Сколько раз был закрыт диалог |
| `tags` | array<string> | Тэги диалога |
| `questionCategory` | string | Категория вопроса |
| `statistic` | object | Статистика диалога<br>Структура: [Статистика диалога (ChatOperatorDialogsReportDialogStatistic)](11-models.md#статистика-диалога-chatoperatordialogsreportdialogstatistic) |
| `operators` | array<object> | Операторы, участвовавшие в диалоге<br>Структура: [Оператор, участвовавший в диалоге (ChatOperatorDialogsReportOperator)](11-models.md#оператор-участвовавший-в-диалоге-chatoperatordialogsreportoperator) |
| `rates` | array<object> | Отзывы, оставленные в ходе диалога |
| `rates[].id` | integer | id отзыва |
| `rates[].rate` | string | Оценка<br>Значения: `good`, `bad`, `1/5`, `2/5`, `3/5`, `4/5`, `5/5` |
| `rates[].text` | string | Текст отзыва |
| `rates[].adminComment` | string | Комментарий администрации |
| `rates[].dateTime` | string | Дата/время отправки отзыва<br>Формат YYYY-MM-DD HH:MM:SS<br>Пример: `"2026-10-01 12:00:00"` |
| `rates[].isRead` | boolean | Отзыв прочтен администраторами? |
| `rates[].isApproved` | boolean | Отзыв одобрен? |
| `rates[].operatorLogin` | string | Логин оператора, кому оставлен отзыв |
| `botCascadeMessages` | array<object> | Каскадные сообщения запущенных во время диалога ботов |
| `botCascadeMessages[].id` | string | id каскадного сообщения |
| `botCascadeMessages[].schemeId` | string | id сценария |
| `lastBotSchemeThatSendMessage` | array<object> | Последний сценарий, отправивший клиенту сообщение в рамках работы бота<br>Тут перечислены все каскадные сообщения (боты) верхнего уровня, и показано - какой сценарий (включая вложенные сценарии) отправил последнее сообщение в рамках работы бота |
| `lastBotSchemeThatSendMessage[].id` | string | id каскадного сообщения |
| `lastBotSchemeThatSendMessage[].schemeId` | string | id сценария |
| `filledFormTabs` | array<object> | Заполненные во время диалога формы |
| `filledFormTabs[].id` | string | id формы |
| `filledFormTabs[].descr` | string | Название формы |
| `ai` | object | AI итоги |
| `ai.isClientSatisfied` | boolean | Удовлетворенность<br>Пример: `true` |
| `ai.clientEmotionId` | integer | Эмоции<br>Расшифровка значений: [Эмоции клиента (AI-анализ диалога)](12-dictionaries.md#эмоции-клиента-ai-анализ-диалога)<br>Пример: `2` |
| `ai.dialogConversationSummarize` | string | Резюме диалога<br>Пример: `"Клиент задал вопрос, и получил ответ от оператора"` |

```json
{
  "clientId": "ha832rjaafle4",
  "client": {
    "searchId": 1234,
    "login": "123_user_at_june",
    "clientId": "123e2rwfjas",
    "name": "Ivan",
    "lastName": "Иванов",
    "firstName": "Иван",
    "secondName": "Иванович",
    "phone": "790012345678",
    "email": "example@gmail.com",
    "country": "Russia",
    "city": "Moscow",
    "firstVisit": {
      "dateTime": "2026-10-01 12:00:00",
      "dateTimeUTC": "2026-10-01 12:00:00",
      "page": {
        "url": "http://example.com",
        "title": "Example.com - Homepage"
      }
    },
    "lastVisit": {
      "dateTime": "2026-10-01 12:00:00",
      "dateTimeUTC": "2026-10-01 12:00:00",
      "lastDateTime": "2026-10-01 12:00:00",
      "lastDateTimeUTC": "2026-10-01 12:00:00",
      "page": {
        "url": "http://example.com",
        "title": "Example.com - Homepage"
      }
    },
    "ip": "85.123.22.41",
    "flag": "red",
    "useragent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54",
    "target": [
      "First reason",
      "Second reason"
    ],
    "isBanned": true,
    "questionCategory": "Common questions",
    "referer": "https://google.com",
    "searchKeyword": "home flowers",
    "visitsCount": 3,
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
    "customData": {
      "foo": "bar",
      "key": "value"
    },
    "utm": {
      "utm_source": "string",
      "utm_medium": "string",
      "utm_campaign": "string",
      "utm_term": "string",
      "utm_content": "string",
      "utm_referrer": "string"
    },
    "tags": [
      "string"
    ],
    "applicationLink": "string",
    "infoLink": "string",
    "roistatVisitId": "1000001",
    "yandexMetrika": {
      "clientId": "abcdef"
    },
    "googleAnalytics": {
      "trackingId": "abcdef",
      "clientId": "abcdef"
    }
  },
  "customFields": {
    "foo": "bar",
    "key": "value"
  },
  "messages": [
    {
      "id": 123,
      "operator": "my_operator",
      "operatorName": "Алексей",
      "whoSend": "operator",
      "text": "Hello, world",
      "content": {
        "text": "Здравствуйте! Чем можем помочь?",
        "attachments": [
          {
            "id": "acbd18db4cc2f85cedef654fccc4a4d8",
            "url": "https://server.com/download?id=123",
            "fileSize": 123,
            "fileName": "example.jpg",
            "type": {
              "id": "file",
              "descr": "string",
              "icon": "string"
            },
            "isUncompressedImage": true,
            "audioTranscribe": {
              "isWaiting": true,
              "text": "Здравствуйте! Чем можем помочь?",
              "language": "string"
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
          "url": "https://example.com",
          "emoji": "👍"
        },
        "knowledgeBaseArticles": [
          {
            "registerId": "string",
            "articleId": "article_id",
            "groupId": "group_id",
            "descr": "string",
            "url": "https://example.com"
          }
        ]
      },
      "dateTime": "2026-10-01 12:00:00",
      "dateTimeOrganization": "2026-10-01 12:00:00",
      "dateTimeUTC": "2026-10-01 12:00:00",
      "messageType": "comment",
      "dialogId": 0,
      "status": "delivered",
      "isVisibleForClient": true,
      "integrationPlatformMessageId": "string",
      "page": {
        "url": "http://example.com",
        "title": "Example.com - Homepage"
      },
      "tags": [
        "string"
      ],
      "senderOverride": {
        "name": "Иван",
        "avatar": "string"
      },
      "replyTo": {}
    }
  ],
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
  "closeTime": 1790000000,
  "closedByOperator": "string",
  "closeCount": 0,
  "tags": [
    "string"
  ],
  "questionCategory": "string",
  "statistic": {
    "firstClientOnlineMessageTime": 1790000000,
    "firstClientOfflineMessageTime": 1790000000,
    "firstOperatorMessageTime": 1790000000,
    "hasOnlineQuestion": true,
    "hasOnlineAnswer": true,
    "isAnsweredInTime": true,
    "hasOfflineQuestion": true,
    "hasOfflineAnswer": true,
    "hasForward": true,
    "hasAutoForward": true,
    "answerTime": 1790000000,
    "delayBetweenFirstAndSecondOperatorAnswer": 1790000000,
    "averageOnlineAnswerTime": 0,
    "averageOfflineAnswerTime": 0,
    "isFirstMessageWasFromOperator": true,
    "isOperatorAnswerWithoutClientQuestion": true,
    "isOperatorAskForRate": true,
    "averageHoldTime": 0,
    "duration": 0,
    "clientRealMessageCount": 0,
    "clientRealMessageCountForBot": 0,
    "operatorRealMessageCount": 0,
    "operatorRealMessageCountByBot": 0
  },
  "operators": [
    {
      "login": "my_login",
      "statistic": {
        "firstClientOnlineMessageTime": 1790000000,
        "firstClientOfflineMessageTime": 1790000000,
        "firstOperatorMessageTime": 1790000000,
        "hasOnlineQuestion": true,
        "hasOnlineAnswer": true,
        "isAnsweredInTime": true,
        "hasOfflineQuestion": true,
        "hasOfflineAnswer": true,
        "hasForward": true,
        "hasAutoForward": true,
        "answerTime": 1790000000,
        "delayBetweenFirstAndSecondOperatorAnswer": 1790000000,
        "averageOnlineAnswerTime": 0,
        "averageOfflineAnswerTime": 0,
        "isFirstMessageWasFromOperator": true,
        "isOperatorAnswerWithoutClientQuestion": true,
        "isOperatorAskForRate": true,
        "averageHoldTime": 0,
        "duration": 0,
        "clientRealMessageCount": 0,
        "clientRealMessageCountForBot": 0,
        "operatorRealMessageCount": 0,
        "operatorRealMessageCountByBot": 0
      }
    }
  ],
  "rates": [
    {
      "id": 0,
      "rate": "good",
      "text": "Здравствуйте! Чем можем помочь?",
      "adminComment": "string",
      "dateTime": "2026-10-01 12:00:00",
      "isRead": true,
      "isApproved": true,
      "operatorLogin": "my_login"
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
  ],
  "ai": {
    "isClientSatisfied": true,
    "clientEmotionId": 2,
    "dialogConversationSummarize": "Клиент задал вопрос, и получил ответ от оператора"
  }
}
```

## Клиент (ChatClient)

| Поле | Тип | Описание |
|---|---|---|
| `searchId` | integer | Уникальный идентификатор посетителя для поиска<br>Пример: `1234` |
| `login` | string | Уникальный логин посетителя (используется в Jabber)<br>Пример: `"123_user_at_june"` |
| `clientId` | string | Идентификатор из Cookie посетителя<br>Пример: `"123e2rwfjas"` |
| `name` | string | ФИО или стандартное имя посетителя<br>Пример: `"Ivan"` |
| `lastName` | string | Фамилия<br>Пример: `"Иванов"` |
| `firstName` | string | Имя<br>Пример: `"Иван"` |
| `secondName` | string | Отчество<br>Пример: `"Иванович"` |
| `phone` | string | Номер телефона<br>Пример: `"790012345678"` |
| `email` | string | Email<br>Пример: `"example@gmail.com"` |
| `country` | string | Страна<br>Пример: `"Russia"` |
| `city` | string | Город<br>Пример: `"Moscow"` |
| `firstVisit` | object | Первый визит |
| `firstVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `firstVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `firstVisit.page` | object | Страница |
| `firstVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `firstVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `lastVisit` | object | Последний визит |
| `lastVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `lastVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `lastVisit.lastDateTime` | string | Дата окончания визита<br>Пример: `"2026-10-01 12:00:00"` |
| `lastVisit.lastDateTimeUTC` | string | Дата окончания визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `lastVisit.page` | object | Страница |
| `lastVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `lastVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `ip` | string | IP-адрес<br>Пример: `"85.123.22.41"` |
| `flag` | string | Флаг<br>Значения: `red`, `orange`, `green`, `blue`, `purple`, `yellow`, `asphalt` |
| `useragent` | string | Useragent браузера<br>Пример: `"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54"` |
| `target` | array<string> | Целевой посетитель |
| `isBanned` | boolean | Пользователь заблокирован |
| `questionCategory` | string | Категория вопроса<br>Пример: `"Common questions"` |
| `referer` | string | Источник перехода<br>Пример: `"https://google.com"` |
| `searchKeyword` | string | Поисковый запрос<br>Пример: `"home flowers"` |
| `visitsCount` | integer | Количество визитов<br>Пример: `3` |
| `isOnline` | boolean | Посетитель в сети |
| `source` | object | Источник диалога |
| `source.type` | object | Тип источника |
| `source.type.id` | string | Идентификатор<br>Пример: `"vk"` |
| `source.type.name` | string | Название<br>Пример: `"VKontakte"` |
| `source.id` | string | ID источника диалога<br>Пример: `"ab4-3fddd45-24dss"` |
| `source.name` | string | Название источника диалога<br>Пример: `"Название сообщества"` |
| `source.link` | string | Ссылка на источник диалога<br>Пример: `"https://vk.com/club0000123"` |
| `source.data` | object | Другие данные об источнике |
| `customData` | object | Другие данные об посетителе |
| `utm` | object | UTM-метки |
| `utm.utm_source` | string |  |
| `utm.utm_medium` | string |  |
| `utm.utm_campaign` | string |  |
| `utm.utm_term` | string |  |
| `utm.utm_content` | string |  |
| `utm.utm_referrer` | string |  |
| `tags` | array<string> | Тэги клиента |
| `applicationLink` | string | Ссылка на приложение оператора для открытия диалога |
| `infoLink` | string | Ссылка на информацию о клиенте |
| `roistatVisitId` | string | Значение Cookie roistat_visit<br>Пример: `"1000001"` |
| `yandexMetrika` | object | Данные Яндекс.Метрики |
| `yandexMetrika.clientId` | string | clientId из Яндекс.Метрики<br>Пример: `"abcdef"` |
| `googleAnalytics` | object | Данные Google Analytics |
| `googleAnalytics.trackingId` | string | trackingId из Google Analytics<br>Пример: `"abcdef"` |
| `googleAnalytics.clientId` | string | clientId из Google Analytics<br>Пример: `"abcdef"` |

```json
{
  "searchId": 1234,
  "login": "123_user_at_june",
  "clientId": "123e2rwfjas",
  "name": "Ivan",
  "lastName": "Иванов",
  "firstName": "Иван",
  "secondName": "Иванович",
  "phone": "790012345678",
  "email": "example@gmail.com",
  "country": "Russia",
  "city": "Moscow",
  "firstVisit": {
    "dateTime": "2026-10-01 12:00:00",
    "dateTimeUTC": "2026-10-01 12:00:00",
    "page": {
      "url": "http://example.com",
      "title": "Example.com - Homepage"
    }
  },
  "lastVisit": {
    "dateTime": "2026-10-01 12:00:00",
    "dateTimeUTC": "2026-10-01 12:00:00",
    "lastDateTime": "2026-10-01 12:00:00",
    "lastDateTimeUTC": "2026-10-01 12:00:00",
    "page": {
      "url": "http://example.com",
      "title": "Example.com - Homepage"
    }
  },
  "ip": "85.123.22.41",
  "flag": "red",
  "useragent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54",
  "target": [
    "First reason",
    "Second reason"
  ],
  "isBanned": true,
  "questionCategory": "Common questions",
  "referer": "https://google.com",
  "searchKeyword": "home flowers",
  "visitsCount": 3,
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
  "customData": {
    "foo": "bar",
    "key": "value"
  },
  "utm": {
    "utm_source": "string",
    "utm_medium": "string",
    "utm_campaign": "string",
    "utm_term": "string",
    "utm_content": "string",
    "utm_referrer": "string"
  },
  "tags": [
    "string"
  ],
  "applicationLink": "string",
  "infoLink": "string",
  "roistatVisitId": "1000001",
  "yandexMetrika": {
    "clientId": "abcdef"
  },
  "googleAnalytics": {
    "trackingId": "abcdef",
    "clientId": "abcdef"
  }
}
```

## Статистика диалога (ChatOperatorDialogsReportDialogStatistic)

| Поле | Тип | Описание |
|---|---|---|
| `firstClientOnlineMessageTime` | integer | Дата\время первого сообщения клиента в онлайн режиме<br>Пример: `1790000000` |
| `firstClientOfflineMessageTime` | integer | Дата\время первого сообщения клиента в оффлайн режиме<br>Пример: `1790000000` |
| `firstOperatorMessageTime` | integer | Дата\время первого сообщения оператора<br>Пример: `1790000000` |
| `hasOnlineQuestion` | boolean | В диалоге есть сообщения, отправленные от клиента к операторам в онлайн-режиме |
| `hasOnlineAnswer` | boolean | Клиент получил ответ в Online-общении? |
| `isAnsweredInTime` | boolean | Ответ дан вовремя? |
| `hasOfflineQuestion` | boolean | В диалоге есть сообщения, отправленные в оффлайн-форму |
| `hasOfflineAnswer` | boolean | Клиент получил ответ на Offline-вопрос? |
| `hasForward` | boolean | В диалоге было переключение на другого оператора? |
| `hasAutoForward` | boolean | В диалоге было автоматическое переключение на другого оператора? |
| `answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `delayBetweenFirstAndSecondOperatorAnswer` | integer | Время между первым и вторым ответом оператора<br>Пример: `1790000000` |
| `averageOnlineAnswerTime` | integer | Среднее время ответа в Online-общении |
| `averageOfflineAnswerTime` | integer | Среднее время ответа на Offline сообщения |
| `isFirstMessageWasFromOperator` | boolean | Первое сообщение было от оператора |
| `isOperatorAnswerWithoutClientQuestion` | boolean | В чате были сообщения клиента, но оператор написал первым (поэтому время ответа не считается) |
| `isOperatorAskForRate` | boolean | Оператор запрашивал отзыв |
| `averageHoldTime` | integer | Средняя задержка между двумя сообщениями оператора подряд |
| `duration` | integer | Продолжительность диалога в секундах |
| `clientRealMessageCount` | integer | Количество реальных сообщений клиента к операторам |
| `clientRealMessageCountForBot` | integer | Количество реальных сообщений клиента к боту |
| `operatorRealMessageCount` | integer | Количество реальных сообщений оператора |
| `operatorRealMessageCountByBot` | integer | Количество реальных сообщений от бота |

```json
{
  "firstClientOnlineMessageTime": 1790000000,
  "firstClientOfflineMessageTime": 1790000000,
  "firstOperatorMessageTime": 1790000000,
  "hasOnlineQuestion": true,
  "hasOnlineAnswer": true,
  "isAnsweredInTime": true,
  "hasOfflineQuestion": true,
  "hasOfflineAnswer": true,
  "hasForward": true,
  "hasAutoForward": true,
  "answerTime": 1790000000,
  "delayBetweenFirstAndSecondOperatorAnswer": 1790000000,
  "averageOnlineAnswerTime": 0,
  "averageOfflineAnswerTime": 0,
  "isFirstMessageWasFromOperator": true,
  "isOperatorAnswerWithoutClientQuestion": true,
  "isOperatorAskForRate": true,
  "averageHoldTime": 0,
  "duration": 0,
  "clientRealMessageCount": 0,
  "clientRealMessageCountForBot": 0,
  "operatorRealMessageCount": 0,
  "operatorRealMessageCountByBot": 0
}
```

## Оператор, участвовавший в диалоге (ChatOperatorDialogsReportOperator)

| Поле | Тип | Описание |
|---|---|---|
| `login` | string | Логин оператора |
| `statistic` | object | Статистика диалога<br>Структура: [Статистика диалога (ChatOperatorDialogsReportDialogStatistic)](11-models.md#статистика-диалога-chatoperatordialogsreportdialogstatistic) |

```json
{
  "login": "my_login",
  "statistic": {
    "firstClientOnlineMessageTime": 1790000000,
    "firstClientOfflineMessageTime": 1790000000,
    "firstOperatorMessageTime": 1790000000,
    "hasOnlineQuestion": true,
    "hasOnlineAnswer": true,
    "isAnsweredInTime": true,
    "hasOfflineQuestion": true,
    "hasOfflineAnswer": true,
    "hasForward": true,
    "hasAutoForward": true,
    "answerTime": 1790000000,
    "delayBetweenFirstAndSecondOperatorAnswer": 1790000000,
    "averageOnlineAnswerTime": 0,
    "averageOfflineAnswerTime": 0,
    "isFirstMessageWasFromOperator": true,
    "isOperatorAnswerWithoutClientQuestion": true,
    "isOperatorAskForRate": true,
    "averageHoldTime": 0,
    "duration": 0,
    "clientRealMessageCount": 0,
    "clientRealMessageCountForBot": 0,
    "operatorRealMessageCount": 0,
    "operatorRealMessageCountByBot": 0
  }
}
```

## Оператор (ChatGetOperatorsListOperator)

| Поле | Тип | Описание |
|---|---|---|
| `id` | string | Идентификатор<br>Пример: `"12fwaihos"` |
| `login` | string | Логин<br>Пример: `"my_operator"` |
| `name` | string | Имя (псевдоним, если он задан)<br>Пример: `"Ivan"` |
| `realName` | string | Основное имя из настроек оператора<br>Пример: `"Ivan"` |
| `avatar` | string | Ссылка на аватар<br>Пример: `"http://link-to-image"` |
| `statusId` | integer | Статус<br>`1` - В сети<br>`-1` - Невидимый<br>`0` - Отошёл |
| `isUnavailableBecauseOfLimits` | boolean | Оператор недоступен из-за ограничений лицензии |
| `isWorkingNow` | boolean | Сейчас рабочее время оператора |
| `isVisibleForClients` | boolean | Оператор видим для посетителей |
| `integrations` | array<object> | Список интеграций, где включен этот оператор |
| `integrations[].platformId` | string | Идентификатор платформы интеграции<br>Пример: `"telegram"` |
| `integrations[].authPrimaryId` | string | Идентификатор интеграции<br>Пример: `"de03131dcab80bafe15f07352a6697d0"` |
| `groups` | array<string> | id отделов, в которых состоит оператор |

```json
{
  "id": "12fwaihos",
  "login": "my_operator",
  "name": "Ivan",
  "realName": "Ivan",
  "avatar": "http://link-to-image",
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
```
