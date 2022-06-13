import re
from pprint import pprint
import csv


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

def edit_phone(str_phone):
    pattern = r"(\+7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\s?\-?(\d{2})\s?\-?(\d{2})"
    str_phone = re.sub(pattern, r"+7(\2)\3-\4-\5", str_phone)
    pattern = r"(\+7\(\d{3}\)\d{3}-\d{2}-\d{2})\s\(?доб.?\s?(\d+)\)?"
    str_phone = re.sub(pattern, r"\1 доб.\2", str_phone)
    # print(str_phone)
    return str_phone

def duplicates_search(contacts_list):
    contacts_list_new = []
    for phone in contacts_list:
        i = 0
        find_index = 0
        while i < len(contacts_list_new):
            retrieved_elements = list(filter(lambda x: phone[0] in x, contacts_list_new[i]))
            # print(retrieved_elements)
            if len(retrieved_elements) > 0:
                find_index = 1
                break
            i += 1
        if find_index == 0:
            contacts_list_new.append(phone)
        else:
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
