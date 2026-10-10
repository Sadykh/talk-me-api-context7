# Webhooks

Методы раздела `chat/webhook`: настройка серверов, на которые Talk-Me отправляет уведомления о событиях онлайн-чата.

Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: `{"success": true, "result": ...}`, ошибка: `{"success": false, "error": {"code", "descr"}}` (подробнее — [01-overview.md](01-overview.md)).

| Метод | Назначение |
|---|---|
| `/chat/webhook/get` | Получение списка серверов |
| `/chat/webhook/save` | Сохранение сервера |
| `/chat/webhook/delete` | Удаление сервера |

## POST /chat/webhook/get — Получение списка серверов

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatwebhook/paths/~1chat~1webhook~1get/post -->

Данный метод позволит получить список настроенных Webhook-ов

`POST https://lcab.talk-me.ru/json/v1.0/chat/webhook/get`

**Параметры запроса**

Метод не принимает параметров — передайте пустой JSON-объект `{}`.

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/webhook/get' \
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
      "id": "hdas872gasdf",
      "url": "https://mysite.com/webhook.php",
      "params": {
        "actions": {
          "dialogStarted": true,
          "dialogStatusUpdated": true,
          "dialogClosed": true,
          "dialogAiSummarize": true,
          "newMessageFromClient": true,
          "newMessageFromOperator": true,
          "editedMessageFromOperator": true,
          "audioAttachmentTranscribeInMessage": true,
          "messageReactionChanged": true,
          "newOfflineQuestion": true,
          "newRate": true,
          "operatorUpdatesClientInfo": true,
          "clientFieldsUpdated": true,
          "dialogUpdated": true,
          "autoAction": true,
          "newMessageStatus": true,
          "clientUnreadMessageCountChange": true,
          "operatorsStatusChange": true,
          "newAdditionalForm": true,
          "clientSkipMessageFromOperator": true,
          "operatorSkipMessageFromClient": true,
          "clientFillFormBeforeDialogStart": true,
          "clientFillFormAfterDialogStart": true,
          "onlineChatBot": true,
          "onlineChatBotStarted": true,
          "onlineChatBotStopped": true,
          "messageForCustomExternalBot": true,
          "newMessageForOfflineBot": true,
          "onlineChatClientBanned": true,
          "onlineChatClientUnbanned": true,
          "onlineChatMessageError": true,
          "onlineChatClientWasForwarded": true,
          "dialogRestarted": true,
          "newPayment": true,
          "knowledgeBaseArticleSaved": true
        }
      }
    }
  ]
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | array<object> | Список серверов |
| `result[].id` | string | Уникальный идентификатор<br>Пример: `"hdas872gasdf"` |
| `result[].url` | string | HTTP(S) адрес для получения уведомлений<br>Пример: `"https://mysite.com/webhook.php"` |
| `result[].secretKey` | string | Секретный ключ, который будет передаваться обратно в уведомлениях<br>Пример: `"foobar"` |
| `result[].params` | object | Параметры |
| `result[].params.actions` | object | Список событий |
| `result[].params.actions.dialogStarted` | boolean | Стартовал новый диалог |
| `result[].params.actions.dialogStatusUpdated` | boolean | Изменился статус диалога |
| `result[].params.actions.dialogClosed` | boolean | Диалог завершён |
| `result[].params.actions.dialogAiSummarize` | boolean | AI подвел итоги диалога |
| `result[].params.actions.newMessageFromClient` | boolean | Новое сообщение от клиента |
| `result[].params.actions.newMessageFromOperator` | boolean | Новое сообщение от оператора |
| `result[].params.actions.editedMessageFromOperator` | boolean | Отредактировано сообщение от оператора |
| `result[].params.actions.audioAttachmentTranscribeInMessage` | boolean | Завершена транскрибация аудио-вложения в сообщении |
| `result[].params.actions.messageReactionChanged` | boolean | Изменена реакция на сообщение |
| `result[].params.actions.newOfflineQuestion` | boolean | Новый оффлайн вопрос |
| `result[].params.actions.newRate` | boolean | Новый отзыв |
| `result[].params.actions.operatorUpdatesClientInfo` | boolean | Оператор обновил информацию клиента |
| `result[].params.actions.clientFieldsUpdated` | boolean | Обновилась информация клиента |
| `result[].params.actions.dialogUpdated` | boolean | Обновились параметры диалога |
| `result[].params.actions.autoAction` | boolean | Сработало автодействие «Отправить Webhook» |
| `result[].params.actions.newMessageStatus` | boolean | Изменился статус сообщения (доставлено\прочитано) |
| `result[].params.actions.clientUnreadMessageCountChange` | boolean | Изменился счетчик непрочитанных сообщений клиента |
| `result[].params.actions.operatorsStatusChange` | boolean | Изменился режим виджета (Online/Offline) |
| `result[].params.actions.newAdditionalForm` | boolean | Заполнена форма из дополнительной вкладки |
| `result[].params.actions.clientSkipMessageFromOperator` | boolean | Клиент с сайта не прочитал сообщение оператора за 10 минут |
| `result[].params.actions.operatorSkipMessageFromClient` | boolean | Оператор не ответил на сообщение клиента за допустимое время |
| `result[].params.actions.clientFillFormBeforeDialogStart` | boolean | Клиент заполнил форму перед началом диалога |
| `result[].params.actions.clientFillFormAfterDialogStart` | boolean | Клиент заполнил форму после начала диалога |
| `result[].params.actions.onlineChatBot` | boolean | Запуск бота |
| `result[].params.actions.onlineChatBotStarted` | boolean | Бот запущен |
| `result[].params.actions.onlineChatBotStopped` | boolean | Бот остановлен |
| `result[].params.actions.messageForCustomExternalBot` | boolean | Сообщение для своего стороннего бота |
| `result[].params.actions.newMessageForOfflineBot` | boolean | Новое сообщение для Offline-бота |
| `result[].params.actions.onlineChatClientBanned` | boolean | Клиент заблокирован |
| `result[].params.actions.onlineChatClientUnbanned` | boolean | Клиент разблокирован |
| `result[].params.actions.onlineChatMessageError` | boolean | Ошибка отправки сообщения |
| `result[].params.actions.onlineChatClientWasForwarded` | boolean | Клиент переключен на другого оператора |
| `result[].params.actions.dialogRestarted` | boolean | Диалог был перезапущен в соответствии с настройками в разделе "Диалоги" |
| `result[].params.actions.newPayment` | boolean | Новая оплата в дополнительной форме |
| `result[].params.actions.knowledgeBaseArticleSaved` | boolean | Сохранена статья в базе знаний |

