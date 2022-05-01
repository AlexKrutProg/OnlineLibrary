OnlineLibrary - онлайн библиотека

Основной функционал для пользователя:
1. Регистрация
2. Вход
3. Выход
4. Основная страница - просмотр всех существующих книг (если книги нет в личной библиотеке, её можно добавить, если есть - открыть прочтение ), переход на страницу просмотра книги.
5. Страница просмотра книги
6. Страница чтения книги
7. Страница профиля

Основной функционал для администратора:
*Для добавления прав ползователя как администратора, ему нужно поставить поле is_admin=true в db.
1. Страница администратора (/admin) - добавление новых книг (нужно внести html файл с текстом книги), добавление новых авторов (создается как отдельный класс - это позволит в будущем добавить например фильтрацию по автору, если необходимо), привязка автора к книге, добавление/удаление книжек из библиотек пользователей.

1.1 Создание новой книги: открыть раздел Book/создать, вписать название и прикрепить файлик с книгой, остальные поля оставить пустыми - они заполняться автоматически.
1.2 Создание автора: Author/создать.
1.3 Добавление автора: Authorship/создать - выбрать книгу, выбрать автора.
1.4 Usage - тоже самое, отвечает за нахождение книгу у пользователя.

Запуск:
В репозитории лежит виртуальное окружение, база данных с администратором (admin, пароль-12345), набор из нескольких книг.
1. Запустить виртуальное окружение (source venv/bin/activate)
2. Запустить приложение (flask run).