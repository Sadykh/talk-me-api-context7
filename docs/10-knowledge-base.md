# База знаний

Методы раздела `chat/knowledgeBase`: список баз знаний, дерево групп и статей, чтение, сохранение и удаление статей и групп.

Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: `{"success": true, "result": ...}`, ошибка: `{"success": false, "error": {"code", "descr"}}` (подробнее — [01-overview.md](01-overview.md)).

| Метод | Назначение |
|---|---|
| `/chat/knowledgeBase/getKnowledgeBaseList` | Список баз знаний |
| `/chat/knowledgeBase/getStructure` | Получение структуры базы знаний |
| `/chat/knowledgeBase/getArticle` | Получение статьи |
| `/chat/knowledgeBase/saveArticle` | Сохранение статьи |
| `/chat/knowledgeBase/deleteArticle` | Удаление статьи |
| `/chat/knowledgeBase/saveGroup` | Сохранение группы |
| `/chat/knowledgeBase/deleteGroup` | Удаление группы |

## POST /chat/knowledgeBase/getKnowledgeBaseList — Список баз знаний

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/ChatknowledgeBase/paths/~1chat~1knowledgeBase~1getKnowledgeBaseList/post -->

С помощью данного метода вы можете получить список созданных баз знаний

`POST https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/getKnowledgeBaseList`

**Параметры запроса**

Метод не принимает параметров — передайте пустой JSON-объект `{}`.

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/getKnowledgeBaseList' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "knowledgeBaseList": [
      {
        "id": "string",
        "descr": "string",
        "address": "string"
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatGetKnowledgeBaseListResult) |
| `result.knowledgeBaseList` | array<object> | База знаний |
| `result.knowledgeBaseList[].id` | string | Уникальный идентификатор базы знаний |
| `result.knowledgeBaseList[].descr` | string | Название |
| `result.knowledgeBaseList[].address` | string | Адрес |

## POST /chat/knowledgeBase/getStructure — Получение структуры базы знаний

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/ChatknowledgeBase/paths/~1chat~1knowledgeBase~1getStructure/post -->

С помощью данного метода вы можете получить дерево статей и групп в базе знаний

`POST https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/getStructure`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `knowledgeBaseId` | string | да | Идентификатор базы знаний |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/getStructure' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "knowledgeBaseId": "kb_id"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "groups": [
      {
        "id": "string",
        "descr": "string",
        "tags": [
          "string"
        ],
        "groups": [
          {}
        ],
        "articles": [
          {
            "id": "string",
            "descr": "string",
            "dateTimeCreate": 1790000000,
            "dateTimeUpdate": 1790000000,
            "isPublished": true,
            "tags": [
              "string"
            ],
            "url": "https://example.com"
          }
        ]
      }
    ],
    "articles": [
      {
        "id": "string",
        "descr": "string",
        "dateTimeCreate": 1790000000,
        "dateTimeUpdate": 1790000000,
        "isPublished": true,
        "tags": [
          "string"
        ],
        "url": "https://example.com"
      }
    ]
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatKnowledgeBaseGetStructureResult) |
| `result.groups` | array<object> | Группы |
| `result.groups[].id` | string | Идентификатор группы |
| `result.groups[].descr` | string | Название группы |
| `result.groups[].tags` | array<string> | Тэги |
| `result.groups[].nameInUrl` | string | Название группы в URL |
| `result.groups[].groups` | array<object> | Вложенные группы |
| `result.groups[].articles` | array<object> | Статьи |
| `result.groups[].articles[].id` | string | Идентификатор статьи |
| `result.groups[].articles[].descr` | string | Название статьи |
| `result.groups[].articles[].dateTimeCreate` | integer | Дата создания<br>Пример: `1790000000` |
| `result.groups[].articles[].dateTimeUpdate` | integer | Дата последнего обновления<br>Пример: `1790000000` |
| `result.groups[].articles[].isPublished` | boolean | Статья опубликована? |
| `result.groups[].articles[].tags` | array<string> | Тэги |
| `result.groups[].articles[].url` | string | Ссылка на статью |
| `result.groups[].articles[].groupId` | string | id группы |
| `result.groups[].articles[].nameInUrl` | string | Название статьи в URL |
| `result.articles` | array<object> | Статьи |
| `result.articles[].id` | string | Идентификатор статьи |
| `result.articles[].descr` | string | Название статьи |
| `result.articles[].dateTimeCreate` | integer | Дата создания<br>Пример: `1790000000` |
| `result.articles[].dateTimeUpdate` | integer | Дата последнего обновления<br>Пример: `1790000000` |
| `result.articles[].isPublished` | boolean | Статья опубликована? |
| `result.articles[].tags` | array<string> | Тэги |
| `result.articles[].url` | string | Ссылка на статью |
| `result.articles[].groupId` | string | id группы |
| `result.articles[].nameInUrl` | string | Название статьи в URL |

