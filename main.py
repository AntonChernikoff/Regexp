import re
from pprint import pprint
import csv
import datetime

def file_log_decorator(file_log = 'function_errors.log'):
    def log_function(old_func):
        def new_func(*args, **kwargs):
            text = f"{datetime.datetime.now()} функция {old_func.__name__}{args}{kwargs}"
            something = old_func(*args, **kwargs)
            text = f"{text} return {something}\n"
            # print(f"{text} return {something}")
            with open(file_log, 'a', encoding='utf8') as file:
                file.write(text)
            return something
        return new_func
    return log_function


def read_csv():
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

def write_csv(contacts_list):
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

def edit_fio(str_list): # Обработка ФИО
    text = str_list[0]+" "+str_list[1]+" "+str_list[2]
    # print(text)
    pattern = r"(\w+)\s+(\w+)\s+(\w+)\s+"
    res = re.sub(pattern, r"\1 \2 \3", text)
    res = res.split()
    if len(res) <= 3:
        j = 0
        while j < len(res):
            str_list[j] = res[j]
            j += 1
    return str_list

@file_log_decorator(file_log = 'edit_phone.log')
def edit_phone(str_phone):
    pattern = r"(\+7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\s?\-?(\d{2})\s?\-?(\d{2})"
    str_phone = re.sub(pattern, r"+7(\2)\3-\4-\5", str_phone)
    pattern = r"(\+7\(\d{3}\)\d{3}-\d{2}-\d{2})\s\(?доб.?\s?(\d+)\)?"
    str_phone = re.sub(pattern, r"\1 доб.\2", str_phone)
    # print(str_phone)
    return str_phone

def search_in_list(contacts_list_new, phone):
    i = 0
    while i < len(contacts_list_new):
        res_list_1 = list(filter(lambda x: phone[0] in x, contacts_list_new[i])) # Фамилия
        res_list_2 = list(filter(lambda x: phone[1] in x, contacts_list_new[i])) # Имя
        if len(res_list_1) > 0 and len(res_list_2) > 0:
            return [i]
        i += 1
    return []

def duplicates_search(contacts_list):
    contacts_list_new = []
    for phone in contacts_list:
        find_index = search_in_list(contacts_list_new, phone)
        if len(find_index) == 0:
            contacts_list_new.append(phone)
        else:
            i = find_index[0]
            j = 0
            for contact in contacts_list_new[i]:
                if contact == "":
                    contacts_list_new[i][j] = phone[j]
                j += 1
    return contacts_list_new

def main():
    contacts_list = read_csv()
    print("+++++++++++++++ contacts_list ++++++++++++++++++++++++")
    i = 1
    while i < len(contacts_list):
        # Обработка ФИО
        contacts_list[i] = edit_fio(contacts_list[i])
        # Обработка телефона
        contacts_list[i][5] = edit_phone(contacts_list[i][5])
        print(contacts_list[i])
        i += 1
    # Поиск дубликатов в контактах
    contacts_list_new = duplicates_search(contacts_list)
    print("+++++++++++++++ contacts_list_new ++++++++++++++++++++++++")
    for contact in contacts_list_new:
        print(contact)
    write_csv(contacts_list_new)

if __name__ == '__main__':
    main()
