# Конвенции относительно кода
## Комментарии
1. Комментарии пишем на **ГРАМОТНОМ** английском
2. На комментарии не скупимся, но не комментируем очевидные вещи. Смотрим на код со стороны разработчика, который видит его впервые, и думаем, нужно ли его объяснять
3. В комментариях используем теги:
    - `TODO`: Something to do later
    - `FIXME`: Used to highlight a known issue or bug in the code that needs to be fixed.
    - `BUG`: Similar to FIXME, denotes the presence of a bug in the code.
    - `HACK`: Indicates a temporary or workaround solution in the code that may not be ideal but serves a purpose.
    - `OPTIMIZE`: Points out a section of code that could be improved for better performance or efficiency.
    - `NOTE`: General purpose note to provide additional context or information about the code.
    - `IDEA`: Indicates a suggestion or potential improvement for future development.
    - `REFACTOR`: Suggests that a particular section of code should be refactored for better structure or readability.
    - `REVIEW`: Signifies that the code or a particular section of it needs to be reviewed by other team members.
    - `DOC`: Indicates that documentation needs to be added or updated for a specific part of the code.
    - `DEPRECATED`: Marks a feature or functionality that is no longer recommended for use and will likely be removed in future versions.

    *пример: `TODO: Implement parallel execution`*

    *пример: `OPTIMIZE: Unify DB calls for multiple entities`*
4. Для ВСЕХ методов и классов пишем комментарии в формате языка (`"""` в Python, `///` в C#). Описываем, что делает метод, какие аргументы принимает, какие ошибки может выбрасывать и какой результат возвращает
5. Очень полезно использовать комментарии чтобы передать какую-то информацию другим разработчикам (*пример: `// NOTE: userSession here is readonly and shall not be modified`*)

## SOLID / архитектура
Следуем принципам SOLID, продумываем код наперед.

**ЕЩЕ РАЗ ПОВТОРЮ, СЛЕДУЕМ ПРИНЦИПАМ SOLID, ВСЕМ ОБЯЗАТЕЛЬНО ИХ ИЗУЧИТЬ**

## Юнит-тесты
1. Пишем юнит-тесты для кода
2. Используем инструменты для замера code-coverage. Стремимся к 100%
3. Создаем тесты для проверки работы функционала кода
4. Создаем тесты для крайних случаев, когда может сломаться код (например, принимаем число в виде строки. Проверяем пустую строку, null/None, отрицательное число, дробное число, т.д. т.п.)
5. **НЕ КОММИТИМ ЕСЛИ ТЕСТЫ НЕ ПРОХОДЯТ**. В крайнем случае можно закоммитить, но ни в коем случае не мержить в основную ветку. В идеале в таких случаях писать TODO, FIXME и т.п.

## Форматирование
1. Слушаемся специфичных для языка конвенций
2. Используем авто-линтеры (`ruff` для Python, `dotnet format` для C#)
3. Слушаемся инструментов языка (`PEP8/ruff` для Python, `IntelliSense` для C#)
4. Минимизируем предупреждения компилятора, линтера и т.п.
5. Сами тоже следим, чтобы код выглядел опрятно и красиво
6. С помощью пустых строк разбиваем код на логические блоки или группы действий. Обязательно

## API
1. Помним, что с нашим кодом работают другие разработчики. Если уже построили контракт API, не нарушаем его (не переименовываем методы, эндпоинты, т.п.). В общем - не ломаем чужой код, который может основываться на нашем

## Микросервисы/Docker
1. Помним, что работаем в специфике микросервисной архитектуры и контейнеров
2. Никаких URL типа `localhost`, `127.0.0.1` и т.п., используем подсеть докера и DNS

## Зависимости
1. Перед внедрением любой библиотеки обязательно собираемся и обсуждаем, действительно ли она нужна и как это может повлиять на проект