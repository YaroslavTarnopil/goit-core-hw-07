import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Номер телефону має бути 10-значним.")

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Неправильний формат дати. Використовуйте формат 'DD.MM.YYYY'.")

class Record:
    def __init__(self, name_value, birthday_value=None):
        self.name = Name(name_value)
        self.phones = []
        self.birthday = None
        if birthday_value:
            self.add_birthday(birthday_value)

    def add_phone(self, phone_value):
        try:
            phone = Phone(phone_value)
            self.phones.append(phone)
        except ValueError as e:
            print(e)

    def remove_phone(self, phone_value):
        self.phones = [phone for phone in self.phones if phone.value != phone_value]

    def edit_phone(self, old_phone_value, new_phone_value):
        self.remove_phone(old_phone_value)
        self.add_phone(new_phone_value)

    def add_birthday(self, birthday_value):
        try:
            birthday = Birthday(birthday_value)
            if not self.birthday:
                self.birthday = birthday
            else:
                raise ValueError("Може бути тільки одне значення для дня народження.")
        except ValueError as e:
            print(e)

    def get_upcoming_birthday(self):
        if self.birthday:
            today = datetime.today()
            birthday_date = datetime.strptime(self.birthday.value, '%d.%m.%Y').replace(year=today.year)
            if birthday_date < today:
                birthday_date = birthday_date.replace(year=today.year + 1)
            return birthday_date
        return None

    def show_birthday(self):
        return self.birthday.value if self.birthday else "N/A"

    def __str__(self):
        return f"Name: {self.name.value}, Birthday: {self.show_birthday()}, Phones: {', '.join([phone.value for phone in self.phones])}"

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find_record_by_name(self, name_value):
        for record in self.records:
            if record.name.value == name_value:
                return record
        return None

    def remove_record_by_name(self, name_value):
        self.records = [record for record in self.records if record.name.value != name_value]

    def get_all_records(self):
        return [record for record in self.records]

    def add_birthday_to_record(self, name_value, birthday_value):
        record = self.find_record_by_name(name_value)
        if record:
            record.add_birthday(birthday_value)
        else:
            print(f"Контакт з ім'ям {name_value} не знайдено.")

    def show_birthday_of_record(self, name_value):
        record = self.find_record_by_name(name_value)
        if record:
            return record.show_birthday()
        return f"Контакт з ім'ям {name_value} не знайдено."

    def get_birthdays_for_next_week(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        birthdays_list = []
        for record in self.records:
            upcoming_birthday = record.get_upcoming_birthday()
            if upcoming_birthday and today <= upcoming_birthday <= next_week:
                birthdays_list.append((record.name.value, upcoming_birthday.strftime('%d.%m.%Y')))
        return birthdays_list

    def __str__(self):
        return "\n".join([str(record) for record in self.records])


address_book = AddressBook()

def handle_command(command):
    command_parts = command.split()
    if command_parts[0] == "add":
        if len(command_parts) == 3:
            name = command_parts[1]
            phone = command_parts[2]
            record = address_book.find_record_by_name(name)
            if record:
                record.add_phone(phone)
                print(f"Номер телефону '{phone}' успішно додано до контакту '{name}'.")
            else:
                new_record = Record(name)
                new_record.add_phone(phone)
                address_book.add_record(new_record)
                print(f"Новий контакт '{name}' з номером телефону '{phone}' успішно створено.")
        else:
            print("Неправильний формат команди. Використовуйте 'add [ім'я] [телефон]'")
    elif command_parts[0] == "change":
        if len(command_parts) == 3:
            name = command_parts[1]
            new_phone = command_parts[2]
            record = address_book.find_record_by_name(name)
            if record:
                record.edit_phone(record.phones[0].value, new_phone)
                print(f"Телефонний номер для контакту '{name}' успішно змінено на '{new_phone}'.")
            else:
                print(f"Контакт з ім'ям {name} не знайдено.")
        else:
            print("Неправильний формат команди. Використовуйте 'change [ім'я] [новий телефон]'")
    elif command_parts[0] == "phone":
        if len(command_parts) == 2:
            name = command_parts[1]
            record = address_book.find_record_by_name(name)
            if record:
                print(f"Телефонний номер для контакту '{name}': {record.phones[0].value}")
            else:
                print(f"Контакт з ім'ям {name} не знайдено.")
        else:
            print("Неправильний формат команди. Використовуйте 'phone [ім'я]'")
    elif command_parts[0] == "all":
        print("Всі контакти:")
        print(address_book)
    elif command_parts[0] == "add-birthday":
        if len(command_parts) == 3:
            name = command_parts[1]
            birthday = command_parts[2]
            address_book.add_birthday_to_record(name, birthday)
            print(f"День народження для контакту '{name}' успішно додано.")
        else:
            print("Неправильний формат команди. Використовуйте 'add-birthday [ім'я] [дата народження]'")
    elif command_parts[0] == "show-birthday":
        if len(command_parts) == 2:
            name = command_parts[1]
            print(f"День народження для контакту '{name}': {address_book.show_birthday_of_record(name)}")
        else:
            print("Неправильний формат команди. Використовуйте 'show-birthday [ім'я]'")
    elif command_parts[0] == "birthdays":
        print("Дні народження наступного тижня:")
        birthdays = address_book.get_birthdays_for_next_week()
        for name, birthday in birthdays:
            print(f"{name}: {birthday}")
    elif command_parts[0] == "hello":
        print("Привіт!")
    elif command_parts[0] in ["close", "exit"]:
        print("До побачення!")
        return True
    else:
        print("Невідома команда.")

    return False

def main():
    print("Ласкаво просимо до адресної книги. Введіть 'help' для перегляду списку команд.")
    while True:
        command = input("Введіть команду: ")
        if command.lower() == "help":
            print("Список команд:")
            print("add [ім'я] [телефон]")
            print("change [ім'я] [новий телефон]")
            print("phone [ім'я]")
            print("all")
            print("add-birthday [ім'я] [дата народження]")
            print("show-birthday [ім'я]")
            print("birthdays")
            print("hello")
            print("close або exit")
        else:
            should_exit = handle_command(command)
            if should_exit:
                break

if __name__ == "__main__":
    main()
