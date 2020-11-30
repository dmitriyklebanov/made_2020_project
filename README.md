# Telegram-канал "Нейро Пирожки"
Telegram-канал с постами, автоматически генерируемым нейронной сетью. Контент – четверостишья, известные как «пирожки». Примером является канал [@pirozhki_page](https://t.me/pirozhki_page).

Похожие каналы: [@NeuralShit](https://t.me/NeuralShit), [@cooktech](https://t.me/cooktech), [@neuralmachine](https://t.me/neuralmachine).

Используемые технологии:
* pytorch
* aiogram
* docker
* google colab
* gpt-2

## Использование
Для использования бота необходимо создать файл bot-variables.env и добавить туда следующие переменные окружения:
* BOT_TOKEN, CHANNEL_ID - настройки бота
* MIN_TIME, MAX_TIME - границы минимального и максимального времени ожидания, перед отправкой сообщения в канал
* LENGTH, TEMPERATURE - параметры модели (рекомендуемые - 40, 0.9 соответственно)

Для сборки образа и запуска контейнера с ботом:
```bash
docker-compose up -d
```