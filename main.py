import telebot
import requests
import json
import datetime 
import time

bot = telebot.TeleBot('7126095826:AAHg-r2KLV9D7IjurCy9LmmsaYWmlzfTbuo')
API = 'cec83fa4b8625fe8b600ab58baab486e'


@bot.message_handler(commands=['start'])
def startingMessage(message):
    bot.send_message(message.chat.id,
                     "Welcome, this is the special bot that will help you to get information about weather in any location!")


@bot.message_handler(content_types=['text'])
def getWeather(message):
    location = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        weatherInfo = data['weather'][0]
        current_hour = datetime.datetime.now().hour
        bot.reply_to(message, f'The current temperature outside is: {data["main"]["temp"]}')
        image = 'img.png' if weatherInfo['description'] == 'clear sky' and 6 <= current_hour < 19 else 'img_9.png' if weatherInfo['description'] == 'clear sky' and 19 <= current_hour < 6 else 'img_1.png' if weatherInfo['description'] == 'few clouds' and 6 <= current_hour < 19 else 'img_10.png' if weatherInfo['description'] == 'few clouds' and 19 <= current_hour < 6 else 'img_2.png' if weatherInfo['description'] == 'scattered clouds' else 'img_3.png' if weatherInfo['description'] == 'broken clouds' else 'img_4.png' if 300 <= weatherInfo['id'] <= 321 else 'img_5.png' if weatherInfo['description'] == 'rain' and 6 <= current_hour < 19 else 'img_11.png' if weatherInfo['description'] == 'rain' and 19 <= current_hour < 6 else 'img_6.png' if 200 <= weatherInfo['id'] <= 232 else 'img_7.png' if 600 <= weatherInfo['id'] <= 622  else 'img_8.png'
        file = open('./' + image, 'rb')
        bot.send_message(message.chat.id, f"The weather is {weatherInfo['description']}")
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'You entered an incorrect name of location!')


bot.polling(non_stop=True)
