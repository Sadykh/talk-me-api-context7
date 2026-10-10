#!/usr/bin/env python3
"""Генерирует Markdown-документацию для Context7 из OpenAPI-спецификации Talk-Me.

Использование:
    python3 scripts/build_docs.py path/to/specification.json

Спецификация: https://lcab.talk-me.ru/cabinet/json-doc/cabinetRestApi/v1.0/online/specification.json
Ручные разделы (docs/01-*.md, docs/90-*.md) не перезаписываются.
"""
import hashlib
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

BASE_URL = "https://lcab.talk-me.ru/json/v1.0"
DOC_PAGE = "https://lcab.talk-me.ru/cabinet/json-doc/online"
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

# Файл, заголовок и вводный текст для каждого тега спецификации.
TAG_FILES = OrderedDict([
    ("Chat/message", ("02-messages.md", "Сообщения и диалоги",
                      "Методы раздела `chat/message`: чтение истории, отправка сообщений клиенту и оператору, "
                      "начало чата в мессенджерах, редактирование и удаление сообщений, статусы, реакции, "
                      "перевод посетителя на другого оператора и завершение диалога.")),
    ("Chat/operator", ("03-operators.md", "Операторы",
                       "Методы раздела `chat/operator`: список операторов, авторизация и сессии, статусы, "
                       "создание, редактирование, удаление и включение операторов, управление отделами.")),
    ("Chat/client", ("04-clients.md", "Посетители (клиенты)",
                     "Методы раздела `chat/client`: данные посетителя, блокировка, прикрепление к операторам, "
                     "посещённые страницы, список и поиск посетителей, Offline-вопросы, счётчик посетителей онлайн.")),
    ("Chat/bot", ("05-bots.md", "Боты",
                  "Методы раздела `chat/bot`: запуск и остановка сценария чат-бота для посетителя.")),
    ("Chat/report", ("06-reports.md", "Отчёты",
                     "Методы раздела `chat/report`: выгрузка диалогов с метриками операторов и отчёт "
                     "по заполненным формам.")),
    ("Chat/rates", ("07-rates.md", "Отзывы",
                    "Методы раздела `chat/rates`: список отзывов (оценок) посетителей и агрегированный отчёт.")),
    ("Chat/webhook", ("08-webhooks.md", "Webhooks",
                      "Методы раздела `chat/webhook`: настройка серверов, на которые Talk-Me отправляет "
                      "уведомления о событиях онлайн-чата.")),
    ("Chat/license", ("09-licenses.md", "Лицензии",
                      "Методы раздела `chat/license`: покупка лицензии для сайта и список действующих лицензий.")),
    ("Chat/knowledgeBase", ("10-knowledge-base.md", "База знаний",
                            "Методы раздела `chat/knowledgeBase`: список баз знаний, дерево групп и статей, "
                            "чтение, сохранение и удаление статей и групп.")),
])
MODELS_FILE = "11-models.md"
DEPRECATED_REPLACEMENTS = {
    "/chat/message/editMessageSentToClient": "/chat/message/editMessage",
    "/chat/message/deleteMessageToClientMethod": "/chat/message/deleteMessage",
    "/chat/report/operators": "/chat/report/operatorDialogs",
}
DICT_FILE = "12-dictionaries.md"

# Модели ответа, которые выносятся в отдельный файл вместо повторения в каждом методе.
SHARED_MIN_ROWS = 12
LONG_DESCR_LINES = 4
MAX_PATTERN_LEN = 60

# Длинные пояснения (списки значений), встречающиеся в нескольких полях: текст -> заголовок.
# Заполняется первым (холостым) проходом генерации.
DICT_USAGE = OrderedDict()
DICTS = OrderedDict()
# Заголовки справочников по названию первого поля, где встретился список.
DICT_TITLES = {"Эмоции": "Эмоции клиента (AI-анализ диалога)", "Идентификатор пакета": "Пакеты лицензий (batchId)"}


