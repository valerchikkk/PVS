from typing import Dict, Union, List, Any
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import datetime
import time
import matplotlib.pyplot as plt


# ВСТАВЬТЕ ЗАМЕСТО "e27c***65c3" ВАШ ТОКЕН API OpenWeather
open_weather_token = 'e27c***65c3'

# ЗАМЕНИТЕ '6653***uldw' НА ВАШ ТОКЕН, ПОЛУЧЕННЫЙ ОТ BotFather В Telegram
tg_bot_token = '6653***uldw'


open_weather_token: str = f'{open_weather_token}'

bot = TeleBot(f'{tg_bot_token}')

# Словарь для соответствия кода погоды с эмодзи
code_to_smile: Dict[str, str] = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain" : "Дождь \U00002614" ,
    "Drizzle": "Дождь \U0001F327",
    "Thunderstorm" : "Гроза \U000026A1",
    "Snow": "Снег \U00002744",
}

# Словарь для хранения данных о мониторинге погоды
weather_monitoring: Dict[int, Dict[str, Union[str, float, bool]]] = {}

#Функция получения значений о погоде или графике в зависимости от выбора пользователя
def get_weather(city: str, open_weather_token: str, user_action: int, chat_id: int) -> None:
    if user_action == 1:
        try:
            r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru')
            data = r.json()
            
            city = data["name"]
            cur_weather = data["main"]["temp"]
            
            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму, что там за погода!"
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = sunset_timestamp - sunrise_timestamp
            bot.send_message(chat_id, f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                  f"Погода в городе {city}\nТемпература: {cur_weather}°C {wd}\n"
                  f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n"
                  f"Ветер: {wind} м/с\nВосход солнца: {sunrise_timestamp}\n"
                  f"Закат солнца:{sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n***Хорошего дня!***"
                  )
        except Exception as ex:
            bot.send_message(chat_id, f"Ошибка: {ex}\nПроверьте название города")
            
    if user_action == 2:
        try:
            r = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_weather_token}&units=metric&lang=ru')
            data = r.json()
            
            city = data["city"]["name"]
                
            result_dict = create_dict_with_temp(data)
            dates = []
            temperatures = []
            
            
            for date, data in result_dict.items():
                for hour, temp in data.items():
                    # Составляем дату и час в формате "YYYY-MM-DD HH:MM"
                    datetime_str = f"{date} {hour}"
                    # Преобразуем строку в объект datetime
                    datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                    dates.append(datetime_obj)
                    temperatures.append(temp)
            
            plot = plt.plot(dates, temperatures, marker='o', linestyle='-', color = 'b')
            plot = plt.title(f'График температуры на 5 дней в городе {city}')
            plot = plt.xlabel('Дата и время')
            plot = plt.ylabel('Температура (°C)')
            plot = plt.xticks(rotation=45, ha='right')
            plot = plt.grid(True)
            plt.tight_layout()
            plot = plt.tight_layout()
            
            plot = plt.savefig('temperature_over_time.png', dpi=300)
                
            bot.send_message(chat_id, f"График температуры на 5 дней в городе {city}")
            with open('temperature_over_time.png', 'rb') as photo:
                bot.send_photo(chat_id, photo)
            
        except Exception as ex:
            print(ex)
            print("\U00002620 Проверьте название города \U00002620")
    

