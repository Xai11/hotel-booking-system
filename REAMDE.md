# Hotel-booking-system
Hotel-booking system - это веб-приложение для бронирования номеров одной сети гостиниц.
Приложение позволяет пользователям просматривать список доступных отелей,  
их комнаты и свободные даты, а также бронировать комнаты онлайн.
## Фукнциональность
- Просмотр списка доступных отелей с их подробной информацией, включая адрес, рейтинг и описание.
- Просмотр списка комнат в выбранном отеле и их свободных дат.
- Бронирование комнаты на выбранные даты.
- Отображение сообщений об ошибках и успешных действиях, таких как успешное бронирование комнаты.
## Требования
- Python 3.12
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
## API Endpoints
Все эндпоинты описаны с помощью Swagger.  
Для этого необходимо запустить проект и перейти по [ссылке](http://127.0.0.1/docs)
### Бронирование комнат
-  GET /booking/ : Получить список всех бронирований с опциональными параметрами поиска (имя гостя,  
дата заезда, дата выезда, статус бронирования).
- GET /bookings/{booking_id}: Получить информацию о конкретном бронировании по его идентификатору.
- POST /bookings/: Создать новое бронирование.
- PUT /bookings/{booking_id}: Обновить информацию о конкретном бронировании по его идентификатору.
- DELETE /bookings/{booking_id}: Удалить конкретное бронирование по его идентификатору.
### Комнаты
- GET /rooms/{hotel_id}: Получить список всех номеров в отеле с опциональными параметрами поиска  
(номер комнаты, вместимость гостей).
- GET /rooms/{hotel_id}/{room_id}: Получить информацию о конкретном номере в отеле по его идентификатору.
- POST /rooms/: Создать новый номер.
- PUT /rooms/{hotel_id}/{room_id}: Обновить информацию о конкретном номере в отеле по его идентификатору.
- DELETE /rooms/{hotel_id}/{room_id}: Удалить конкретный номер в отеле по его идентификатору.
### Отели
- GET /hotels/: Получить список всех отелей с опциональными параметрами поиска (название, рейтинг, адрес).
- GET /hotels/{hotel_id}: Получить информацию о конкретном отеле по его идентификатору.
- POST /hotels/: Создать новый отель.
- PUT /hotels/{hotel_id}: Обновить информацию о конкретном отеле по его идентификатору.
- DELETE /hotels/{hotel_id}: Удалить конкретный отель по его идентификатору.