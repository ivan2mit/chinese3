# Макет кабинета участника олимпиады (ЦСК)

- `olympiad.html` — самодостаточный макет (один файл): вход, выбор теста, проверка звука, окно теста со всеми типами заданий.
- `hz/` — задания по иероглифам (hz-*): `hz.js` (плеер, собран esbuild из `animcjk-task-editor/exercises/olympiad-bridge.js`), `hz.css` (`player.css`), `hzq.json` (`exercises/demo/questions.json`).
- `build-hz.py` — встраивает/обновляет блоки hz в `olympiad.html` (первый запуск правит код кабинета, повторные обновляют блоки между маркерами `hz:css` и `hz:js`).
- `backups/` — снимки `olympiad.html` перед правками.

Локально: `python3 -m http.server 8765` в этой папке, затем http://localhost:8765/olympiad.html (микрофон работает только на localhost или HTTPS).
Опубликованная копия: https://claude.ai/artifact/JfimhX8oXqD7KXHXqNKBzK
