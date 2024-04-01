# Документация проекта FastAPI для нахождения оптимального пути по точкам

## Описание проекта

Этот проект представляет собой API для нахождения оптимального пути между заданными точками на карте. Проект разработан с использованием FastAPI и применяет n-layer паттерн проектирования для обеспечения модульности и масштабируемости.

## Установка

Для установки необходимо выполнить следующие шаги:

1. Клонировать репозиторий проекта:
   ``git clone https://github.com/HiRurgLipay/OptiRoute``
2. Установить зависимости:
   ``pip install -r requirements.txt``

## Запуск

Для запуска API выполните следующие команды:

`uvicorn main:app --reload`

API будет доступно по адресу [http://127.0.0.1:8000]()

## Использование

### Получение списка точек

1. Для получения списка точек отправьте GET запрос на `/points`.
2. Перейдите по `http://127.0.0.1:8000/docs`.
3. Выберите `GET` запрос из `Swagger`, нажмите `Try it on` и введите `id` маршрута.
4. Так же вы можете настроить пагинацию (сколько точек показывать на странице и выбор самой страницы)
5. Спустя некоторое время вы увидете ответ в формате `JSON` с координатами точек.

### Добавление новой точки

1. Чтобы рассчитать новый оптимальный маршрут, отправьте `POST` запрос на `/points`, конкретно `CSV` файл.
2. Перейдите по `http://127.0.0.1:8000/docs`.
3. Выберите `POST` запрос из `Swagger`, нажмите `Try it on` и выберите `CSV` файл.
4. Спустя некоторое время вы увидете ответ в формате `JSON` с оптимальным маршрутом из точек.
5. Так же, вы можете увидеть загрузочную полоску в вашем Терминале которая показывает обработку вашего `CSV` файла

Примеры `CSV` файлов находится в корневой дирректории проекта.

## Архитектура

### Слои приложения:

1. **Презентационный слой (Presentation Layer)** :

* Отвечает за взаимодействие с клиентами посредством API.
* Включает в себя контроллеры и роутер.

  2. **Бизнес-логика (Business Logic Layer)** :**
* Обрабатывает запросы, валидирует данные и управляет бизнес-процессами.
* Реализует бизнес-правила и алгоритмы, связанные с нахождением оптимального пути.

3. **Слой доступа к данным (Data Access Layer)** :

* Взаимодействует с базой данных, настраиваем сессии, включает механизм миграции и модели данных.
* Обеспечивает доступ к точкам и сохраняет изменения.

### API

* **GET /points** : Получить список всех точек.
* **POST /points** : Добавить новую точку.

## Описание реализации функционала

### Business_logic:

**business_logic/csv_service.py:**

* `read_csv` - cчитывает содержимое CSV-файла и возвращает список объектов Point.

**business_logic/nearest_neighbor_service.py**

* `calculate_distance` - функция вычисляет расстояние между двумя точками с использованием евклидова расстояния. Это расстояние используется для определения ближайшей точки к текущей в функции `find_closest_point`.
* `find_closest_point` - функция находит ближайшую точку к текущей точке. Она использует функцию `calculate_distance`, чтобы определить расстояние между текущей точкой и всеми оставшимися точками, а затем выбирает ту, которая наименее удалена.
* `optimize_route` - функция оптимизирует маршрут, используя алгоритм ближайшего соседа. Она начинает с первой точки в списке и находит ближайшую к ней точку. Затем она добавляет эту точку в маршрут и продолжает этот процесс, пока не будут пройдены все точки.

### Data_access:

**Alembic** (data_access/alembic) - механизм для миграцияя SQLAlchemy.

**DataBase:**

* data_access/database/database.py - модуль включает в себя , настройку сессий и создание асинхронного движка для работы с базой данных PostgreSQL.

**Models:**

* data_access/database/models.py - модуль содержит определения моделей данных для точек маршрута и маршрутов в базе данных. Он использует SQLAlchemy для создания сопоставлений между объектами Python и таблицами в базе данных.

Session:

* data_access/database/session.py - файл содержит функцию для получения асинхронного сеанса с базой данных. Он использует `async_session` из модуля `data_access.database.database` для создания асинхронной сессии SQLAlchemy.

### Presentation:

**presentation/controllers/route_controller.py:**

* `upload_file` - функция обрабатывает загрузку CSV файла с точками маршрута для создания нового маршрута. Загруженный файл анализируется для извлечения точек маршрута, затем маршрут оптимизируется, создается объект маршрута в базе данных и возвращается оптимизированный маршрут в формате JSON.
* `get_route_by_id` - функция получает маршрут по его уникальному идентификатору из базы данных. После получения маршрута, точки маршрута оптимизируются с учетом параметров пагинации, и возвращается пагинированный результат.

**presentation/router.py** - инициализация и настройка роутера.

### test_optimize_route:

Небольшой тест как описано в ТЗ

## Недостатки:

В силу нехватки времени и большой занятости не успел реализовать некоторый функционал

1. Нет логгирования (его просто реализовать)
2. Небольшая трудность для Front-End разработчиков будет то что в ответе в Swagger выводится тип данных string (так же просто реализовать)
3. Нет достаточного количества тестов

## Лицензия

Этот проект лицензируется по [MIT License]().