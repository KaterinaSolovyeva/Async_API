# Асинхронный API для кинотеатра
### Используемые технологии:

- Код приложения пишется на Python + FastAPI.
- Приложение запускается под управлением сервера ASGI(uvicorn).
- В качестве хранилища используется ElasticSearch.
- Для кеширования данных понадобится Redis Cluster.
- Все компоненты системы запускаются через Docker.
### Основные сущности

- Фильм — заголовок, содержание, дата создания, возрастной ценз, режиссёры, актёры, сценаристы, жанры, ссылка на файл.
- Сериал — заголовок, содержание, даты создания, режиссёры, актёры, сценаристы, жанры, ссылка на файл.
- Актёр — имя, фамилия, фильмы с его участием.
- Режиссёр — имя, фамилия, фильмы, которые он снял.
- Сценарист — имя, фамилия, фильмы по его сценариям.
- Жанр — описание, популярность.
### Особенности проекта:

- Время ответа сервиса не превышает 200 мс.
- В сервисе решена проблема 10к соединений.
- 200 000+ фильмов.
- 200 000+ сериалов.
- 100+ жанров
## Эндпоинты

**1. Главная страница.** 
- На ней выводятся популярные фильмы. В качестве критерия популярности — imdb_rating.
```
/api/v1/films?sort=-imdb_rating

  http request
  GET /api/v1/films?sort=-imdb_rating&page[size]=50&page[number]=1
  [
  {
    "uuid": "uuid",
    "title": "str",
    "imdb_rating": "float"
  },
  ...
  ]

  [
  {
    "uuid": "524e4331-e14b-24d3-a156-426614174003",
    "title": "Ringo Rocket Star and His Song for Yuri Gagarin",
    "imdb_rating": 9.4
  },
  {
    "uuid": "524e4331-e14b-24d3-a156-426614174003",
    "title": "Lunar: The Silver Star",
    "imdb_rating": 9.2
  },
  ...
  ]
```
- Жанр и популярные фильмы в нём. Это фильтрация.
```
/api/v1/films?sort=-imdb_rating&filter[genre]=<comedy-uuid>

http request
GET /api/v1/films?filter[genre]=<uuid:UUID>&sort=-imdb_rating&page[size]=50&page[number]=1
[
{
  "uuid": "uuid",
  "title": "str",
  "imdb_rating": "float"
},
...
]

[
{
  "uuid": "524e4331-e14b-24d3-a156-426614174003",
  "title": "Ringo Rocket Star and His Song for Yuri Gagarin",
  "imdb_rating": 9.4
},
{
  "uuid": "524e4331-e14b-24d3-a156-426614174003",
  "title": "Lunar: The Silver Star",
  "imdb_rating": 9.2
},
...
]
```
- Список жанров.
```
/api/v1/genres/

http request
GET /api/v1/genres/
[
{
  "uuid": "uuid",
  "name": "str",
  ...
},
...
]

[
{
  "uuid": "d007f2f8-4d45-4902-8ee0-067bae469161",
  "name": "Adventure",
  ...
},
{
  "uuid": "dc07f2f8-4d45-4902-8ee0-067bae469164",
  "name": "Fantasy",
  ...
},
...
]
```
**2. Поиск**
- Поиск по фильмам.
```
/api/v1/films/search/

  http request
GET /api/v1/films/search?query=captain&page[number]=1&page[size]=50
[
{
  "uuid": "uuid",
  "title": "str",
  "imdb_rating": "float"
},
...
]

[
{
  "uuid": "223e4317-e89b-22d3-f3b6-426614174000",
  "title": "Billion Star Hotel",
  "imdb_rating": 6.1
},
{
  "uuid": "524e4331-e14b-24d3-a456-426614174001",
  "title": "Wishes on a Falling Star",
  "imdb_rating": 8.5
},
...
]
```

