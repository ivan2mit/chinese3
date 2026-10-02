#!/usr/bin/env python3
"""Встраивает задания по иероглифам (hz-*) в olympiad.html.

Источник: hz/hz.js (плеер, собран esbuild из animcjk-task-editor/exercises/olympiad-bridge.js),
hz/hz.css (player.css) и hz/hzq.json (exercises/demo/questions.json).
Первый запуск вносит правки в код кабинета; повторные только обновляют три
встроенных блока между маркерами hz:css / hz:js. Запуск: python3 build-hz.py
"""
import json, pathlib, re

here = pathlib.Path(__file__).parent
page = here / "olympiad.html"
s = page.read_text(encoding="utf-8")
css = (here / "hz" / "hz.css").read_text(encoding="utf-8")
js = (here / "hz" / "hz.js").read_text(encoding="utf-8")
data = json.dumps(json.loads((here / "hz" / "hzq.json").read_text(encoding="utf-8")), ensure_ascii=False, separators=(",", ":"))

def rep(a, b):
    global s
    if a not in s: raise SystemExit("не найден фрагмент: " + a[:70])
    s = s.replace(a, b, 1)

css_block = f"/* hz:css:begin */\n{css}\n/* hz:css:end */"
js_block = f"<script>/* hz:js:begin */\nwindow.HZQ = {data};\n{js}\n/* hz:js:end */</script>\n"

if "hz:css:begin" in s:   # обновление блоков
    s = re.sub(r"/\* hz:css:begin \*/.*?/\* hz:css:end \*/", lambda m: css_block, s, count=1, flags=re.S)
    s = re.sub(r"<script>/\* hz:js:begin \*/.*?/\* hz:js:end \*/</script>\n", lambda m: js_block, s, count=1, flags=re.S)
else:                     # первый запуск
    rep("</style>", css_block + "\n</style>")
    rep("<script>\nconst $ = ", js_block + "<script>\nconst $ = ")
    rep("\n];\nconst S = {i:20,", "\n];\nconst HZ_FIRST = Q.length;\nHZQ.questions.forEach(q => Q.push({type:q.type, prompt:q.prompt, hz:q}));\nconst S = {i:HZ_FIRST, hz:[],")
    rep("record:'Запись голоса'}", "record:'Запись голоса', 'hz-strokes':'Недостающие черты', 'hz-keys':'Недостающие ключи', 'hz-order':'Порядок черт'}")
    rep("  if(q.type === 'match'){ renderMatch", "  if(q.type.startsWith('hz-')){ renderHz(q); chrome(); $('#tune').innerHTML = '<p class=\"note\">Оформление этого типа задаёт редактор заданий по иероглифам.</p>'; return; }\n  if(q.type === 'match'){ renderMatch")
    rep("function fit(){", """function renderHz(q){
  HZ.mount($('#qBody'), q.hz, HZQ.bank, S.hz[S.i] || null, (answer, filled) => {
    S.hz[S.i] = answer; S.ans[S.i] = new Set(filled ? [0] : []); chrome(); markSaving();
  });
}
function fit(){""")
    rep("  const o = e.target.closest('.opt'); if(!o) return;", "  if(!Q[S.i].a) return;\n  const o = e.target.closest('.opt'); if(!o) return;")
page.write_text(s, encoding="utf-8")
print("ok", len(s))
