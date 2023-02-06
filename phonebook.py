import os
from sys import platform
from operator import itemgetter

DATA_BASE = 'phonebook.txt'


def console_clear():
    if platform in {'linux', 'linux2', 'darwin'}:
        os.system('clear')
    else:
        os.system('cls')


def main_menu() -> str:
    print('''
    Введите номер действия:
1 - Показать все записи
2 - Найти запись по вхождению частей имени
3 - Найти запись по телефону
4 - Добавить новый контакт
5 - Удалить контакт
6 - Изменить номер телефона у контакта
7 - Выход''')
    print()
    return str(input('ваш выбор > '))

def write_file(file_name: str, text) -> None:
    with open(file_name, 'w', encoding='utf8') as data:
        for line in text:
            print(",".join(line), file=data)


def read_file(file_name: str) -> list:
    result = []
    with open(file_name, 'r', encoding='utf8') as data:
        for line in data:
            line = line.replace('\n', '')
            result.append(line.split(','))
    return result


def find_users_by_name(file_name: str) -> None:
    console_clear()
    user_list = read_file(file_name)
    request = str(input('введите часть имени: ').capitalize())
    for user in user_list:
        if request in user[0] or request in user[1] or request in user[2]:
            print(f'{user[0]} {user[1]} {user[2]}: {user[3]}')


def find_users_by_phone(file_name: str) -> None:
    console_clear()
    user_list = read_file(file_name)
    request = str(input('введите часть номера: '))
    for user in user_list:
        if request in user[3]:
            print(f'{user[3]}: {user[0]} {user[1]} {user[2]}')


def show_all(file_name: str) -> None:
    console_clear()
    user_list = read_file(file_name)
    for num, line in enumerate(user_list):
        print(f'{num+1}) {line[0]} {line[1]} {line[2]}, тел: {line[3]}')


def add_new_contact(file_name: str) -> None:
    console_clear()
    contact = []

    contact.append(str(input('фамилия: ').capitalize()))
    contact.append(str(input('имя: ').capitalize()))
    contact.append(str(input('отчество: ').capitalize()))
    contact.append(str(input('телефон: ').capitalize()))

    all_contacts = read_file(file_name)
    all_contacts.append(contact)
    result = sorted(all_contacts, key=itemgetter(0))
    write_file(file_name, result)
    print('контакт добавлен!')


def remove_contact_by_number(file_name: str) -> None:
    console_clear()
    user_list = read_file(file_name)
    for num, line in enumerate(user_list):
        print(f'{num+1}) {line[0]} {line[1]} {line[2]}, тел: {line[3]}')
    print()
    line_to_del = int(input('номер строки для удаления: '))
    del_contact = user_list.pop(line_to_del - 1)
    console_clear()
    print(f'контакт {del_contact[0]} {del_contact[1]} {del_contact[2]} удален')
    write_file(file_name, user_list)


def remove_contact_by_surname(file_name: str) -> None:
    console_clear()
    user_list = read_file(file_name)
    surname_to_del = str(input('фамилия контакта для удаления: ').capitalize())
    console_clear()
    contacts_to_delete = []
    for i, contact in enumerate(user_list):
        if contact[0] == surname_to_del:
            request = int(input(
                'введите номер действия:\n'
                f'1 - удалить "{user_list[i][0]} {user_list[i][1]} {user_list[i][2]}"\n'
                'другая цифра - не удалять\n'))
            console_clear()
            if request == 1:
                contacts_to_delete.append(user_list[i])
    result_list = [person for person in user_list \
                    if person not in contacts_to_delete]
    print('контакт(ы)')
    for line in contacts_to_delete:
        string_contact = ' '.join(line)
        print(f'{string_contact}')
    print('удален(ы)')
    write_file(file_name, result_list)


def change_phone_num(file_name: str) -> None:
    console_clear()
    user_list = read_file(file_name)
    contact_to_change = str(input('фамилия контакта для изменения номера: ').capitalize())
    for i, contact in enumerate(user_list):
        if contact[0] == contact_to_change:
            request = int(input(
                'введите номер действия:\n'
                f'1 - изменить номер "{user_list[i][0]} {user_list[i][1]} {user_list[i][2]}"\n'
                'другая цифра - не менять этот контакт\n'))
            if request == 1:
                new_number = str(input('новый номер: '))
                user_list[i][3] = new_number
                print('номер телефона изменен')
            else:
                print()
    write_file(file_name, user_list)


def delete_mode(ile_name: str) -> None:
    while True:
        console_clear()
        print('''
        выберете способ удаления:
    1 - удалить по номеру строки
    2 - удалить по фамилии
    3 - главное меню''')
        del_mode = str(input('ваш выбор > '))
        if del_mode == '1':
            remove_contact_by_number(ile_name)
            print()
            input('Нажмите Enter чтобы вернуться в меню..')

        elif del_mode == '2':
            remove_contact_by_surname(ile_name)
            print()
            input('Нажмите Enter чтобы вернуться в меню..')
        elif del_mode == '3':
            break
        else:
            print('неизвестная комманда')
            input('Нажмите Enter..')

run = True

while run:
    console_clear()
    mode = main_menu()
    if mode == '1':
        show_all(DATA_BASE)
        print()
        input('Нажмите Enter чтобы вернуться в меню..')
    elif mode == '2':
        find_users_by_name(DATA_BASE)
        print()
        input('Нажмите Enter чтобы вернуться в меню..')
    elif mode == '3':
        find_users_by_phone(DATA_BASE)
        print()
        input('Нажмите Enter чтобы вернуться в меню..')
    elif mode == '4':
        add_new_contact(DATA_BASE)
        print()
        input('Нажмите Enter чтобы вернуться в меню..')
    elif mode == '5':
        delete_mode(DATA_BASE)
    elif mode == '6':
        change_phone_num(DATA_BASE)
        print()
        input('Нажмите Enter чтобы вернуться в меню..')
    elif mode == '7':
        console_clear()
        print()
        print('всего доброго!')
        run = False
    else:
        console_clear()
        print('неизвестная комманда')
        print()
        input('Нажмите Enter чтобы вернуться в меню..')