- Поиск по персонам.
```
/api/v1/persons/search/

http request
GET /api/v1/persons/search?query=captain&page[number]=1&page[size]=50
[
{
  "uuid": "uuid",
  "full_name": "str",
  "role": "str",
  "film_ids": ["uuid"]
},
...
]
[
  {
    "uuid": "724e5631-e14b-14e3-g556-888814284902",
    "full_name": "Captain Raju",
    "role": "actor",
    "film_ids": ["eb055946-4841-4b83-9c32-14bb1bde5de4", ...]
 },
]
```
**3. Страница фильма**
- Полная информация по фильму.
```
 /api/v1/films/<uuid:UUID>/

  http request
GET /api/v1/films/<uuid:UUID>/
{
"uuid": "uuid",
"title": "str",
"imdb_rating": "float",
"description": "str",
"genre": [
  { "uuid": "uuid", "name": "str" },
  ...
],
"actors": [
  {
    "uuid": "uuid",
    "full_name": "str"
  },
  ...
],
"writers": [
  {
    "uuid": "uuid",
    "full_name": "str"
  },
  ...
],
"directors": [
  {
    "uuid": "uuid",
    "full_name": "str"
  },
  ...
],
}

{
"uuid": "b31592e5-673d-46dc-a561-9446438aea0f",
"title": "Lunar: The Silver Star",
"imdb_rating": 9.2,
"description": "From the village of Burg, a teenager named Alex sets out to become the fabled guardian of the goddess Althena...the Dragonmaster. Along with his girlfriend Luna, and several friends they meet along the journey, they soon discover that the happy world of Lunar is on the verge of Armageddon. As Dragonmaster, Alex could save it. As a ruthless and powerful sorceror is about to play his hand, will Alex and company succeed in their quest before all is lost? And is his girlfriend Luna involved in these world shattering events? Play along and find out.",
"genre": [
  {"name": "Action", "uuid": "6f822a92-7b51-4753-8d00-ecfedf98a937"},
  {"name": "Adventure", "uuid": "00f74939-18b1-42e4-b541-b52f667d50d9"},
  {"name": "Comedy", "uuid": "7ac3cb3b-972d-4004-9e42-ff147ede7463"}
],
"actors": [
  {
    "uuid": "afbdbaca-04e2-44ca-8bef-da1ae4d84cdf",
    "full_name": "Ashley Parker Angel"
  },
  {
    "uuid": "3c08931f-6138-46d1-b179-1bd076b6a236",
    "full_name": "Rhonda Gibson"
  },
  ...
],
"writers": [
  {
    "uuid": "1bd9a00b-9596-49a3-afbe-f39a632a09a9",
    "full_name": "Toshio Akashi"
  },
  {
    "uuid": "27fc3dc6-2656-43cb-8e56-d0dfb75ea0b2",
    "full_name": "Takashi Hino"
  },
  ...
],
"directors": [
  {
    "uuid": "4a893a97-e713-4936-9dd4-c8ca437ab483",
    "full_name": "Toshio Akashi"
  },
  ...
],
}
```
**4. Страница персонажа**
- Данные по персоне.
```
/api/v1/persons/<uuid:UUID>/
  http request
GET /api/v1/persons/<uuid:UUID>
{
"uuid": "uuid",
"full_name": "str",
"role": "str",
"film_ids": ["uuid"]
}

{
"uuid": "524e4331-e14b-24d3-a456-426614174002",
"full_name": "George Lucas",
"role": "writer",
"film_ids": ["uuid", ...]
}
```
- Фильмы по персоне.
```
/api/v1/persons/<uuid:UUID>/film/

http request
GET /api/v1/persons/<uuid:UUID>/film
[
{
  "uuid": "uuid",
  "title": "str",
  "imdb_rating": "float"
},
...
]

[
{
  "uuid": "524e4331-e14b-24d3-a456-426614174001",
  "title": "Star Wars: Episode VI - Return of the Jedi",
  "imdb_rating": 8.3
},
{
  "uuid": "123e4317-e89b-22d3-f3b6-426614174001",
  "title": "Star Wars: Episode VII - The Force Awakens",
  "imdb_rating": 7.9
},
...
]
```
**5. Страница жанра**
- Данные по конкретному жанру.
```
/api/v1/genres/<uuid:UUID>/

http request
GET /api/v1/genres/<uuid:UUID>
{
"uuid": "uuid",
"name": "str",
...
}

{
"uuid": "aabbd3f3-f656-4fea-9146-63f285edf5с1",
"name": "Action",
...
}
```
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
- Создание административного сайта в Django
- Написать сервис для получения информации о фильмах
- Кеширование данных в Redis