RANDOM_ID_RE = re.compile(r"^(?=.*[g-z])[a-z0-9]{32}$")
DATETIME_RE = re.compile(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d$")
FIXED_DATES = {"start": "2026-10-01 00:00:00", "stop": "2026-10-07 23:59:59"}


def fix_examples(o, key=None):
    """Сервер подставляет в примеры текущее время; делаем их постоянными и осмысленными."""
    if isinstance(o, dict):
        ex = o.get("example")
        if isinstance(ex, str) and RANDOM_ID_RE.match(ex):
            o["example"] = hashlib.md5(str(key).encode()).hexdigest()
        elif isinstance(ex, str) and DATETIME_RE.match(ex):
            o["example"] = FIXED_DATES.get(key, "2026-10-01 12:00:00")
        elif isinstance(ex, int) and not isinstance(ex, bool) and 1_600_000_000 < ex < 2_100_000_000:
            o["example"] = 1790000000
        for k, v in o.items():
            fix_examples(v, k if k not in ("properties", "items") else key)
    elif isinstance(o, list):
        for v in o:
            fix_examples(v, key)


class Spec:
    def __init__(self, data):
        fix_examples(data)
        self.data = data
        self.schemas = data["components"]["schemas"]

    def resolve(self, s):
        """Возвращает (схема, имя модели или None)."""
        name = None
        while isinstance(s, dict) and "$ref" in s:
            name = s["$ref"].rsplit("/", 1)[-1]
            s = self.schemas[name]
        return s, name

    def merged(self, s):
        """Сливает allOf в одну схему с properties/required."""
        s, _ = self.resolve(s)
        if "allOf" not in s:
            return s
        out = {k: v for k, v in s.items() if k != "allOf"}
        props = OrderedDict()
        required = []
        for part in s["allOf"]:
            p = self.merged(part)
            for k in ("title", "description", "type"):
                if k in p and k not in out:
                    out[k] = p[k]
            props.update(p.get("properties", {}))
            required += p.get("required", [])
        props.update(s.get("properties", {}))
        out["properties"] = props
        out["required"] = required + s.get("required", [])
        out.setdefault("type", "object")
        return out


# ---------------------------------------------------------------- текст

def clean(text):
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"\\\n", "\n", text)  # markdown hard break
    lines = [ln.strip() for ln in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.replace("(/cabinet/json-doc/", "(https://lcab.talk-me.ru/cabinet/json-doc/")
    return text.strip()


def cell(text):
    text = clean(text)
    text = re.sub(r"\n\s*\n", "\n", text)
    text = re.sub(r"^\* ", "", text, flags=re.M)
    return text.replace("|", "\\|").replace("\n", "<br>")


def md_text(text):
    """Текст описания для вывода вне таблицы."""
    return clean(text)


# ---------------------------------------------------------------- таблицы полей

def type_str(spec, s):
    s, name = spec.resolve(s)
    s = spec.merged(s)
    t = s.get("type")
    if t == "array":
        it, _ = spec.resolve(s.get("items", {}))
        it = spec.merged(it)
        inner = it.get("type", "object" if "properties" in it or "oneOf" in it else "any")
        t = f"array<{inner}>"
    elif not t:
        t = "object" if ("properties" in s or "oneOf" in s or "additionalProperties" in s) else "any"
    if s.get("nullable"):
        t += " \\| null"
    return t


def constraints(s):
    parts = []
    if "enum" in s:
        vals = ", ".join(f"`{v}`" if v != "" else "`\"\"`" for v in s["enum"])
        parts.append(f"Значения: {vals}")
    if "default" in s:
        parts.append(f"По умолчанию: `{json.dumps(s['default'], ensure_ascii=False)}`")
    for key, label in (("minimum", "min"), ("maximum", "max"), ("minLength", "minLength"),
                       ("maxLength", "maxLength"), ("minItems", "minItems"), ("maxItems", "maxItems")):
        if key in s:
            parts.append(f"{label}: {s[key]}")
    if "pattern" in s and len(s["pattern"]) <= MAX_PATTERN_LEN:
        parts.append(f"Шаблон: `{s['pattern']}`")
    if "format" in s:
        parts.append(f"Формат: `{s['format']}`")
    if "example" in s and not isinstance(s["example"], (dict, list)):
        parts.append(f"Пример: `{json.dumps(s['example'], ensure_ascii=False)}`")
    return parts


class Table:
    def __init__(self, spec, shared=None, with_required=True):
        self.spec = spec
        self.shared = shared or {}
        self.with_required = with_required
        self.rows = []
        self.notes = []
        self.refs = []  # общие модели, на которые сослались

    def add(self, path, s, required, title, descr, extra=None):
        s_res, _ = self.spec.resolve(s)
        s_res = self.spec.merged(s_res)
        text = clean(title)
        d = clean(descr)
        if d and d != text:
            if d.count("\n") + 1 > LONG_DESCR_LINES:
                DICT_USAGE.setdefault(d, []).append((clean(title) or path, path))
                if d in DICTS:
                    link = f"[{DICTS[d]}]({DICT_FILE}#{anchor(DICTS[d])})"
                    text = (text + "<br>" if text else "") + f"Расшифровка значений: {link}"
                else:
                    self.notes.append((path, d))
                    text = (text + " " if text else "") + "(см. пояснение ниже)"
            else:
                text = f"{text}\n{d}" if text else d
        parts = constraints(s_res)
        if s_res.get("deprecated") or s.get("deprecated"):
            parts.insert(0, "**Устарело**")
        if extra:
            parts.append(extra)
        full = cell(text)
        if parts:
            full = (full + "<br>" if full else "") + "<br>".join(cell(p) for p in parts)
        self.rows.append((f"`{path}`", type_str(self.spec, s), required, full))

    def walk(self, s, prefix="", stack=(), top=False):
        s, name = self.spec.resolve(s)
        if name and not top and name in self.shared:
            return
        s = self.spec.merged(s)
        if name:
            stack = stack + (name,)
        props = s.get("properties", {})
        req = set(s.get("required", []))
        for key, p in props.items():
            self.prop(prefix + key, p, "да" if key in req else "", stack)
        if "oneOf" in s and not s.get("discriminator"):
            variants = []
            for v in s["oneOf"]:
                vs, vname = self.spec.resolve(v)
                vs = self.spec.merged(vs)
                vreq = set(vs.get("required", []))
                keys = [k for k in vs.get("properties", {}) if k not in props]
                variants.append((vs.get("title") or vname, [prefix + k for k in keys if k in vreq]))
                for k in keys:
                    self.prop(prefix + k, vs["properties"][k], "условно" if k in vreq else "", stack)
            label = prefix.rstrip(".") or "тело запроса"
            options = "; ".join(f"{t}: " + ", ".join(f"`{k}`" for k in ks) for t, ks in variants)
            self.notes.append((label, f"Нужно передать один из вариантов идентификации — {options}."))
        ap = s.get("additionalProperties")
        if isinstance(ap, dict):
            self.prop(prefix + "{key}", ap, "", stack)

    def prop(self, path, p, required, stack):
        ps, name = self.spec.resolve(p)
        ps_m = self.spec.merged(ps)
        title = p.get("title") or ps_m.get("title", "")
        descr = p.get("description") or ps_m.get("description", "")
        if not descr and ps_m.get("type") == "array":
            descr = self.spec.resolve(ps_m.get("items", {}))[0].get("description", "")
        if name and name in stack:
            self.add(path, p, required, title, descr, f"Рекурсивно: та же структура, что у `{name.replace('OpenApiModel', '')}`")
            return
        target, tname, suffix = ps_m, name, ""
        if ps_m.get("type") == "array":
            it, iname = self.spec.resolve(ps_m.get("items", {}))
            target, tname, suffix = self.spec.merged(it), iname, "[]"
        extra = None
        if tname and tname in self.shared:
            extra = f"Структура: [{self.shared[tname]}]({MODELS_FILE}#{anchor(self.shared[tname])})"
            self.refs.append(tname)
        self.add(path, p, required, title, descr, extra)
        if extra:
            return
        if tname and tname in stack:
            return
        if target.get("properties") or target.get("oneOf") or isinstance(target.get("additionalProperties"), dict):
            sub_stack = stack + ((tname,) if tname else ())
            self.walk(target, path + suffix + ".", sub_stack)

    def render(self):
        if not self.rows:
            return ""
        if self.with_required:
            out = ["| Поле | Тип | Обязательный | Описание |", "|---|---|---|---|"]
            out += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in self.rows]
        else:
            out = ["| Поле | Тип | Описание |", "|---|---|---|"]
            out += [f"| {a} | {b} | {d} |" for a, b, c, d in self.rows]
        text = "\n".join(out)
        if self.notes:
            text += "\n\n**Пояснения к полям**\n"
            for path, d in self.notes:
                body = d.replace("\n___\n", "\n").strip()
                text += f"\n`{path}`:\n\n{body}\n"
        return text


