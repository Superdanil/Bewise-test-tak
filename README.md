# Bewise-test-task
Тестовое задание Junior

Описанный ниже старт программы предназначен для систем Linux и версии python 3.10. На других ОС запуск не тестировался.

Старт
1. git clone https://github.com/Superdanil/Bewise-test-task
2. Создаем виртуальное окружение командой python3 -m venv venv
3. Активируем виртуальное окружение командой source venv/bin/activate
4. Устанавливаем зависимости: pip install -r requirements.txt
5. Освободите порт 5432
6. Разворачиваем контейнер БД на Postgresql: docker-compose up --build
7. Запускаем контейнер: docker-compose start
8. Запускаем приложение: python3 main.py
9. Переходим по ссылке: http://127.0.0.1:8000/docs
10. Пост-запрос -> Try it out
11. В обязательно поле пост-запроса вводим любое целое число от 1 до 100
12. Execute :)
13. Также для дополнительного удобства реализованы get и delete запросы