## POST /chat/webhook/save — Сохранение сервера

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatwebhook/paths/~1chat~1webhook~1save/post -->

Данный метод позволит сохранить сервер для Webhook

`POST https://lcab.talk-me.ru/json/v1.0/chat/webhook/save`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `id` | string |  | Уникальный идентификатор<br>Пример: `"hdas872gasdf"` |
| `url` | string | да | HTTP(S) адрес для получения уведомлений<br>Пример: `"https://mysite.com/webhook.php"` |
| `secretKey` | string |  | Секретный ключ, который будет передаваться обратно в уведомлениях<br>Пример: `"foobar"` |
| `params` | object | да | Параметры |
| `params.actions` | object | да | Список событий |
| `params.actions.dialogStarted` | boolean |  | Стартовал новый диалог |
| `params.actions.dialogStatusUpdated` | boolean |  | Изменился статус диалога |
| `params.actions.dialogClosed` | boolean |  | Диалог завершён |
| `params.actions.dialogAiSummarize` | boolean |  | AI подвел итоги диалога |
| `params.actions.newMessageFromClient` | boolean |  | Новое сообщение от клиента |
| `params.actions.newMessageFromOperator` | boolean |  | Новое сообщение от оператора |
| `params.actions.editedMessageFromOperator` | boolean |  | Отредактировано сообщение от оператора |
| `params.actions.audioAttachmentTranscribeInMessage` | boolean |  | Завершена транскрибация аудио-вложения в сообщении |
| `params.actions.messageReactionChanged` | boolean |  | Изменена реакция на сообщение |
| `params.actions.newOfflineQuestion` | boolean |  | Новый оффлайн вопрос |
| `params.actions.newRate` | boolean |  | Новый отзыв |
| `params.actions.operatorUpdatesClientInfo` | boolean |  | Оператор обновил информацию клиента |
| `params.actions.clientFieldsUpdated` | boolean |  | Обновилась информация клиента |
| `params.actions.dialogUpdated` | boolean |  | Обновились параметры диалога |
| `params.actions.autoAction` | boolean |  | Сработало автодействие «Отправить Webhook» |
| `params.actions.newMessageStatus` | boolean |  | Изменился статус сообщения (доставлено\прочитано) |
| `params.actions.clientUnreadMessageCountChange` | boolean |  | Изменился счетчик непрочитанных сообщений клиента |
| `params.actions.operatorsStatusChange` | boolean |  | Изменился режим виджета (Online/Offline) |
| `params.actions.newAdditionalForm` | boolean |  | Заполнена форма из дополнительной вкладки |
| `params.actions.clientSkipMessageFromOperator` | boolean |  | Клиент с сайта не прочитал сообщение оператора за 10 минут |
| `params.actions.operatorSkipMessageFromClient` | boolean |  | Оператор не ответил на сообщение клиента за допустимое время |
| `params.actions.clientFillFormBeforeDialogStart` | boolean |  | Клиент заполнил форму перед началом диалога |
| `params.actions.clientFillFormAfterDialogStart` | boolean |  | Клиент заполнил форму после начала диалога |
| `params.actions.onlineChatBot` | boolean |  | Запуск бота |
| `params.actions.onlineChatBotStarted` | boolean |  | Бот запущен |
| `params.actions.onlineChatBotStopped` | boolean |  | Бот остановлен |
| `params.actions.messageForCustomExternalBot` | boolean |  | Сообщение для своего стороннего бота |
| `params.actions.newMessageForOfflineBot` | boolean |  | Новое сообщение для Offline-бота |
| `params.actions.onlineChatClientBanned` | boolean |  | Клиент заблокирован |
| `params.actions.onlineChatClientUnbanned` | boolean |  | Клиент разблокирован |
| `params.actions.onlineChatMessageError` | boolean |  | Ошибка отправки сообщения |
| `params.actions.onlineChatClientWasForwarded` | boolean |  | Клиент переключен на другого оператора |
| `params.actions.dialogRestarted` | boolean |  | Диалог был перезапущен в соответствии с настройками в разделе "Диалоги" |
| `params.actions.newPayment` | boolean |  | Новая оплата в дополнительной форме |
| `params.actions.knowledgeBaseArticleSaved` | boolean |  | Сохранена статья в базе знаний |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/webhook/save' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "hdas872gasdf",
  "url": "https://mysite.com/webhook.php",
  "secretKey": "foobar",
  "params": {
    "actions": {}
  }
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
| `result` | object | Результат работы метода (ChatSaveWebhookResult) |
| `result.id` | string | Уникальный идентификатор |

## POST /chat/webhook/delete — Удаление сервера

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/Chatwebhook/paths/~1chat~1webhook~1delete/post -->

Данный метод позволит удалить сервер для Webhook

`POST https://lcab.talk-me.ru/json/v1.0/chat/webhook/delete`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `id` | string | да | Идентификатор<br>Пример: `"qjas89912121eddsas"` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/webhook/delete' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "qjas89912121eddsas"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```
