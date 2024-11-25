import logging

# Настройка логирования
logging.basicConfig(
    filename='app.log',  # Имя файла для хранения логов
    filemode='a',        # Режим записи: 'a' - добавление, 'w' - перезапись
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    level=logging.DEBUG   # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
)

# Пример использования логирования
logging.info("Программа запущена")

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def my_function():
    # Замените на ваш ID таблицы
    spreadsheet_id = "1o2-Qq0RJrnxRpQKG0NYyNdKd-QQHYwYBxU56bYbdd0o"
    
    # Определите массив с разными значениями Amort
    amort_values = ["Амортизаторы задние", "Стойки передние", "Пружины задние", "Пружины передние"]
    
    # Создаем массив запросов
    queries = [{"Firma": "ss20", "Amort": amort, "Auto": "2101", "Zaniz": "Без занижения"} for amort in amort_values]

    total_cost = 0  # Переменная для хранения суммы
    items_list = []  # Массив для хранения названий товаров

    # Перебираем массив запросов
    for query in queries:
        # Создаем JSON строку с использованием значений переменных
        search_criteria = json.dumps({
            "1": query["Firma"],
            "2": query["Amort"],
            "3": query["Auto"],
            "6": query["Zaniz"]
        })

        # Вызов функции поиска
        result = sheet_search_in_multiple_cols_return_row(spreadsheet_id, search_criteria)
        
        # Проверяем результат
        if result:
            # Извлекаем цену из результата
            price = float(result.split(" ")[-1])  # Предполагается, что цена - это последнее слово в строке
            total_cost += price  # Добавляем цену к общей сумме
            items_list.append(" ".join(result.split(" ")[:-1]))  # Добавляем название товара (все кроме последнего элемента)
        else:
            print(f"Совпадений не найдено для: {query['Amort']}")

    # Выводим названия товаров
    for item in items_list:
        print(item)

    # Выводим общую сумму с изменением текста
    print(f"Комплект стоит: {total_cost}")

def sheet_search_in_multiple_cols_return_row(spreadsheet_id, search_criteria):
    # Проверяем, что searchCriteria не является None
    if not search_criteria:
        print("searchCriteria не определен")
        return None  # Возвращаем None, если searchCriteria не определен

    criteria = json.loads(search_criteria)  # Преобразуем строку JSON обратно в объект

    # Настройка доступа к Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(spreadsheet_id).sheet1  # Получаем активный лист таблицы
    data = sheet.get_all_values()  # Получаем все данные из листа

    # Перебираем строки данных для поиска совпадений
    for row in data:
        match = True  # Переменная для отслеживания совпадений
        for key in criteria:
            # Проверяем, есть ли критерий в текущей строке
            if row[int(key) - 1] != criteria[key]:  # key - 1, т.к. индексация массивов начинается с 0
                match = False
                break  # Если есть несоответствие, выходим из цикла
        if match:
            # Получаем значения из нужных колонок
            item_number = row[3]  # Номер детали из четвертой колонки
            additional_info = row[4]  # Дополнительная информация из пятой колонки
            return f"{additional_info} {item_number}"  # Форматируем строку

    return None  # Возвращаем None, если совпадений не найдено

# Для тестирования
if __name__ == "__main__":
    my_function()