def anchor(title):
    a = title.strip().lower()
    a = re.sub(r"[^\w\- ]", "", a)
    return a.replace(" ", "-")


# ---------------------------------------------------------------- примеры

# Заглушки для строковых полей без примера в спецификации.
STRING_PLACEHOLDERS = {
    "operatorLogin": "my_login", "login": "my_login", "recipientId": "79001234567",
    "text": "Здравствуйте! Чем можем помочь?", "sourceId": "my_sender", "clientId": "ha832rjaafle4",
    "email": "ivan@example.com", "phone": "79001234567", "url": "https://example.com",
    "emailSubject": "Ответ на ваш вопрос", "name": "Иван", "emoji": "👍",
    "knowledgeBaseId": "kb_id", "articleId": "article_id", "groupId": "group_id",
}


def placeholder(s, key=None):
    t = s.get("type")
    if t == "string" and "почт" in (s.get("description", "") + s.get("title", "")).lower():
        return STRING_PLACEHOLDERS["email"]
    if t == "string" and key in STRING_PLACEHOLDERS:
        return STRING_PLACEHOLDERS[key]
    if t == "integer":
        return 0
    if t == "number":
        return 0
    if t == "boolean":
        return True
    if t == "string":
        return "string"
    return None


def example(spec, s, mode, stack=(), depth=0, key=None):
    """mode: request — обязательные поля и поля с примером; required — только обязательные;
    response — обязательные (или все, если обязательных нет); full — все."""
    s, name = spec.resolve(s)
    if name in stack or depth > 8:
        return [] if s.get("type") == "array" else {}
    if name:
        stack = stack + (name,)
    if "example" in s:
        return s["example"]
    s = spec.merged(s)
    if s.get("type") == "array":
        return [example(spec, s.get("items", {}), mode, stack, depth + 1)]
    props = OrderedDict(s.get("properties", {}))
    req = list(s.get("required", []))
    if "oneOf" in s:
        v = spec.merged(s["oneOf"][0])
        for k, p in v.get("properties", {}).items():
            props.setdefault(k, p)
        req += v.get("required", [])
    if props or s.get("type") == "object" or "additionalProperties" in s:
        out = OrderedDict()
        for k, p in props.items():
            ps, _ = spec.resolve(p)
            if p.get("deprecated") or ps.get("deprecated"):
                continue
            if mode == "request" and k not in req:
                if "example" not in p and "example" not in ps:
                    continue
            if mode == "response" and req and k not in req:
                continue
            if mode == "required" and k not in req:
                continue
            if mode in ("request", "required") and k in req and k == "channelId" and "enum" in ps and len(ps["enum"]) == 1:
                out[k] = ps["enum"][0]
                continue
            out[k] = example(spec, p, mode, stack, depth + 1, k)
        if mode == "required" and not out and props:
            # «Нужен хотя бы один из идентификаторов» — берём первое поле с примером.
            k = next((k for k, p in props.items() if "example" in p or "example" in spec.resolve(p)[0]),
                     next(iter(props)))
            out[k] = example(spec, props[k], mode, stack, depth + 1, k)
        if not props and isinstance(s.get("additionalProperties"), dict):
            out["key"] = example(spec, s["additionalProperties"], mode, stack, depth + 1)
        return out
    if "default" in s:
        return s["default"]
    if s.get("enum"):
        return s["enum"][0]
    return placeholder(s, key)


