import json
import re
from rich.console import Console
from rich.table import Table

JSON_PATH = 'data.json'
MENU_TEXT = '1. Add contact\n2. Edit contact\n3. Delete contact\n4. View contacts\n5. Exit\n'
CONTACT_FIELDS = ['name', 'phone', 'email']
FIELDS_REGEX = {'name': r'^[a-zA-Z ]+$',
                'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                'phone': r'^\d{11}$'}


def load_data(arr='contacts'):
    try:
        with open(JSON_PATH) as f:
            return json.load(f)[arr]
    except FileNotFoundError:
        create_data()


def create_data(arr='contacts'):
    with open(JSON_PATH, 'w') as f:
        json.dump({arr: []}, f)
        f.close()


def update_data(data, arr='contacts'):
    with open(JSON_PATH, 'w') as f:
        json.dump({arr: data}, f)
        f.close()


def sort_data(data, key, reverse=False):
    return sorted(data, key=lambda x: x[key], reverse=reverse)


def find_contact(data, key, value):
    for contact in data:
        if contact[key] == value:
            return contact
    return None


def create_table(data, sort='name', reverse=False):
    table = Table(title=f"Contacts List (Sorted by {sort} {'Descending' if reverse else 'Ascending'})",
                  show_header=True, header_style="bold")
    table.add_column("name", justify="center", style="bold cyan")
    table.add_column("phone", justify="center", style="magenta")
    table.add_column("email", justify="center", style="green")

    sorted_data = sort_data(data, sort, reverse)

    for contact in sorted_data:
        table.add_row(contact['name'],
                      contact['phone'], contact['email'], end_section=True)

    return table


def create_contact(data):
    contact = {}
    for field in CONTACT_FIELDS:
        value = input(f'Enter {field}: ')
        while not re.match(FIELDS_REGEX[field], value):
            print(f'Invalid {field}')
            value = input(f'Enter {field}: ')
        contact[field] = value
    if find_contact(data, 'name', contact['name']):
        print('\n'+contact['name'] + ' already exists with that name\n')
        return
    data.append(contact)
    update_data(data)

    print('\n' + contact['name'] + ' added successfully\n')


def edit_contact(data):

    table = create_table(data)
    console = Console()
    console.print(table)

    input_name = input('Enter exact name of contact to edit: ')
    if input_name == 'exit':
        return
    contact = find_contact(data, 'name', input_name)
    if contact:
        for field in CONTACT_FIELDS:
            value = input(
                f'Enter new {field} [leave blank to don\'t change] : ')
            if value == '':
                continue
            while not re.match(FIELDS_REGEX[field], value):
                print(f'Invalid {field}')
                value = input(f'Enter {field}: ')
            contact[field] = value
        update_data(data)
        print(f'\n{input_name} updated\n')
    else:
        print(f'\ncould not find {input_name}\n')


def delete_contact(data):

    table = create_table(data)
    console = Console()
    console.print(table)

    input_name = input('Enter exact name of contact to delete: ')
    if input_name == 'exit':
        return
    contact = find_contact(data, 'name', input_name)
    if contact:
        data.remove(contact)
        update_data(data)
        print(f'\n{input_name} deleted successfully\n')
    else:
        print(f'\ncould not find {input_name}\n')


def show_contacts(data):
    sort = 'name'
    reverse = False
    while True:
        table = create_table(data, sort, reverse)
        caption = 'Sort by: ' + ', '.join(CONTACT_FIELDS) + ' or type "exit" to return\n' + \
            'To sort by a field, type the field name\n' +\
            'repeat the field name to sort in descending order'
        table.caption = caption
        console = Console()
        console.print(table)

        choice = input('Enter choice: ')

        while not (choice in CONTACT_FIELDS or choice == 'exit'):
            print('Invalid choice')
            choice = input('Enter choice: ')

        if choice == 'exit':
            break
        elif sort == choice:
            reverse = not reverse
        else:
            sort = choice
            reverse = False


data = load_data()

while True:
    print(MENU_TEXT)
    choice = input('Enter choice: ')
    if choice == '1':
        create_contact(data)
    elif choice == '2':
        edit_contact(data)
    elif choice == '3':
        delete_contact(data)
    elif choice == '4':
        show_contacts(data)
    elif choice == '5':
        print('Goodbye!')
        break
