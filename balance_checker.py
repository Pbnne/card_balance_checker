import requests
from bs4 import BeautifulSoup
import json

SMS = input("Введите номер карты: ")
# URL и данные для запроса
url = "https://alpha.ltkarta.ru/fideth"
data = {
    'bsk': SMS,
    'cardsource': 'new',
    'user_lang': 'ru'
}
# Заголовки запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}
# Выполнение POST-запроса
response = requests.post(url, data=data, headers=headers)
# Проверка статуса ответа и вывод данных
if response.status_code == 200:
    # Получаем текст ответа
    response_text = response.text
    
    # Если ответ в формате JSON
    try:
        # Попытка распарсить как JSON
        json_response = json.loads(response_text)
        html_content = json_response.get('html', '')
    except json.JSONDecodeError:
        print("Ответ не в формате JSON.")
        html_content = response_text  # Если не JSON, используем текст напрямую
    # Используем BeautifulSoup для извлечения баланса
    soup = BeautifulSoup(html_content, 'html.parser')
    balance_text = soup.find('div', class_='main-card main-card-blue').get_text()
    # Ищем баланс в тексте
    balance_line = [line for line in balance_text.split('\n') if 'баланс' in line.lower()]
    if balance_line:
        # Извлекаем баланс
        balance = balance_line[0].split('не более')[-1].strip()
        
        # Убираем лишние символы и выводим только цифры с символом рубля
        balance = balance.split()[0] + " ₽"
        print(balance)
    else:
        print("Баланс не найден.")
else:
    print(f"Ошибка: {response.status_code}")