def response_example(spec, schema):
    s = spec.merged(schema)
    body = OrderedDict([("success", True)])
    if "result" in s.get("properties", {}):
        body["result"] = example(spec, s["properties"]["result"], "response")
    return body


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- генерация

def op_heading(path, op):
    return f"POST {path} — {op.get('summary', '').strip()}"


def find_shared(spec, ops):
    """Модели ответа, встречающиеся в нескольких методах и достаточно крупные."""
    usage = {}

    def collect(s, stack, op_path):
        s, name = spec.resolve(s)
        if name:
            if name in stack:
                return
            usage.setdefault(name, set()).add(op_path)
            stack = stack + (name,)
        s = spec.merged(s)
        for p in s.get("properties", {}).values():
            collect(p, stack, op_path)
        if s.get("type") == "array":
            collect(s.get("items", {}), stack, op_path)
        for v in s.get("oneOf", []):
            collect(v, stack, op_path)
        if isinstance(s.get("additionalProperties"), dict):
            collect(s["additionalProperties"], stack, op_path)

    for path, op in ops:
        r = op["responses"].get("200", {}).get("content", {}).get("application/json", {}).get("schema")
        if r:
            collect(r, (), path)
    shared = OrderedDict()
    for name, paths in usage.items():
        if len(paths) < 2:
            continue
        t = Table(spec)
        t.walk({"$ref": f"#/components/schemas/{name}"}, top=True)
        if len(t.rows) >= SHARED_MIN_ROWS:
            title = spec.merged(spec.schemas[name]).get("title") or name
            shared[name] = f"{title} ({name.replace('OpenApiModel', '')})"
    return shared


