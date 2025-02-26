 Goroskopbot @Gorouskop_bot
=
>Этот бот создан для просмотра гороскопа. С его помощью можно узнать, что звезды предсказывают для вашего знака зодиака на ближайшее время. Бот работает очень просто: достаточно добавить его в свой список контактов в Telegram и отправить запрос с указанием своего знака зодиака. В ответ вы получите прогноз, включающий информацию о том, какие события могут произойти в вашей жизни, как лучше всего поступить в той или иной ситуации, а также советы по улучшению отношений с окружающими людьми. Кроме того, этот бот может предложить вам рекомендации по здоровью, карьере, любви и другим важным аспектам жизни. Так что если вы хотите всегда быть в курсе того, что вас ждет впереди, попробуйте воспользоваться этим удобным и полезным ботом!

Команды:
-
- /set_sign (Выводит кнопки со знаками зодиака)
- /start (Команда для взаимодействия с ботом)
- /help (Выводит список всех доступных команд)
- /stats (Выводит статистику по знакам зодиака)
- /history (История всех запросов пользователя связанных с гороскопом)
- /clearhistory (Очищает всю историю пользователя)
- /today (Отправляет гороскоп на сегодня, для указанного знака зодиака командой /set_sign)
- /tomorrow (Аналогично, как и с командой /today, но данная команда показывает гороскоп на завтра)

Пример использования:
-
1. Отправьте команду /start, чтобы использовать бота.
2. Используйте команду /set_sign чтобы выбрать знак зодиака, вы можете также его сменить, этой же командой.
3. Далее команду /stats чтобы узнать, какой знак зодиака широко используется(популярен) среди пользователей.


Установка:
-

1. Скопируйте репозиторий.

       git clone https://github.com/DaniilFinch/TGBOT

       cd TGBOT

3. Для того чтобы запустить бота, вам необходимо установить следующие библиотеки:

       pip install pyTelegramBotAPI

       pip install requests

       pip install beautifulsoup4
   
       pip install telebot
   
Модули:
-

> telebot — Создание и управление Telegram-ботом..<br/>
> requests — Отправка HTTP-запросов (запросы к веб-сайтам)<br/>
> bs4 (Beautiful Soup) — Парсинг HTML и XML (извлечение данных из веб-страниц)<br/>
> json — Работа с данными в формате JSON (чтение и запись).<br/>
> datetime — Работа с датами и временем.<br/>
> timedelta — Представление разницы между датами и временем.<br/>
> types (из telebot) — Типы объектов Telegram API (клавиатуры, кнопки и т.д.).<br/>
> collections.Counter — Подсчет количества элементов в списке.<br/>

3. Замените в коде токен:

>В файле main.py замените BOT_TOKEN = "здесь ваш токен" на свой токен.
>Вместо слов здесь ваш токен, заменить на то, что вы получили у BOTFATHER(@BotFather).
4. Запуск бота

       python main.py
