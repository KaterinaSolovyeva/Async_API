## Как запустить проект:
Создайте env файл в той же директории, где описан его example файл

Запустите docker-compose командой:
```
docker-compose up -d
```
Создайте миграции и соберите статику командой:
```
make setup
```
Загрузите первоначальные данные из sqlite в postgres командой. После этого сработает сервис ETL
(Данные необходимо занести за 10 минут, иначе сервис ETL умрет (т.к. получит критическое кол-во ошибок для работы))
на загрузку в ElasticSearch:
```
make load_data
```
Создайте суперпользователя Django:
```
make admin
```
Команда для подключения к серверу redis:
```
make redis
```
## Запуск в браузере
- Открытие административного сайта - http://127.0.0.1:80/admin/
- Api - http://127.0.0.1:80/api/v1/
- Страница с документацией http://127.0.0.1:80/api/openapi


### Над проектом работали:

https://github.com/Vatson76

- Настроить докерфайл и докеркомпоуз
- Доработать ETL для записи в ES данных жанров
- Доработать ETL для записи в ES данных персоналий
- Написать сервисы для получения информации об персоналиях и жанрах

https://github.com/KaterinaSolovyeva - тимлид

- Создать репозиторий, дать в него доступы
- Создать базовую структуру приложения
- Создать модели для фильмов и связанных данных
- Написать сервис для получения информации о фильмах
- Кеширование данных в Redis
