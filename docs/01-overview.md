# Talk-Me Online Chat REST API — общая информация

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#section/Vvedenie -->

REST API онлайн-чата Talk-Me (версия `v1.0`) позволяет из внешней системы (CRM, бэкенда сайта, бота) читать переписку, отправлять сообщения клиентам и операторам, начинать чаты в мессенджерах, управлять операторами, посетителями, ботами, webhook-уведомлениями, лицензиями и базой знаний, а также выгружать отчёты.

API описано в формате OpenAPI 3.0, поэтому клиент можно сгенерировать автоматически (например, `openapi-generator`) из спецификации:
`https://lcab.talk-me.ru/cabinet/json-doc/cabinetRestApi/v1.0/online/specification.json`.

## Базовый URL и формат запросов

- Каждый URL начинается с `https://lcab.talk-me.ru/json/v1.0`, например `https://lcab.talk-me.ru/json/v1.0/chat/message/sendToClient`.
- Все методы вызываются только методом `POST`.
- Обязательный заголовок `Content-Type: application/json`; тело — JSON по схеме метода, кодировка `utf-8`.
- Методы без параметров (`chat/message/getStartChatChannels`, `chat/message/getDialogStatusList`, `chat/client/onlineCount`, `chat/webhook/get`, `chat/license/get`, `chat/knowledgeBase/getKnowledgeBaseList`) вызываются с пустым объектом `{}`.

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/operator/getList' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

## Авторизация (X-Token)

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#section/Avtorizaciya -->

Каждый запрос должен содержать заголовок `X-Token` с API-токеном, выданным в личном кабинете Talk-Me. Если токен не передан или неверен, сервер отвечает HTTP **401**.

```http
POST /json/v1.0/chat/operator/getList HTTP/1.1
Host: lcab.talk-me.ru
X-Token: abcde12345
Content-Type: application/json

{}
```

Методы загрузки файлов (вложения сообщений) относятся к отдельному API файлового хранилища и вызываются с **токеном от API личного кабинета**, а не с токеном онлайн-чата. Документация: https://lcab.talk-me.ru/cabinet/json-doc/fileshare#tag/Fileshareupload. Полученные идентификаторы файлов передаются в `message.attachments` методов `chat/message/sendToClient` и `chat/message/sendToOperator`.

## Формат ответа

Если запрос понят и обработан, сервер возвращает HTTP **200** и JSON-конверт. Успех определяется полем `success`, а не HTTP-статусом.

Успешный ответ (`result` у каждого метода свой):

```json
{
  "success": true,
  "result": {}
}
```

Ошибка бизнес-логики (HTTP 200):

```json
{
  "success": false,
  "error": {
    "code": 123,
    "descr": "Описание ошибки"
  }
}
```

Объект `error` присутствует только при `success == false`.

## HTTP-статусы и ошибки

| Статус | Значение |
|---|---|
| `200` | Запрос обработан; смотрите поле `success` |
| `400` | Ошибка валидации входящего JSON |
| `401` | Ошибка авторизации: передан неверный `X-Token` или он отсутствует |
| `500` | Непредвиденная ошибка на сервере |

При статусах 4xx и 5xx тело имеет тот же формат, а `error.code` равен HTTP-коду:

```json
{
  "success": false,
  "error": {
    "code": 400,
    "descr": "Ошибка валидации входящего JSON"
  }
}
```

## Версионирование

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#section/Versionirovanie-API -->

Номер версии в URI (`v1.0`) меняется только при добавлении несовместимого функционала. В рамках одной версии API может получать новые методы и новые необязательные параметры, поэтому клиент должен игнорировать неизвестные поля в ответах.

## Общие соглашения

- **Даты в запросах** — строки `YYYY-MM-DD HH:MM:SS` или `YYYY-MM-DD`. По умолчанию время считается московским; передайте `isLocal: true` в объекте периода, чтобы время трактовалось в часовом поясе проекта.
- **Даты в ответах** — `YYYY-MM-DD HH:MM:SS`; у сообщений есть `dateTime`, `dateTimeOrganization` и `dateTimeUTC`.
- **Ограничения периода**: `chat/message/getList` — не более 14 дней (`dateRange`); `chat/report/operatorDialogs`, `chat/report/operators`, `chat/report/forms` — не более 31 дня (`dateTimeRange`); `chat/client/getList` — не более 7 дней (`lastActivityDateTimeRange`).
- **Пагинация** — параметры `page` (с 0) и `limit` (по умолчанию 30, максимум 500); в ответе возвращаются `page`, `limit` и данные страницы.
- **Идентификация посетителя**: `clientId` (или `id`) — идентификатор из Cookies виджета; `searchId` — числовой идентификатор посетителя в Talk-Me. В большинстве методов достаточно одного из них.
- **Оператор** указывается логином (`login`, `operatorLogin`). Флаг `virtual: true` отключает проверку существования логина (сообщение от «виртуального» оператора).
- **Каналы** (мессенджеры, соцсети, телефония) обозначаются строковыми `sourceId`, список — в [12-dictionaries.md](12-dictionaries.md).

## Пример на PHP

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#section/Primer-na-PHP -->

