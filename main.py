from address_book import AddressBook
from fields import Record

ADDRESS_BOOK_FILENAME = "address_book.pickle"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(e)
        except AttributeError as e:
            print(e)
        except IndexError:
            print("⛔️ Sorry. Contact book is empty.")
        except TypeError:
            print("⛔️ Wrong value for operation.")

    return inner


def parse_input(user_input: str) -> tuple[str, list]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list, contacts: dict) -> str:
    name, phone = args

    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    print("🟢 Contact added")


@input_error
def update_contact(args: list, contacts: dict) -> None:
    name, old_phone, new_phone = args
    search_record = contacts.find(name)
    search_record.edit_phone(old_phone, new_phone)
    print("🟠 Contact updated")


@input_error
def get_contact(args: list, contacts: dict) -> str:
    search_name = str(args[0])
    search_contact = contacts.find(search_name)
    if not search_contact:
        print("Contact is not found!")
    else:
        print(search_contact)


@input_error
def get_all_contacts(contacts: dict) -> None:
    phonebook = "*** {:^20} ***\n\n".format("📒 Phonebook")

    for name, info in contacts.items():
        phones = ""
        for phone in info.phones:
            phones += str(phone)
        phonebook += "📍 Contact: {:<10} 📱 {:<10}\n".format(name.title(), phones)

    print(phonebook)


@input_error
def set_birthday(args: list, contacts: dict) -> None:
    name, b_date = args
    contacts.set_birthday(name, b_date)
    print("🎉 Birthday added")


@input_error
def show_birthday(args: list, contacts: dict) -> None:
    name = str(args[0])
    contact_bday = contacts.show_birthday(name)
    print(contact_bday)


def happy_birthdays(contacts: dict) -> None:
    birthdays = contacts.get_birthdays_per_week()
    if not birthdays:
        print("No birthdays this week")
    else:
        print(birthdays)


def main():
    book = AddressBook()
    book.load(ADDRESS_BOOK_FILENAME)
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:  # exit from function
            book.save(ADDRESS_BOOK_FILENAME)
            print("Good bye!")
            break
        elif command == "hello":  # start phonebook
            print("How can I help you?")
        elif command == "add":  # add contact to phonebook
            add_contact(args, book)
        elif command == "change":  # update contact from phonebook
            update_contact(args, book)
        elif command == "phone":  # get contact from phonebook
            get_contact(args, book)
        elif command == "all":  # get all contacts from phonebook
            get_all_contacts(book)
        elif command == "add-birthday":  # add birthday to contact
            set_birthday(args, book)
        elif command == "show-birthday":  # show contact birthday
            show_birthday(args, book)
        elif command == "birthdays":  # show contacts birthday for next week
            happy_birthdays(book)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
