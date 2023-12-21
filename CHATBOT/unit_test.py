import unittest
from bot import create_dict_with_temp  
import requests
from config import open_weather_token


open_weather_token = f"{open_weather_token}"


class TestCreateDictWithTemp(unittest.TestCase):
    

    def test_create_dict_with_temp(self):
        '''Данные о городе введены корректно'''
        # Подготавливаем данные для теста (заглушка данных)
        city = "Северодвинск"
        r = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_weather_token}&units=metric&lang=ru')
        self.mock_data = r.json()
        
        
        # Вызываем функцию с подготовленными данными
        result_dict = create_dict_with_temp(self.mock_data)
        
        # Ожидаемые результаты для теста
        expected_result = {
            '2023-12-21': 
                {'09:00': -3.67, 
                 '12:00': -6.41, 
                 '15:00': -9.13, 
                 '18:00': -11.15, 
                 '21:00': -13.88}, 
            '2023-12-22': 
                {'00:00': -15.85, 
                 '03:00': -16.16, 
                 '06:00': -12.71, 
                 '09:00': -9.45, 
                 '12:00': -7.04, 
                 '15:00': -5.34, 
                 '18:00': -5.46, 
                 '21:00': -4.1}, 
            '2023-12-23': 
                {'00:00': -1.66, 
                 '03:00': -1.56, 
                 '06:00': -1.2, 
                 '09:00': 0.1, 
                 '12:00': 0.76, 
                 '15:00': 0.65, 
                 '18:00': 0.84, 
                 '21:00': 0.88}, 
            '2023-12-24': 
                {'00:00': 0.75, 
                 '03:00': 0.71, 
                 '06:00': 0.62, 
                 '09:00': 0.36, 
                 '12:00': -0.53, 
                 '15:00': -2.69, 
                 '18:00': -4.78, 
                 '21:00': -5.72}, 
            '2023-12-25': 
                {'00:00': -6.33, 
                 '03:00': -7.55, 
                 '06:00': -6.49, 
                 '09:00': -4.73, 
                 '12:00': -4.68, 
                 '15:00': -7.37, 
                 '18:00': -9.07, 
                 '21:00': -9.51}, 
            '2023-12-26': 
                {'00:00': -8.41, 
                 '03:00': -7.83, 
                 '06:00': -8.34}
        }
        # Проверяем, что результат соответствует ожидаемому значению
        self.assertEqual(result_dict, expected_result)
        
        
        
    def test_create_dict_with_temp_bad_town(self):
        '''Данные о городе введены некорректно'''
        # Подготавливаем данные для теста (заглушка данных)
        city = "Йцукенгшщ"
        r = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_weather_token}&units=metric&lang=ru')
        self.mock_data = r.json()
        
        expected_cod = '200'
        result_cod = self.mock_data['cod']
        
        self.assertNotEqual(result_cod, expected_cod)        
        

if __name__ == '__main__':
    unittest.main()
