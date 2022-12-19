# Foodrgam

 Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект реализован на `Django` и `DjangoRestFramework`. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием `Redoc`.

<span style="color:red">**Проект находится в стадии разработки!**</span>

## Особенности реализации

- Проект завернут в Docker-контейнеры;
- Будет Реализован workflow;
- Проект будет развернут на удаленном сервере;

## Развертывание проекта

### Развертывание на локальном сервере

1. Установите на сервере `docker` и `docker-dompose`.
2. Создайте файл `/infra/.env`. Шаблон для заполнения файла нахоится в `/infra/.env.example`.
3. Выполните команду `docker-compose up -d --buld`.
4. Выполните миграции `docker-compose exec web python manage.py migrate`.
5. Создайте суперюзера `docker-compose exec web python manage.py createsuperuser`.
6. Соберите статику `docker-compose exec web python manage.py collectstatic --no-input`.
7. Заполните базу ингредиентами `docker-compose exec web python manage.py load_ingredients`.
8. Документация к API находится по адресу: <http://localhost/api/docs/redoc.html>.

## Автор

 Андрей Плотников (Andy.Plo@yandex.ru)

[![Django-app workflow](https://github.com/AndyPlo/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/AndyPlo/yamdb_final/actions/workflows/yamdb_workflow.yml)
