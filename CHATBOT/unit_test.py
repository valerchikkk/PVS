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
            '2023-12-19': 
                {'21:00': -1.94}, 
            '2023-12-20': 
                {'00:00': -1.43, 
                 '03:00': -1.17, 
                 '06:00': -2.73, 
                 '09:00': -3.34, 
                 '12:00': -2.31, 
                 '15:00': -4.2, 
                 '18:00': -4.12, 
                 '21:00': -4.42}, 
            '2023-12-21': 
                {'00:00': -4.56, 
                 '03:00': -3.89, 
                 '06:00': -4.69, 
                 '09:00': -6.15, 
                 '12:00': -9.64, 
                 '15:00': -13.52, 
                 '18:00': -15.1, 
                 '21:00': -13.45}, 
            '2023-12-22': 
                {'00:00': -12.99, 
                 '03:00': -9.46, 
                 '06:00': -7.4, 
                 '09:00': -7.59, 
                 '12:00': -9.04, 
                 '15:00': -13.18, 
                 '18:00': -14.81, 
                 '21:00': -9.38}, 
            '2023-12-23': 
                {'00:00': -5.76, 
                 '03:00': -3.25, 
                 '06:00': -1.41, 
                 '09:00': -1.76, 
                 '12:00': -1.82, 
                 '15:00': -0.62, 
                 '18:00': 0.46, 
                 '21:00': 0.76}, 
            '2023-12-24': 
                {'00:00': 0.76, 
                 '03:00': 0.82, 
                 '06:00': 0.69, 
                 '09:00': 0.09, 
                 '12:00': -1.2, 
                 '15:00': -0.99, 
                 '18:00': -2.38}
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