## POST /chat/knowledgeBase/getArticle — Получение статьи

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/ChatknowledgeBase/paths/~1chat~1knowledgeBase~1getArticle/post -->

С помощью данного метода вы можете получить дерево статей и групп в базе знаний

`POST https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/getArticle`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `knowledgeBaseId` | string | да | Идентификатор базы знаний |
| `articleId` | string | да | Идентификатор статьи |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/getArticle' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "knowledgeBaseId": "kb_id",
  "articleId": "article_id"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "article": {
      "id": "string",
      "descr": "string",
      "dateTimeCreate": 1790000000,
      "dateTimeUpdate": 1790000000,
      "isPublished": true,
      "tags": [
        "string"
      ],
      "url": "https://example.com",
      "html": "string"
    }
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatKnowledgeBaseGetArticleResult) |
| `result.article` | object | Статья |
| `result.article.id` | string | Идентификатор статьи |
| `result.article.descr` | string | Название статьи |
| `result.article.dateTimeCreate` | integer | Дата создания<br>Пример: `1790000000` |
| `result.article.dateTimeUpdate` | integer | Дата последнего обновления<br>Пример: `1790000000` |
| `result.article.isPublished` | boolean | Статья опубликована? |
| `result.article.tags` | array<string> | Тэги |
| `result.article.url` | string | Ссылка на статью |
| `result.article.groupId` | string | id группы |
| `result.article.nameInUrl` | string | Название статьи в URL |
| `result.article.html` | string | HTML-контент статьи |

## POST /chat/knowledgeBase/saveArticle — Сохранение статьи

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/ChatknowledgeBase/paths/~1chat~1knowledgeBase~1saveArticle/post -->

С помощью данного метода вы можете сохранить статью в базе знаний

`POST https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/saveArticle`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `knowledgeBaseId` | string | да | Идентификатор базы знаний |
| `articleId` | string |  | Идентификатор статьи |
| `descr` | string | да | Название статьи |
| `nameInUrl` | string |  | Название статьи в URL |
| `isPublished` | boolean |  | Статья опубликована?<br>По умолчанию: `true` |
| `tags` | array<string> |  | Тэги |
| `content` | string | да | Контент статьи в формате HTML |
| `groupId` | string |  | id группы |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/saveArticle' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "knowledgeBaseId": "kb_id",
  "descr": "string",
  "content": "string"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "articleId": "article_id"
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatKnowledgeBaseSaveArticleResult) |
| `result.articleId` | string | id сохраненной статьи |

## POST /chat/knowledgeBase/deleteArticle — Удаление статьи

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/ChatknowledgeBase/paths/~1chat~1knowledgeBase~1deleteArticle/post -->

С помощью данного метода вы можете удалить статью в базе знаний

`POST https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/deleteArticle`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `knowledgeBaseId` | string | да | Идентификатор базы знаний |
| `articleId` | string | да | Идентификатор статьи |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/deleteArticle' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "knowledgeBaseId": "kb_id",
  "articleId": "article_id"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```

## POST /chat/knowledgeBase/saveGroup — Сохранение группы

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/ChatknowledgeBase/paths/~1chat~1knowledgeBase~1saveGroup/post -->

С помощью данного метода вы можете сохранить группу в базе знаний

`POST https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/saveGroup`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `knowledgeBaseId` | string | да | Идентификатор базы знаний |
| `groupId` | string |  | Идентификатор группы |
| `descr` | string | да | Название группы |
| `nameInUrl` | string | да | Название группы в URL |
| `parentGroupId` | string |  | id группы |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/saveGroup' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "knowledgeBaseId": "kb_id",
  "descr": "string",
  "nameInUrl": "string"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {
    "groupId": "group_id"
  }
}
```

**Поля ответа**

| Поле | Тип | Описание |
|---|---|---|
| `result` | object | Результат работы метода (ChatKnowledgeBaseSaveGroupResult) |
| `result.groupId` | string | id сохраненной группы |

## POST /chat/knowledgeBase/deleteGroup — Удаление группы

<!-- source: https://lcab.talk-me.ru/cabinet/json-doc/online#tag/ChatknowledgeBase/paths/~1chat~1knowledgeBase~1deleteGroup/post -->

С помощью данного метода вы можете удалить группу в базе знаний

`POST https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/deleteGroup`

**Параметры запроса**

| Поле | Тип | Обязательный | Описание |
|---|---|---|---|
| `knowledgeBaseId` | string | да | Идентификатор базы знаний |
| `groupId` | string | да | Идентификатор статьи |
| `moveChildrenToTop` | boolean |  | Перенос вложенных статей и групп на уровень выше<br>По умолчанию: `false` |

**Пример запроса**

```bash
curl -X POST 'https://lcab.talk-me.ru/json/v1.0/chat/knowledgeBase/deleteGroup' \
  -H 'X-Token: YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "knowledgeBaseId": "kb_id",
  "groupId": "group_id"
}'
```

**Пример ответа** (показаны обязательные поля)

```json
{
  "success": true,
  "result": {}
}
```
