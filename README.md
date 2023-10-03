# Проект на Django rest framework "BookStore".

## Как запустить проект
#### 1. Клонировать проект: <br>
```git clone https://github.com/MaksimLogvinov/DRF-BookStore.git```
#### 2. Заполнить .env файл. Пример заполненного файла - [.env-example](https://github.com/MaksimLogvinov/DRF-BookStore/tree/main/Books/.env-example)
#### 3. Настроить smtp (рассылка сообщений на почту). [Помощь](https://firstvds.ru/technology/yandex-mail-for-domain)
#### 4. Создать миграции: <br>
```python manage.py makemigrations ```
#### 3. Применить миграции: <br>
```python manage.py migrate ```       
#### 4. Запустить проект: <br>
```python manage.py runserver ```

## Где найти доступные url адреса 
- #### Перейти по http://127.0.0.1:8000/swagger
- #### В каждом приложении найдите файл urls.py, в котором прописана навигация. <br> Вот несколько из них: [Books](https://github.com/MaksimLogvinov/DRF-BookStore/blob/main/Books/Books/urls.py), [Users](https://github.com/MaksimLogvinov/DRF-BookStore/blob/main/Books/apps/users/urls.py), [Categories](https://github.com/MaksimLogvinov/DRF-BookStore/blob/main/Books/apps/categories/urls.py)

## Функционал сайта
1. #### Регистрация пользователей, с подтверждением по почте
2. #### Аутентификация и авторизация
3. #### Возможность смены пароля с валидацией по почте
4. #### Расширенный профиль пользователя
5. #### Корзина с возможностью добавления, удаления, обновления количества товаров
6. #### Создание заказов
7. #### Бронирование заказов
8. #### Рассылка различных сообщений о действиях пользователя на сайте
9. #### Административная панель с возможностью скачать данные
10. #### Каталог товаров с фильтрацией результатов
11. #### Поиск товаров по ключевым словам

