import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Настройка доступа к Google Sheets
def connect_to_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('G:/1/credentials.json', scope)
    client = gspread.authorize(creds)
    return client

def sheet_search_in_multiple_cols_return_row(sheet, search_criteria):
    if not search_criteria:
        print("searchCriteria не определен")
        return None

    criteria = json.loads(search_criteria)
    data = sheet.get_all_values()

    for row in data:
        match = True
        for key in criteria:
            if row[int(key) - 1] != criteria[key]:
                match = False
                break
        if match:
            item_number = row[3]  # Номер товара
            additional_info = row[4]  # Дополнительная информация
            return f"{additional_info} {item_number}"  # Возвращаем информацию о товаре и номер
    return None  # Если совпадений не найдено

def my_function():
    spreadsheet_id = "1pOyg3-_oyDWyxqBiao8mATIgbSvHO_uRW2dBfbU31aA"  # Замените на ваш ID таблицы
    client = connect_to_google_sheets()
    sheet = client.open_by_key(spreadsheet_id).sheet1

    amort_values = ["Амортизаторы задние", "Стойки передние", "Пружины задние", "Пружины передние"]
    queries = [{'Firma': 'ss20', 'Amort': amort, 'Auto': '2101', 'Zaniz': 'Без занижения'} for amort in amort_values]

    total_cost = 0
    items_list = []  # Список найденных товаров

    for query in queries:
        search_criteria = json.dumps({
            "1": query['Firma'],
            "2": query['Amort'],
            "3": query['Auto'],
            "6": query['Zaniz']
        })

        result = sheet_search_in_multiple_cols_return_row(sheet, search_criteria)

        if result:
            price = float(result.split(" ")[-1])
            if not isinstance(price, float):
                print(f"Ошибка при получении цены для: {query['Amort']}")
                continue
            total_cost += price
            items_list.append(" ".join(result.split(" ")[:-1]))  # Добавляем найденный товар (без цены) в список
        else:
            print(f"Совпадений не найдено для: {query['Amort']}")

    # Выводим найденные товары
    print("Найденные товары:")
    for item in items_list:
        print(item)

    # Выводим общую стоимость
    print(f"Общая стоимость комплекта: {total_cost:.2f} руб.")

if __name__ == "__main__":
    my_function()
