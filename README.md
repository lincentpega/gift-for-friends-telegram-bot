# Бот Gift for a Friend
Для запуска надо склонировать репозиторий

Для того, чтобы репозиторий склонировался, т.к. он закрытый надо будет ввести токен, которые можно создать на гитхабе выполнив последовательность действий:

Иконка профиля -> Settings -> Developer settings -> Personal access token -> Tokens(classic) -> Generate new token -> Generate new token (classic) -> Указать название -> галочка на repo -> Generate token и записать его куда нибудь (он больше не появится), ну или каждый раз создавать новый
```shell
git clone https://github.com/lincentpega/gift-for-friends-telegram-bot.git
```

Если нет докера, то надо его установить. Гайд для Windows по [ссылке](https://docs.docker.com/desktop/install/windows-install/).

Для запуска бота надо зайти в консоль, перейти в склонированный с гитхаба репозиторий и ввести в консоли:
```shell
docker compose up -d --build
```

Можно проверять бота