def render_op(spec, path, op, shared):
    out = [f"## {op_heading(path, op)}", ""]
    tag = op.get("tags", [""])[0].replace("/", "")
    out.append(f"<!-- source: {DOC_PAGE}#tag/{tag}/paths/{path.replace('/', '~1')}/post -->")
    out.append("")
    if op.get("deprecated"):
        repl = DEPRECATED_REPLACEMENTS.get(path)
        hint = f"используйте `{repl}`" if repl else "используйте актуальный аналог"
        out.append(f"> **Устаревший метод.** Сохраняется для совместимости; в новых интеграциях {hint}.")
        out.append("")
    descr = md_text(op.get("description", ""))
    out.append(descr or f"{op.get('summary', '').strip()}.")
    out.append("")
    out.append(f"`POST {BASE_URL}{path}`")
    out.append("")

    rb = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
    if rb:
        t = Table(spec)
        t.walk(rb, top=True)
        out += ["**Параметры запроса**", "", t.render(), ""]
        rs, _ = spec.resolve(rb)
        if rs.get("discriminator"):
            out += render_discriminator(spec, rs)
        body = example(spec, rb, "request")
    else:
        out += ["**Параметры запроса**", "", "Метод не принимает параметров — передайте пустой JSON-объект `{}`.", ""]
        body = {}

    out += ["**Пример запроса**", "", "```bash",
            f"curl -X POST '{BASE_URL}{path}' \\",
            "  -H 'X-Token: YOUR_API_TOKEN' \\",
            "  -H 'Content-Type: application/json' \\",
            f"  -d '{json.dumps(body, ensure_ascii=False, indent=2)}'",
            "```", ""]

    r = op["responses"].get("200", {}).get("content", {}).get("application/json", {}).get("schema")
    if r:
        rs = spec.merged(r)
        res = rs.get("properties", {}).get("result")
        out += ["**Пример ответа** (показаны обязательные поля)", "", "```json", dumps(response_example(spec, r)), "```", ""]
        if res:
            t = Table(spec, shared, with_required=False)
            t.prop("result", res, "", ())
            if len(t.rows) > 1 or t.notes:
                out += ["**Поля ответа**", "", t.render(), ""]
    return "\n".join(out).rstrip() + "\n"


