# Справочники значений

Списки допустимых значений, которые используются в нескольких методах API онлайн-чата Talk-Me.

## Тип сообщения

Используется в полях: `messageType`.

* `` - Реальное сообщение
* `comment` - Системный комментарий
* `operatorComment` - Комментарий оператора
* `futureNotify` - Будущее напоминание
* `autoForward` - Автоматическое переключение на другого оператора
* `autoForwardOffline` - Автоматическое переключение Offline-вопроса на оператора
* `initiate` - Оператор инициировал диалог
* `simulated` - Имитация разговора
* `sms` - Ответ отправлен через SMS
* `viber` - Ответ отправлен через Viber
* `whatsapp` - Ответ отправлен через Whatsapp
* `mailru` - Ответ отправлен через VK
* `email` - Ответ отправлен через Email
* `messengerAggregator` - Ответ отправлен через агрегатора
* `autoMessage` - Автоматическое приветствие
* `supportAPI` - Отправка с помощью Javascript API
* `forward` - Переключение на другого оператора
* `forwardHidden` - Переключение на другого оператора (скрытое)
* `unsubscribe` - Отписка
* `notification` - Системное уведомление
* `rithoricQuestion` - Обращение не требует ответа
* `acceptDialog` - Оператор принял диалог
* `setActiveDialogStatus` - Изменение статуса диалога
* `closeDialog` - Диалог завершён
* `autoCloseDialog` - Диалог завершён автоматически
* `reopenDialog` - Диалог перезапущен
* `tab` - Вкладка
* `tip` - Запрос чаевых
* `requestContact` - Запрос контакта
* `cabinetSender` - Рассылка из личного кабинета
* `operatorRunBot` - Оператор запустил бота
* `bot` - Бот
* `integrationStart` - Старт интеграции
* `integrationStop` - Интеграция остановлена
* `integrationCallSuccess` - Успешный звонок
* `integrationCallFailed` - Неуспешный звонок
* `webRTCCallStart` - Начался звонок
* `webRTCCallUpdate` - Обновились данные звонка
* `webRTCCallError` - Ошибка во время звонка
* `webRTCCallStop` - Звонок завершён

## Эмоции клиента (AI-анализ диалога)

Используется в полях: `ai.clientEmotionId`.

Возможные значения:

* **2** (Позитивные)
* **1** (Нейтральные)
* **0** (Негативные)

## Идентификаторы каналов

Используется в полях: `client.sourceIds`, `sourceIds`.

`site` - Сайт
`max` - Max
`whatsappOfficial` - WhatsApp
`telegram` - Telegram
`viber` - Viber
`slack` - Slack
`fbGroup` - Facebook + Instagram
`vkGroup` - VK
`okGroup` - OK
`email` - Email
`ozon` - Ozon
`wb` - Wildberries
`domclick` - Домклик
`cian` - Циан
`avito` - Avito
`youla` - Юла
`aliExpress` - AliExpress
`autoru` - Auto.ru
`drom` - Дром
`tgcars` - tgcars
`wazzup` - Wazzup
`greenApi` - Green API
`wammchat` - Wamm.chat
`onlineChatRest` - REST API
`megafon` - Мегафон
`zadarma` - Zadarma
`telphin` - Телфин
`novofon` - Новофон
`mangoOffice` - Mango Office
`mcn` - MCNtelecom
`altegro` - Altegro
`moizvonki` - Мои Звонки

## Пакеты лицензий (batchId)

Используется в полях: `batchId`, `result.licenseList[].batchId`.

Для typeId `period`:

* `1` - 1 день
* `31` - 1 месяц
* `91` - 3 месяца
* `182` - 6 месяцев
* `365` - 1 год
* `730` - 2 года

Для typeId `pack`:

* `1` - 10 обращений
* `2` - 20 обращений
* `3` - 30 обращений
* `4` - 40 обращений
* `5` - 50 обращений
