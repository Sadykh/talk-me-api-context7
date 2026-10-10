#!/usr/bin/env python3
"""Генерирует Postman-коллекцию (v2.1) из OpenAPI-спецификации Talk-Me.

Использование:
    python3 scripts/build_postman.py path/to/specification.json

Результат: postman/talk-me-online-chat.postman_collection.json — импортируется в Postman
через File → Import. Перед запросами задайте переменную коллекции `token`.
"""
import json
import re
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_docs as bd  # noqa: E402

OUT_FILE = Path(__file__).resolve().parent.parent / "postman" / "talk-me-online-chat.postman_collection.json"
DOC_LINK_RE = re.compile(r"\[([^\]]+)\]\((\d\d-[\w-]+\.md)(?:#[^)]*)?\)")
# Поля, добавляемые в тело, чтобы случайный запуск не имел платных последствий.
BODY_OVERRIDES = {
    "/chat/license/create": {"validate": True},  # проверка без создания лицензии и списания денег
}
NAMESPACE = uuid.UUID("6f1f1c1e-3c55-4b8e-9a51-7a1c0e5d2b10")

CHECK_SUCCESS = [
    'pm.test("HTTP 200", function () {',
    "    pm.response.to.have.status(200);",
    "});",
    'pm.test("success == true", function () {',
    "    const body = pm.response.json();",
    "    pm.expect(body.success, body.error ? body.error.code + ': ' + body.error.descr : '').to.eql(true);",
    "});",
]


def stable_id(*parts):
    return str(uuid.uuid5(NAMESPACE, "/".join(parts)))


def json_body(obj):
    return {"mode": "raw", "raw": json.dumps(obj, ensure_ascii=False, indent=2),
            "options": {"raw": {"language": "json"}}}


def url(path):
    segments = path.strip("/").split("/")
    return {"raw": "{{baseUrl}}/" + "/".join(segments), "host": ["{{baseUrl}}"], "path": segments}


def headers():
    return [{"key": "Content-Type", "value": "application/json"}]


def description(spec, path, op):
    """Markdown-описание запроса: текст метода и таблица параметров."""
    out = []
    if op.get("deprecated"):
        repl = bd.DEPRECATED_REPLACEMENTS.get(path)
        out.append("> **Устаревший метод.**" + (f" Используйте `{repl}`." if repl else ""))
        out.append("")
    out.append(bd.md_text(op.get("description", "")) or op.get("summary", "").strip() + ".")
    out.append("")
    rb = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
    if rb:
        t = bd.Table(spec)
        t.walk(rb, top=True)
        out += ["**Параметры запроса**", "", t.render(), ""]
        rs, _ = spec.resolve(rb)
        if rs.get("discriminator"):
            out += bd.render_discriminator(spec, rs)
    else:
        out.append("Метод не принимает параметров — передаётся пустой объект `{}`.")
    tag = op.get("tags", [""])[0].replace("/", "")
    out += ["", f"Документация: {bd.DOC_PAGE}#tag/{tag}/paths/{path.replace('/', '~1')}/post"]
    # Относительные ссылки на файлы docs/ в Postman не открываются — оставляем текстовый указатель.
    return DOC_LINK_RE.sub(r"\1 (docs/\2)", "\n".join(out)).strip()


def request_item(spec, path, op):
    rb = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
    # Только обязательные поля: тело должно отправляться без правок (необязательные описаны в description).
    body = bd.example(spec, rb, "required") if rb else {}
    body.update(BODY_OVERRIDES.get(path, {}))
    name = op.get("summary", "").strip() or path
    if op.get("deprecated"):
        name = "[устарел] " + name
    request = {
        "method": "POST",
        "header": headers(),
        "body": json_body(body),
        "url": url(path),
        "description": description(spec, path, op),
    }
    item = {"id": stable_id(path), "name": name, "request": request, "response": []}
    r = op["responses"].get("200", {}).get("content", {}).get("application/json", {}).get("schema")
    if r:
        item["response"].append({
            "id": stable_id(path, "200"),
            "name": "Успешный ответ",
            "originalRequest": {k: v for k, v in request.items() if k != "description"},
            "status": "OK",
            "code": 200,
            "_postman_previewlanguage": "json",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": json.dumps(bd.response_example(spec, r), ensure_ascii=False, indent=2),
        })
    item["response"].append({
        "id": stable_id(path, "401"),
        "name": "Неверный X-Token",
        "originalRequest": {k: v for k, v in request.items() if k != "description"},
        "status": "Unauthorized",
        "code": 401,
        "_postman_previewlanguage": "json",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": json.dumps({"success": False, "error": {"code": 401, "descr": "Ошибка авторизации"}},
                           ensure_ascii=False, indent=2),
    })
    return item


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    spec = bd.Spec(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    ops = [(p, v["post"]) for p, v in spec.data["paths"].items()]
    folders = []
    for tag, (fname, title, intro) in bd.TAG_FILES.items():
        items = [request_item(spec, p, o) for p, o in ops if tag in o.get("tags", [])]
        folders.append({"id": stable_id("folder", tag), "name": title, "description": intro, "item": items})
    info = spec.data["info"]
    collection = {
        "info": {
            "_postman_id": stable_id("collection"),
            "name": "Talk-Me Online Chat REST API",
            "description": (
                "Коллекция методов REST API онлайн-чата Talk-Me (`json/v1.0`), сгенерирована из "
                "OpenAPI-спецификации https://lcab.talk-me.ru/cabinet/json-doc/cabinetRestApi/v1.0/online/specification.json.\n\n"
                "**Перед началом** задайте переменную коллекции `token` — API-токен онлайн-чата из личного кабинета. "
                "Он передаётся в заголовке `X-Token` во всех запросах.\n\n"
                "Все методы вызываются через `POST` с телом JSON. Успех определяется полем `success` ответа: "
                "при `true` данные лежат в `result`, при `false` — в `error {code, descr}`. "
                "Тест коллекции проверяет HTTP 200 и `success == true`.\n\n"
                f"Версия спецификации: {info.get('version', '')}."
            ),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "auth": {
            "type": "apikey",
            "apikey": [
                {"key": "key", "value": "X-Token", "type": "string"},
                {"key": "value", "value": "{{token}}", "type": "string"},
                {"key": "in", "value": "header", "type": "string"},
            ],
        },
        "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": CHECK_SUCCESS}}],
        "variable": [
            {"key": "baseUrl", "value": bd.BASE_URL, "type": "string"},
            {"key": "token", "value": "", "type": "secret"},
        ],
        "item": folders,
    }
    OUT_FILE.parent.mkdir(exist_ok=True)
    OUT_FILE.write_text(json.dumps(collection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{OUT_FILE.name}: {sum(len(f['item']) for f in folders)} запросов в {len(folders)} папках")


if __name__ == "__main__":
    main()