def render_discriminator(spec, s):
    """Поля для каждого значения дискриминатора; варианты с одинаковым набором полей объединяются."""
    disc = s["discriminator"]
    key = disc["propertyName"]
    groups = OrderedDict()
    for value, ref in disc["mapping"].items():
        t = Table(spec)
        t.walk({"$ref": ref}, top=True)
        t.rows = [r for r in t.rows if r[0] != f"`{key}`"]
        groups.setdefault(t.render(), []).append((value, ref))
    out = [f"Остальные поля зависят от значения `{key}`:", ""]
    for table, items in groups.items():
        values = ", ".join(f"`{v}`" for v, _ in items)
        out += [f"**`{key}` = {values}**", "", table, ""]
        for value, ref in items[:1]:
            out += ["```json", dumps(example(spec, {"$ref": ref}, "request")), "```", ""]
    return out


def render_models(spec, shared):
    out = ["# Модели данных в ответах API", "",
           "Структуры объектов, которые возвращаются сразу несколькими методами онлайн-чата Talk-Me. "
           "В описаниях методов на них стоят ссылки «Структура: …».", ""]
    for name, title in shared.items():
        out.append(f"## {title}")
        out.append("")
        s = spec.merged(spec.schemas[name])
        d = md_text(s.get("description", ""))
        if d:
            out += [d, ""]
        others = {k: v for k, v in shared.items() if k != name}
        t = Table(spec, others, with_required=False)
        t.walk({"$ref": f"#/components/schemas/{name}"}, top=True)
        out += [t.render(), ""]
        out += ["```json", dumps(example(spec, {"$ref": f"#/components/schemas/{name}"}, "full")), "```", ""]
    return "\n".join(out).rstrip() + "\n"


def render_dicts():
    out = ["# Справочники значений", "",
           "Списки допустимых значений, которые используются в нескольких методах API онлайн-чата Talk-Me.", ""]
    for text, title in DICTS.items():
        fields = sorted({f"`{path}`" for _, path in DICT_USAGE[text]})
        out += [f"## {title}", "", "Используется в полях: " + ", ".join(fields) + ".", "",
                text.replace("\n___\n", "\n"), ""]
    return "\n".join(out).rstrip() + "\n"


def build_files(spec, ops, shared):
    files = OrderedDict()
    for tag, (fname, title, intro) in TAG_FILES.items():
        tag_ops = [(p, o) for p, o in ops if tag in o.get("tags", [])]
        out = [f"# {title}", "", intro, "",
               "Все методы вызываются через `POST` на `https://lcab.talk-me.ru/json/v1.0/{method}` "
               "с заголовками `X-Token` и `Content-Type: application/json`. Успешный ответ: "
               "`{\"success\": true, \"result\": ...}`, ошибка: `{\"success\": false, \"error\": {\"code\", \"descr\"}}` "
               "(подробнее — [01-overview.md](01-overview.md)).", "",
               "| Метод | Назначение |", "|---|---|"]
        for p, o in tag_ops:
            mark = " (устарел)" if o.get("deprecated") else ""
            out.append(f"| `{p}` | {cell(o.get('summary', ''))}{mark} |")
        out.append("")
        for p, o in tag_ops:
            out.append(render_op(spec, p, o, shared))
        files[fname] = "\n".join(out).rstrip() + "\n"
    files[MODELS_FILE] = render_models(spec, shared)
    return files


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    spec = Spec(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    ops = [(p, v["post"]) for p, v in spec.data["paths"].items()]
    shared = find_shared(spec, ops)
    # Первый проход только собирает длинные пояснения, которые повторяются в разных полях.
    build_files(spec, ops, shared)
    for text, fields in DICT_USAGE.items():
        if len(fields) > 1:
            title = DICT_TITLES.get(fields[0][0], fields[0][0])
            DICTS[text] = title
    DICT_USAGE.clear()
    files = build_files(spec, ops, shared)
    files[DICT_FILE] = render_dicts()
    DOCS_DIR.mkdir(exist_ok=True)
    for fname, text in files.items():
        (DOCS_DIR / fname).write_text(text, encoding="utf-8")
    print(f"{len(ops)} методов, общих моделей: {len(shared)}: {', '.join(shared)}")


if __name__ == "__main__":
    main()
