# Отчёты

Методы раздела `chat/report`: выгрузка диалогов с метриками операторов и отчёт по заполненным формам.

Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: `{"success": true, "result": ...}`, ошибка: `{"success": false, "error": {"code", "descr"}}` (подробнее — [01-overview.md](01-overview.md)).

| Метод | Назначение |
|---|---|
| `/chat/report/operatorDialogs` | Отчёт по операторам |
| `/chat/report/operators` | Отчёт по операторам (устарел) |
| `/chat/report/forms` | Отчёт по заполненным формам |

## POST /chat/report/operatorDialogs — Отчёт по операторам

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatreport/paths/~1chat~1report~1operatorDialogs/post -->

Отчёт по операторам.

`POST https://lcab.talk-me.ru/json/v1.0/chat/report/operatorDialogs`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `dateTimeRange` | object | да | Период отчёта (максимум 31 дней) |
| `dateTimeRange.start` | string | да | Начало диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-01 00:00:00"` |
| `dateTimeRange.stop` | string | да | Конец диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-07 23:59:59"` |
| `dateTimeType` | string |  | Тип даты для периода отчёта<br>`start` - дата начала диалога<br>`close` - дата последнего сообщения завершённого диалога<br>`closeStatusUpdate` - дата завершения диалога<br>Значения: `start`, `close`, `closeStatusUpdate`<br>По умолчанию: `"start"` |
| `sourceIds` | array<string> |  | Идентификаторы каналов<br>Расшифровка значений: [Идентификаторы каналов](12-dictionaries.md#идентификаторы-каналов) |
| `withClients` | boolean |  | Выгружать ли данные клиентов<br>По умолчанию: `false` |
| `withMessages` | boolean |  | Выгружать ли сообщения<br>По умолчанию: `false` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/report/operatorDialogs' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "dateTimeRange": {
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
    "dialogs": [
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
    ],
    "aggregatedStatistic": {
      "allOperators": {
        "uniqueClientsCount": 0,
        "clientMessageCount": 0,
        "operatorMessageCount": 0,
        "averageOnlineAnswerTime": 0,
        "averageOfflineAnswerTime": 0,
        "averageFirstAnswerTime": 0,
        "averageDialogDuration": 0,
        "onlineTime": 0,
        "invisibleTime": 0,
        "awayTime": 0,
        "answeredCount": 0,
        "notAnsweredCount": 0,
        "answeredInTimeCount": 0,
        "answeredNotInTimeCount": 0,
        "offlineQuestionAnswerCount": 0
      },
      "byOperators": [
        {
          "login": "my_login",
          "statistic": {
            "uniqueClientsCount": 0,
            "clientMessageCount": 0,
            "operatorMessageCount": 0,
            "averageOnlineAnswerTime": 0,
            "averageOfflineAnswerTime": 0,
            "averageFirstAnswerTime": 0,
            "averageDialogDuration": 0,
            "onlineTime": 0,
            "invisibleTime": 0,
            "awayTime": 0,
            "answeredCount": 0,
            "notAnsweredCount": 0,
            "answeredInTimeCount": 0,
            "answeredNotInTimeCount": 0,
            "offlineQuestionAnswerCount": 0
          }
        }
      ]
    }
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (OperatorDialogsReportResult) |
| `result.dialogs` | array<object> | Диалоги<br>Структура: [Диалог (ChatOperatorDialogsReportDialog)](11-models.md#диалог-chatoperatordialogsreportdialog) |
| `result.aggregatedStatistic` | object | Агрегированная статистика по операторам |
| `result.aggregatedStatistic.allOperators` | object | Статистика по оператору |
| `result.aggregatedStatistic.allOperators.uniqueClientsCount` | integer | Количество уникальных клиентов |
| `result.aggregatedStatistic.allOperators.clientMessageCount` | integer | Количество сообщений клиентов |
| `result.aggregatedStatistic.allOperators.operatorMessageCount` | integer | Количество сообщений операторов |
| `result.aggregatedStatistic.allOperators.averageOnlineAnswerTime` | integer | Среднее время ответа на все online-сообщения в секундах |
| `result.aggregatedStatistic.allOperators.averageOfflineAnswerTime` | integer | Среднее время ответа на все offline-сообщения в секундах |
| `result.aggregatedStatistic.allOperators.averageFirstAnswerTime` | integer | Среднее время ответа на первое сообщение в секундах |
| `result.aggregatedStatistic.allOperators.averageDialogDuration` | integer | Среднее время продолжительности диалога |
| `result.aggregatedStatistic.allOperators.onlineTime` | integer | Время в статусе "В сети" (в секундах) |
| `result.aggregatedStatistic.allOperators.invisibleTime` | integer | Время в статусе "Невидимый" (в секундах) |
| `result.aggregatedStatistic.allOperators.awayTime` | integer | Время в статусе "Отошёл" (в секундах) |
| `result.aggregatedStatistic.allOperators.answeredCount` | integer | Количество отвеченных диалогов |
| `result.aggregatedStatistic.allOperators.notAnsweredCount` | integer | Количество пропущенных диалогов |
| `result.aggregatedStatistic.allOperators.answeredInTimeCount` | integer | Количество диалогов, с ответом данным вовремя |
| `result.aggregatedStatistic.allOperators.answeredNotInTimeCount` | integer | Количество диалогов, с ответом данным не вовремя |
| `result.aggregatedStatistic.allOperators.offlineQuestionAnswerCount` | integer | Количество ответов на Offline вопросы |
| `result.aggregatedStatistic.byOperators` | array<object> | Агрегированная статистика по конкретным операторам |
| `result.aggregatedStatistic.byOperators[].login` | string | Логин оператора |
| `result.aggregatedStatistic.byOperators[].statistic` | object | Статистика по оператору |
| `result.aggregatedStatistic.byOperators[].statistic.uniqueClientsCount` | integer | Количество уникальных клиентов |
| `result.aggregatedStatistic.byOperators[].statistic.clientMessageCount` | integer | Количество сообщений клиентов |
| `result.aggregatedStatistic.byOperators[].statistic.operatorMessageCount` | integer | Количество сообщений операторов |
| `result.aggregatedStatistic.byOperators[].statistic.averageOnlineAnswerTime` | integer | Среднее время ответа на все online-сообщения в секундах |
| `result.aggregatedStatistic.byOperators[].statistic.averageOfflineAnswerTime` | integer | Среднее время ответа на все offline-сообщения в секундах |
| `result.aggregatedStatistic.byOperators[].statistic.averageFirstAnswerTime` | integer | Среднее время ответа на первое сообщение в секундах |
| `result.aggregatedStatistic.byOperators[].statistic.averageDialogDuration` | integer | Среднее время продолжительности диалога |
| `result.aggregatedStatistic.byOperators[].statistic.onlineTime` | integer | Время в статусе "В сети" (в секундах) |
| `result.aggregatedStatistic.byOperators[].statistic.invisibleTime` | integer | Время в статусе "Невидимый" (в секундах) |
| `result.aggregatedStatistic.byOperators[].statistic.awayTime` | integer | Время в статусе "Отошёл" (в секундах) |
| `result.aggregatedStatistic.byOperators[].statistic.answeredCount` | integer | Количество отвеченных диалогов |
| `result.aggregatedStatistic.byOperators[].statistic.notAnsweredCount` | integer | Количество пропущенных диалогов |
| `result.aggregatedStatistic.byOperators[].statistic.answeredInTimeCount` | integer | Количество диалогов, с ответом данным вовремя |
| `result.aggregatedStatistic.byOperators[].statistic.answeredNotInTimeCount` | integer | Количество диалогов, с ответом данным не вовремя |
| `result.aggregatedStatistic.byOperators[].statistic.offlineQuestionAnswerCount` | integer | Количество ответов на Offline вопросы |

## POST /chat/report/operators — Отчёт по операторам

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatreport/paths/~1chat~1report~1operators/post -->

> **Устаревший метод.** Сохраняется для совместимости; в новых интеграциях используйте `/chat/report/operatorDialogs`.

Отчёт по операторам.

`POST https://lcab.talk-me.ru/json/v1.0/chat/report/operators`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `dateTimeRange` | object | да | Период отчёта (максимум 31 дней) |
| `dateTimeRange.start` | string | да | Начало диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-01 00:00:00"` |
| `dateTimeRange.stop` | string | да | Конец диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-07 23:59:59"` |
| `sourceIds` | array<string> |  | Идентификаторы каналов<br>Расшифровка значений: [Идентификаторы каналов](12-dictionaries.md#идентификаторы-каналов) |
| `withClients` | boolean |  | Выгружать ли данные клиентов<br>По умолчанию: `false` |
| `wasConversationWithOperator` | boolean |  | Фильтр: Было общение с оператором |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/report/operators' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "dateTimeRange": {
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
    "all": {
      "dialogs": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "dialogsWithOffline": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "allDialogs": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "uniqueClientsCount": 0,
      "clientMessageCount": 0,
      "operatorMessageCount": 0,
      "answeredDialogs": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "answeredInTimeDialogs": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "answeredNotInTimeDialogs": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "dialogsWithSimulation": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "forward": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "autoForward": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "notAnsweredDialogs": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "averageAnswerTime": 0,
      "averageFirstAnswerTime": 0,
      "answersOnOfflineQuestions": [
        {
          "dialogId": 0,
          "startTime": 1790000000,
          "operatorLogins": [
            "string"
          ]
        }
      ],
      "onlineTime": 0,
      "invisibleTime": 0,
      "awayTime": 0
    }
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (OperatorsReportResult) |
| `result.all` | object | Элемент отчета по операторам |
| `result.all.dialogs` | array<object> | Диалоги, в которых было Online общение |
| `result.all.dialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.dialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.dialogs[].dialogId` | integer | id диалога |
| `result.all.dialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.dialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.dialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.dialogs[].questionCategory` | string | Категория вопроса |
| `result.all.dialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.dialogsWithOffline` | array<object> | Диалоги, в которых был Offline вопрос |
| `result.all.dialogsWithOffline[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.dialogsWithOffline[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.dialogsWithOffline[].dialogId` | integer | id диалога |
| `result.all.dialogsWithOffline[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.dialogsWithOffline[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.dialogsWithOffline[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.dialogsWithOffline[].questionCategory` | string | Категория вопроса |
| `result.all.dialogsWithOffline[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.allDialogs` | array<object> | Все диалоги |
| `result.all.allDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.allDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.allDialogs[].dialogId` | integer | id диалога |
| `result.all.allDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.allDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.allDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.allDialogs[].questionCategory` | string | Категория вопроса |
| `result.all.allDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.uniqueClientsCount` | integer | Количество уникальных клиентов |
| `result.all.clientMessageCount` | integer | Количество сообщений клиентов |
| `result.all.operatorMessageCount` | integer | Количество сообщений операторов |
| `result.all.answeredDialogs` | array<object> | Отвеченные диалоги |
| `result.all.answeredDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.answeredDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.answeredDialogs[].dialogId` | integer | id диалога |
| `result.all.answeredDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.answeredDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.answeredDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.answeredDialogs[].questionCategory` | string | Категория вопроса |
| `result.all.answeredDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.answeredInTimeDialogs` | array<object> | Отвеченные вовремя диалоги |
| `result.all.answeredInTimeDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.answeredInTimeDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.answeredInTimeDialogs[].dialogId` | integer | id диалога |
| `result.all.answeredInTimeDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.answeredInTimeDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.answeredInTimeDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.answeredInTimeDialogs[].questionCategory` | string | Категория вопроса |
| `result.all.answeredInTimeDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.answeredNotInTimeDialogs` | array<object> | Отвеченные не вовремя диалоги |
| `result.all.answeredNotInTimeDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.answeredNotInTimeDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.answeredNotInTimeDialogs[].dialogId` | integer | id диалога |
| `result.all.answeredNotInTimeDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.answeredNotInTimeDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.answeredNotInTimeDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.answeredNotInTimeDialogs[].questionCategory` | string | Категория вопроса |
| `result.all.answeredNotInTimeDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.dialogsWithSimulation` | array<object> | Диалоги, в которых была имитация общения |
| `result.all.dialogsWithSimulation[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.dialogsWithSimulation[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.dialogsWithSimulation[].dialogId` | integer | id диалога |
| `result.all.dialogsWithSimulation[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.dialogsWithSimulation[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.dialogsWithSimulation[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.dialogsWithSimulation[].questionCategory` | string | Категория вопроса |
| `result.all.dialogsWithSimulation[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.forward` | array<object> | Диалоги, в которых было ручное переключение на другого оператора |
| `result.all.forward[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.forward[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.forward[].dialogId` | integer | id диалога |
| `result.all.forward[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.forward[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.forward[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.forward[].questionCategory` | string | Категория вопроса |
| `result.all.forward[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.autoForward` | array<object> | Диалоги, в которых было автоматическое переключение на другого оператора |
| `result.all.autoForward[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.autoForward[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.autoForward[].dialogId` | integer | id диалога |
| `result.all.autoForward[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.autoForward[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.autoForward[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.autoForward[].questionCategory` | string | Категория вопроса |
| `result.all.autoForward[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.notAnsweredDialogs` | array<object> | Диалоги без ответа |
| `result.all.notAnsweredDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.notAnsweredDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.notAnsweredDialogs[].dialogId` | integer | id диалога |
| `result.all.notAnsweredDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.notAnsweredDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.notAnsweredDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.notAnsweredDialogs[].questionCategory` | string | Категория вопроса |
| `result.all.notAnsweredDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.averageAnswerTime` | integer | Среднее время ответа на все сообщения в секундах |
| `result.all.averageFirstAnswerTime` | integer | Среднее время ответа на первое сообщение в секундах |
| `result.all.answersOnOfflineQuestions` | array<object> | Диалоги, в которых были ответы на оффлайн вопрос |
| `result.all.answersOnOfflineQuestions[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.all.answersOnOfflineQuestions[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.all.answersOnOfflineQuestions[].dialogId` | integer | id диалога |
| `result.all.answersOnOfflineQuestions[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.all.answersOnOfflineQuestions[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.all.answersOnOfflineQuestions[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.all.answersOnOfflineQuestions[].questionCategory` | string | Категория вопроса |
| `result.all.answersOnOfflineQuestions[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.all.onlineTime` | integer | Время в статусе "В сети" (в секундах) |
| `result.all.invisibleTime` | integer | Время в статусе "Невидимый" (в секундах) |
| `result.all.awayTime` | integer | Время в статусе "Отошёл" (в секундах) |
| `result.operators` | object | Операторы |
| `result.operators.{key}` | object | Элемент отчета по операторам |
| `result.operators.{key}.dialogs` | array<object> | Диалоги, в которых было Online общение |
| `result.operators.{key}.dialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.dialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.dialogs[].dialogId` | integer | id диалога |
| `result.operators.{key}.dialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.dialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.dialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.dialogs[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.dialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.dialogsWithOffline` | array<object> | Диалоги, в которых был Offline вопрос |
| `result.operators.{key}.dialogsWithOffline[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.dialogsWithOffline[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.dialogsWithOffline[].dialogId` | integer | id диалога |
| `result.operators.{key}.dialogsWithOffline[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.dialogsWithOffline[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.dialogsWithOffline[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.dialogsWithOffline[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.dialogsWithOffline[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.allDialogs` | array<object> | Все диалоги |
| `result.operators.{key}.allDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.allDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.allDialogs[].dialogId` | integer | id диалога |
| `result.operators.{key}.allDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.allDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.allDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.allDialogs[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.allDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.uniqueClientsCount` | integer | Количество уникальных клиентов |
| `result.operators.{key}.clientMessageCount` | integer | Количество сообщений клиентов |
| `result.operators.{key}.operatorMessageCount` | integer | Количество сообщений операторов |
| `result.operators.{key}.answeredDialogs` | array<object> | Отвеченные диалоги |
| `result.operators.{key}.answeredDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.answeredDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.answeredDialogs[].dialogId` | integer | id диалога |
| `result.operators.{key}.answeredDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.answeredDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.answeredDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.answeredDialogs[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.answeredDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.answeredInTimeDialogs` | array<object> | Отвеченные вовремя диалоги |
| `result.operators.{key}.answeredInTimeDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.answeredInTimeDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.answeredInTimeDialogs[].dialogId` | integer | id диалога |
| `result.operators.{key}.answeredInTimeDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.answeredInTimeDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.answeredInTimeDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.answeredInTimeDialogs[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.answeredInTimeDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.answeredNotInTimeDialogs` | array<object> | Отвеченные не вовремя диалоги |
| `result.operators.{key}.answeredNotInTimeDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.answeredNotInTimeDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.answeredNotInTimeDialogs[].dialogId` | integer | id диалога |
| `result.operators.{key}.answeredNotInTimeDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.answeredNotInTimeDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.answeredNotInTimeDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.answeredNotInTimeDialogs[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.answeredNotInTimeDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.dialogsWithSimulation` | array<object> | Диалоги, в которых была имитация общения |
| `result.operators.{key}.dialogsWithSimulation[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.dialogsWithSimulation[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.dialogsWithSimulation[].dialogId` | integer | id диалога |
| `result.operators.{key}.dialogsWithSimulation[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.dialogsWithSimulation[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.dialogsWithSimulation[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.dialogsWithSimulation[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.dialogsWithSimulation[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.forward` | array<object> | Диалоги, в которых было ручное переключение на другого оператора |
| `result.operators.{key}.forward[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.forward[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.forward[].dialogId` | integer | id диалога |
| `result.operators.{key}.forward[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.forward[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.forward[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.forward[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.forward[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.autoForward` | array<object> | Диалоги, в которых было автоматическое переключение на другого оператора |
| `result.operators.{key}.autoForward[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.autoForward[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.autoForward[].dialogId` | integer | id диалога |
| `result.operators.{key}.autoForward[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.autoForward[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.autoForward[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.autoForward[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.autoForward[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.notAnsweredDialogs` | array<object> | Диалоги без ответа |
| `result.operators.{key}.notAnsweredDialogs[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.notAnsweredDialogs[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.notAnsweredDialogs[].dialogId` | integer | id диалога |
| `result.operators.{key}.notAnsweredDialogs[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.notAnsweredDialogs[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.notAnsweredDialogs[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.notAnsweredDialogs[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.notAnsweredDialogs[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.averageAnswerTime` | integer | Среднее время ответа на все сообщения в секундах |
| `result.operators.{key}.averageFirstAnswerTime` | integer | Среднее время ответа на первое сообщение в секундах |
| `result.operators.{key}.answersOnOfflineQuestions` | array<object> | Диалоги, в которых были ответы на оффлайн вопрос |
| `result.operators.{key}.answersOnOfflineQuestions[].clientId` | string | id посетителя из Cookies<br>Если null, то клиент уже удален из базы |
| `result.operators.{key}.answersOnOfflineQuestions[].client` | object | Клиент<br>Структура: [Клиент (ChatClient)](11-models.md#клиент-chatclient) |
| `result.operators.{key}.answersOnOfflineQuestions[].dialogId` | integer | id диалога |
| `result.operators.{key}.answersOnOfflineQuestions[].startTime` | integer | Время начала диалога<br>Пример: `1790000000` |
| `result.operators.{key}.answersOnOfflineQuestions[].closeTime` | integer | Время завершения диалога<br>Пример: `1790000000` |
| `result.operators.{key}.answersOnOfflineQuestions[].answerTime` | integer | Время, затраченное на ответ (в секундах)<br>Пример: `1790000000` |
| `result.operators.{key}.answersOnOfflineQuestions[].questionCategory` | string | Категория вопроса |
| `result.operators.{key}.answersOnOfflineQuestions[].operatorLogins` | array<string> | Логины операторов, участвовавших в диалоге |
| `result.operators.{key}.onlineTime` | integer | Время в статусе "В сети" (в секундах) |
| `result.operators.{key}.invisibleTime` | integer | Время в статусе "Невидимый" (в секундах) |
| `result.operators.{key}.awayTime` | integer | Время в статусе "Отошёл" (в секундах) |

## POST /chat/report/forms — Отчёт по заполненным формам

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatreport/paths/~1chat~1report~1forms/post -->

Отчёт по заполненным формам.

`POST https://lcab.talk-me.ru/json/v1.0/chat/report/forms`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `dateTimeRange` | object | да | Период отчёта (максимум 31 дней) |
| `dateTimeRange.start` | string | да | Начало диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-01 00:00:00"` |
| `dateTimeRange.stop` | string | да | Конец диапазона<br>Формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD<br>Пример: `"2026-10-07 23:59:59"` |
| `withClients` | boolean |  | Выгружать ли данные клиентов<br>По умолчанию: `false` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/report/forms' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "dateTimeRange": {
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
    "forms": [
      {
        "dateTime": 1790000000,
        "username": "string",
        "clientDescr": "string",
        "form": {
          "typeId": "string"
        },
        "values": [
          {
            "fieldName": "string",
            "fieldDescr": "string",
            "value": "string"
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
| `result` | object | Результат работы метода (ChatFormReportResult) |
| `result.forms` | array<object> | Заполненные формы |
| `result.forms[].dateTime` | integer | Дата заполнения формы<br>Пример: `1790000000` |
| `result.forms[].client` | object | Клиент<br>Если `null`, то клиент уже удален из базы. Выгружается только если передано `withClients` = `true` |
| `result.forms[].client.searchId` | integer | Уникальный идентификатор посетителя для поиска<br>Пример: `1234` |
| `result.forms[].client.login` | string | Уникальный логин посетителя (используется в Jabber)<br>Пример: `"123_user_at_june"` |
| `result.forms[].client.clientId` | string | Идентификатор из Cookie посетителя<br>Пример: `"123e2rwfjas"` |
| `result.forms[].client.name` | string | ФИО или стандартное имя посетителя<br>Пример: `"Ivan"` |
| `result.forms[].client.lastName` | string | Фамилия<br>Пример: `"Иванов"` |
| `result.forms[].client.firstName` | string | Имя<br>Пример: `"Иван"` |
| `result.forms[].client.secondName` | string | Отчество<br>Пример: `"Иванович"` |
| `result.forms[].client.phone` | string | Номер телефона<br>Пример: `"790012345678"` |
| `result.forms[].client.email` | string | Email<br>Пример: `"example@gmail.com"` |
| `result.forms[].client.country` | string | Страна<br>Пример: `"Russia"` |
| `result.forms[].client.city` | string | Город<br>Пример: `"Moscow"` |
| `result.forms[].client.firstVisit` | object | Первый визит |
| `result.forms[].client.firstVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.forms[].client.firstVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.forms[].client.firstVisit.page` | object | Страница |
| `result.forms[].client.firstVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result.forms[].client.firstVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result.forms[].client.lastVisit` | object | Последний визит |
| `result.forms[].client.lastVisit.dateTime` | string | Дата начала визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.forms[].client.lastVisit.dateTimeUTC` | string | Дата начала визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.forms[].client.lastVisit.lastDateTime` | string | Дата окончания визита<br>Пример: `"2026-10-01 12:00:00"` |
| `result.forms[].client.lastVisit.lastDateTimeUTC` | string | Дата окончания визита (UTC)<br>Пример: `"2026-10-01 12:00:00"` |
| `result.forms[].client.lastVisit.page` | object | Страница |
| `result.forms[].client.lastVisit.page.url` | string | Адрес страницы<br>Пример: `"http://example.com"` |
| `result.forms[].client.lastVisit.page.title` | string | Заголовок страницы<br>Пример: `"Example.com - Homepage"` |
| `result.forms[].client.ip` | string | IP-адрес<br>Пример: `"85.123.22.41"` |
| `result.forms[].client.flag` | string | Флаг<br>Значения: `red`, `orange`, `green`, `blue`, `purple`, `yellow`, `asphalt` |
| `result.forms[].client.useragent` | string | Useragent браузера<br>Пример: `"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54"` |
| `result.forms[].client.target` | array<string> | Целевой посетитель |
| `result.forms[].client.isBanned` | boolean | Пользователь заблокирован |
| `result.forms[].client.questionCategory` | string | Категория вопроса<br>Пример: `"Common questions"` |
| `result.forms[].client.referer` | string | Источник перехода<br>Пример: `"https://google.com"` |
| `result.forms[].client.searchKeyword` | string | Поисковый запрос<br>Пример: `"home flowers"` |
| `result.forms[].client.visitsCount` | integer | Количество визитов<br>Пример: `3` |
| `result.forms[].client.isOnline` | boolean | Посетитель в сети |
| `result.forms[].client.source` | object | Источник диалога |
| `result.forms[].client.source.type` | object | Тип источника |
| `result.forms[].client.source.type.id` | string | Идентификатор<br>Пример: `"vk"` |
| `result.forms[].client.source.type.name` | string | Название<br>Пример: `"VKontakte"` |
| `result.forms[].client.source.id` | string | ID источника диалога<br>Пример: `"ab4-3fddd45-24dss"` |
| `result.forms[].client.source.name` | string | Название источника диалога<br>Пример: `"Название сообщества"` |
| `result.forms[].client.source.link` | string | Ссылка на источник диалога<br>Пример: `"https://vk.com/club0000123"` |
| `result.forms[].client.source.data` | object | Другие данные об источнике |
| `result.forms[].client.customData` | object | Другие данные об посетителе |
| `result.forms[].client.utm` | object | UTM-метки |
| `result.forms[].client.utm.utm_source` | string |  |
| `result.forms[].client.utm.utm_medium` | string |  |
| `result.forms[].client.utm.utm_campaign` | string |  |
| `result.forms[].client.utm.utm_term` | string |  |
| `result.forms[].client.utm.utm_content` | string |  |
| `result.forms[].client.utm.utm_referrer` | string |  |
| `result.forms[].client.tags` | array<string> | Тэги клиента |
| `result.forms[].client.applicationLink` | string | Ссылка на приложение оператора для открытия диалога |
| `result.forms[].client.infoLink` | string | Ссылка на информацию о клиенте |
| `result.forms[].client.roistatVisitId` | string | Значение Cookie roistat_visit<br>Пример: `"1000001"` |
| `result.forms[].client.yandexMetrika` | object | Данные Яндекс.Метрики |
| `result.forms[].client.yandexMetrika.clientId` | string | clientId из Яндекс.Метрики<br>Пример: `"abcdef"` |
| `result.forms[].client.googleAnalytics` | object | Данные Google Analytics |
| `result.forms[].client.googleAnalytics.trackingId` | string | trackingId из Google Analytics<br>Пример: `"abcdef"` |
| `result.forms[].client.googleAnalytics.clientId` | string | clientId из Google Analytics<br>Пример: `"abcdef"` |
| `result.forms[].username` | string | username клиента |
| `result.forms[].clientDescr` | string | Имя клиента на момент заполнения формы |
| `result.forms[].form` | object | Форма |
| `result.forms[].form.typeId` | string | Тип формы |
| `result.forms[].form.id` | string | id формы |
| `result.forms[].form.descr` | string | Название формы |
| `result.forms[].values` | array<object> | Заполненные значения |
| `result.forms[].values[].fieldName` | string | Системное название поля |
| `result.forms[].values[].fieldDescr` | string | Название поля |
| `result.forms[].values[].value` | string | Значение поля |
