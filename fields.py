from datetime import datetime


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        is_string = isinstance(value, str)
        is_empty = len(value.strip()) < 0
        has_numbers = any(char.isdigit() for char in value)

        if not is_string and is_empty and has_numbers:
            raise ValueError("⛔️ Field name is incorrect")

        self.__value = value


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        has_ten_symbols = len(value) == 10
        is_digit = value.isdigit()

        if has_ten_symbols and is_digit:
            self.__value = value
        else:
            raise ValueError("⛔️ Field phone is incorrect")


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value, expected_format="%d.%m.%Y"):
        try:
            parsed_date = datetime.strptime(value, expected_format)
            self.__value = parsed_date.strftime("%d %B %Y")
        except ValueError:
            print("⛔️ The date format is not 'DD.MM.YYYY'")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        idx_num = self.phones.index(Phone(phone_number))
        self.phones.pop(idx_num)
        return self.phones

    def edit_phone(self, edit_number, new_number):
        for p in self.phones:
            if p.value == edit_number:
                idx_num = self.phones.index(p)

                self.phones[idx_num] = Phone(new_number)

        return self.phones

    def find_phone(self, searh_number):
        find_phone = ""
        for phone in self.phones:
            if str(phone) == str(searh_number):
                find_phone = str(phone)

        if find_phone:
            return find_phone
        else:
            return f"Search phone {searh_number} does not exist in AddressBook"

    def add_birthday(self, date):
        if self.birthday is not None:
            raise ValueError("Field birthday has value")

        self.birthday = Birthday(date)

    def __str__(self):
        name = self.name.value.title()
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday if self.birthday else "empty"

        return f"""
        📱 Contact info:
            ● name: {name}
            ● phones: {phones}
            ● birthday: {birthday}
        """