def create_dict_with_temp(data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    days = []
    hours = []
    dict_days_and_hours = {}
    list_to_append = []
    first_time = datetime.datetime.utcfromtimestamp(data["list"][0]["dt"]).strftime('%H:%M')
    for day in range (0, 41, 8):
        if day >= 40:
            if first_time == '00:00':
                break
            else:
                date_object = datetime.datetime.utcfromtimestamp(data["list"][day-1]["dt"])
                formatted_date = date_object.strftime('%Y-%m-%d')
                days.append(formatted_date)
                break
        else:
            date_object = datetime.datetime.utcfromtimestamp(data["list"][day]["dt"])
            formatted_date = date_object.strftime('%Y-%m-%d')
            days.append(formatted_date)
        
    for hour in range (40):
        date_object = datetime.datetime.utcfromtimestamp(data["list"][hour]["dt"])
        formatted_date = date_object.strftime('%H:%M')
        hours.append(formatted_date)
    every_three_hours = ['00:00','03:00','06:00','09:00','12:00','15:00','18:00', '21:00']
    flag = True
    for day in days:
        i = 0
        if flag == False and len(dict_days_and_hours) != 5:
            dict_days_and_hours[day] = every_three_hours
        elif flag == True or len(dict_days_and_hours) == 5:    
            for hourr in hours:
                if hourr == '21:00':
                    list_to_append.append(hourr)
                    del hours[:i+1]
                    break
                else:
                    list_to_append.append(hourr)
                    i += 1
            dict_days_and_hours[day] = list_to_append 
            list_to_append = []
            if len(dict_days_and_hours) != 6:
                del hours[:32]
            flag = False      
            
    
    dict_hour_temp = {}
    dict_day_hour_temp = {}
    hour_count = 0
    flag_day = 0
    for day in days:
        
        flag = 0
        
        while dict_days_and_hours.get(day)[flag] != '21:00' and flag_day == 0:
            time = dict_days_and_hours.get(day)[flag]
            dict_hour_temp[time] = data['list'][hour_count]['main']['temp']
            hour_count += 1
            flag += 1
        time = dict_days_and_hours.get(day)[flag]
        dict_hour_temp[time] = data['list'][hour_count]['main']['temp']
        hour_count += 1
        if flag_day == 0:
            dict_day_hour_temp[day] = dict_hour_temp
            dict_hour_temp = {}
        if flag_day == 5:
            flag = 1
            while dict_days_and_hours.get(day)[flag] != hours[-1]:
                time = dict_days_and_hours.get(day)[flag]
                dict_hour_temp[time] = data['list'][hour_count]['main']['temp']
                hour_count += 1
                flag += 1
            time = dict_days_and_hours.get(day)[flag]
            dict_hour_temp[time] = data['list'][hour_count]['main']['temp']
            hour_count += 1
            dict_day_hour_temp[day] = dict_hour_temp
            dict_hour_temp = {}
            flag += 1    
        elif flag_day != 0 and flag_day != 5:
            for i in range (1, 8):
                time = dict_days_and_hours.get(day)[i]
                dict_hour_temp[time] = data['list'][hour_count]['main']['temp']
                hour_count += 1
            dict_day_hour_temp[day] = dict_hour_temp
            dict_hour_temp = {}  
            
        flag_day += 1
    return dict_day_hour_temp




    
def start_monitoring(chat_id, city, threshold, direction):
    weather_monitoring[chat_id] = {
        'city': city,
        'threshold': threshold,
        'direction': direction,
        'monitoring': True,
    }
    

#Если пользователь вводит "стоп", то мониторинг прекращается
@bot.message_handler(func=lambda message: message.text.lower() == 'стоп')
def stop_monitoring(message: Message) -> None:
    chat_id = message.chat.id
    if chat_id in weather_monitoring:
        weather_monitoring[chat_id]['monitoring'] = False
        bot.send_message(chat_id, "Мониторинг погоды завершён")
        bot.send_message(
            chat_id,
            "Отправь 1, если хочешь узнать погоду в данный момент\nОтправь 2, если хочешь получить прогноз на 5 дней в виде графика\nОтправь 3, если хочешь мониторить погоду",
        )


#Регистрация порогового значения измерений
def handle_monitoring_city(message: Message) -> None:
    chat_id = message.chat.id
    city = message.text

    bot.send_message(chat_id, "Укажите пороговое значение для измерения температуры")
    bot.register_next_step_handler(message, handle_threshold, city)

#Пользователь вводит, выше или ниже должна быть температура
def handle_threshold(message: Message, city: str) -> None:
    chat_id = message.chat.id
    try:
        threshold = float(message.text)
    except ValueError:
        bot.send_message(chat_id, "Неверное значение. Пожалуйста, введите числовое значение.")
        return

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Выше", callback_data='higher'))
    markup.row(InlineKeyboardButton("Ниже", callback_data='lower'))

    bot.send_message(chat_id, "Температура должна быть выше или ниже порогового значения?", reply_markup=markup)

    weather_monitoring[chat_id] = {'city': city, 'threshold': threshold, 'monitoring': False}
    

#Процесс мониторинга   
@bot.callback_query_handler(func=lambda call: True)
def handle_monitoring_direction(call: Any) -> None: 
    chat_id = call.message.chat.id
    direction = 'higher' if call.data == 'higher' else 'lower'

    if chat_id not in weather_monitoring:
        bot.send_message(chat_id, "Что-то пошло не так. Попробуйте еще раз.")
        return

    weather_monitoring[chat_id]['direction'] = direction
    weather_monitoring[chat_id]['monitoring'] = True

    bot.send_message(chat_id, "Ожидаем изменения температуры.... Если хотите прекратить мониторинг, напишите 'стоп' без кавычек")
 

    while weather_monitoring[chat_id]['monitoring']:
        city = weather_monitoring[chat_id]['city']
        threshold = weather_monitoring[chat_id]['threshold']
        direction = weather_monitoring[chat_id]['direction']

        try:
            r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru')
            data = r.json()

            current_temp = data["main"]["temp"]
            bot.send_message(chat_id, f"Текущая погода: {current_temp}")
            if (direction == 'higher' and current_temp > threshold) or (direction == 'lower' and current_temp < threshold):
                direction = 'выше' if direction == 'higher' else 'ниже'
                bot.send_message(
                    chat_id,
                    f"В данный момент температура воздуха стала {direction} порогового значения в {threshold} градусов. Температура в данный момент: {current_temp}°C."
                )
                direction = 'higher' if direction == 'выше' else 'lower'
                weather_monitoring[chat_id]['monitoring'] = False
                break

        except Exception as ex:
            bot.send_message(chat_id, f"Ошибка при получении погоды: {ex}")

        time.sleep(600)

    bot.send_message(
        chat_id,
        "Отправь 1, если хочешь узнать погоду в данный момент\nОтправь 2, если хочешь получить прогноз на 5 дней в виде графика\nОтправь 3, если хочешь мониторить погоду",
    )

#СТАРТ БОТА
@bot.message_handler(commands=['start'])
def handle_start(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        "Отправь 1, если хочешь узнать погоду в данный момент\nОтправь 2, если хочешь получить прогноз на 5 дней в виде графика\nОтправь 3, если хочешь мониторить погоду"
    )

#Регистрация начального пользовательского ввода
@bot.message_handler(func=lambda message: message.text in ['1', '2', '3'])
def handle_user_action(message: Message) -> None:
    user_action = int(message.text)

    if user_action == 1 or user_action == 2 or user_action == 3:
        if user_action == 3:
            bot.send_message(message.chat.id, "Напишите город")
            bot.register_next_step_handler(message, handle_monitoring_city)
        else:
            bot.send_message(message.chat.id, "Введите город")
            bot.register_next_step_handler(message, handle_city, user_action)
    else:
        bot.send_message(message.chat.id, "Выберите 1, 2 или 3")

#Отправление сообщения о выборе следующего действия пользователем
def handle_city(message: Message, user_action: int) -> None:
    city = message.text

    try:
        get_weather(city, open_weather_token, user_action, message.chat.id)
    except Exception as ex:
        bot.send_message(message.chat.id, f"Ошибка: {ex}")
    bot.send_message(
        message.chat.id,
        "Отправь 1, если хочешь узнать погоду в данный момент\nОтправь 2, если хочешь получить прогноз на 5 дней в виде графика\nОтправь 3, если хочешь мониторить погоду",
    )

def run_bot():
    bot.polling(none_stop=True)
    