```php
<?php
$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => "https://lcab.talk-me.ru/json/v1.0/chat/message/sendToClient",
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => [
        "X-Token: YOUR_API_TOKEN",
        "Content-Type: application/json",
    ],
    CURLOPT_POSTFIELDS => json_encode([
        "client" => ["id" => "ha832rjaafle4"],
        "operator" => ["login" => "my_login"],
        "message" => ["text" => "Здравствуйте! Чем можем помочь?"],
    ]),
    CURLOPT_RETURNTRANSFER => true,
]);

$response = json_decode(curl_exec($ch), true);
if (!$response["success"]) {
    throw new RuntimeException($response["error"]["descr"], $response["error"]["code"]);
}
var_dump($response["result"]);
```

## Пример на Python

```python
import requests

BASE_URL = "https://lcab.talk-me.ru/json/v1.0"


class TalkMeError(Exception):
    def __init__(self, code, descr):
        super().__init__(f"{code}: {descr}")
        self.code = code


def talkme(method: str, payload: dict | None = None, token: str = "YOUR_API_TOKEN"):
    """Вызывает метод Talk-Me, например talkme("chat/operator/getList")."""
    resp = requests.post(
        f"{BASE_URL}/{method}",
        json=payload or {},
        headers={"X-Token": token},
        timeout=30,
    )
    data = resp.json()
    if not data.get("success"):
        err = data.get("error", {})
        raise TalkMeError(err.get("code"), err.get("descr"))
    return data.get("result")


# Сообщения за период (не более 14 дней)
messages = talkme("chat/message/getList", {
    "dateRange": {"start": "2026-10-01", "stop": "2026-10-10 23:59:59"},
})
```

## Пример на JavaScript (Node.js 18+)

```javascript
const BASE_URL = "https://lcab.talk-me.ru/json/v1.0";

async function talkme(method, payload = {}, token = process.env.TALKME_TOKEN) {
  const res = await fetch(`${BASE_URL}/${method}`, {
    method: "POST",
    headers: { "X-Token": token, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!data.success) {
    throw new Error(`Talk-Me ${data.error?.code}: ${data.error?.descr}`);
  }
  return data.result;
}

// Ответ клиенту от имени оператора
const { id } = await talkme("chat/message/sendToClient", {
  client: { id: "ha832rjaafle4" },
  operator: { login: "my_login" },
  message: { text: "Здравствуйте! Чем можем помочь?" },
});
```

## Типовые сценарии

**Ответить посетителю из CRM.** Вызовите `chat/message/sendToClient` с `client.id` (или `client.searchId`), `operator.login` и `message.text`. Отправка возможна, если последнее сообщение в диалоге было от клиента или с момента последнего сообщения клиента прошло меньше 7 дней.

**Первым написать клиенту в мессенджер.** Получите настроенные каналы и имена отправителя через `chat/message/getStartChatChannels`, затем вызовите `chat/message/startChat` с `channelId`, `operatorLogin`, `recipientId` (телефон или email), `content.text` и `sourceId`. В некоторых каналах допускается только одобренный шаблон сообщения; отправка может тарифицироваться.

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/message/startChat' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "channelId": "whatsapp",
  "operatorLogin": "my_login",
  "recipientId": "79001234567",
  "content": {"text": "Здравствуйте! Ваш заказ готов."},
  "sourceId": "my_sender"
}'
```

**Передать сообщение посетителя операторам** (например, из своего канала): `chat/message/sendToOperator`.

**Получать события в реальном времени.** Зарегистрируйте сервер через `chat/webhook/save`, указав `url`, `secretKey` и включив нужные события в `params.actions` (например, `newMessageFromClient`, `dialogClosed`). Значение `secretKey` возвращается в каждом уведомлении — проверяйте его на своей стороне. Формат тел уведомлений в этой спецификации не описан.

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/webhook/save' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://mysite.com/webhook.php",
  "secretKey": "foobar",
  "params": {
    "actions": {
      "newMessageFromClient": true,
      "dialogClosed": true
    }
  }
}'
```

**Выгрузить статистику.** `chat/report/operatorDialogs` возвращает диалоги за период до 31 дня с метриками ответа операторов; `chat/rates/getList` и `chat/rates/getSummary` — отзывы клиентов.

## Разделы документации

| Файл | Раздел |
|---|---|
| [02-messages.md](02-messages.md) | Сообщения и диалоги (`chat/message/*`) |
| [03-operators.md](03-operators.md) | Операторы (`chat/operator/*`) |
| [04-clients.md](04-clients.md) | Посетители (`chat/client/*`) |
| [05-bots.md](05-bots.md) | Боты (`chat/bot/*`) |
| [06-reports.md](06-reports.md) | Отчёты (`chat/report/*`) |
| [07-rates.md](07-rates.md) | Отзывы (`chat/rates/*`) |
| [08-webhooks.md](08-webhooks.md) | Webhooks (`chat/webhook/*`) |
| [09-licenses.md](09-licenses.md) | Лицензии (`chat/license/*`) |
| [10-knowledge-base.md](10-knowledge-base.md) | База знаний (`chat/knowledgeBase/*`) |
| [11-models.md](11-models.md) | Общие модели ответов (сообщение, посетитель, диалог и др.) |
| [12-dictionaries.md](12-dictionaries.md) | Справочники значений (каналы, типы сообщений и др.) |
