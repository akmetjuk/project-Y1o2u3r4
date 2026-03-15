from src.ContactHelper.core import AddressBook
from src.ContactHelper.models.contact import Contact
from src.ContactHelper.logger import setup_logger
import difflib
import pathlib
from colorama import init, Fore

init(autoreset=True)
logger = setup_logger()
logger.info("Application started")

__commands__ = ["add", "get", "delete", "find-by"
                "update-phone",
                "set-birthday", "upcome-birthdays",
                "set-note", "delete-note",
                "set-email",
                "set-address",
                "add-tag", "delete-tag",
                "help", "quit", "exit"]
'''List of available commands for CLI.
This is just a reference and not used in code.
The actual command handling is done in the main() function below.'''


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {e}"
        except KeyError as e:
            return f"Key error: {e}"
        except IndexError:
            return "Enter the argument for the command"
    return inner


def format_contact(contact: Contact) -> str:
    """Повертає красивий рядок з усією інформацією про контакт."""
    lines = []
    lines.append(f"{" "*4}{Fore.GREEN}Name{Fore.RESET}: {contact.name}")

    # телефони
    if contact.phones:
        phones_str = ", ".join(p.value for p in contact.phones)
    else:
        phones_str = "—"
    lines.append(f"{" "*4}{Fore.GREEN}Phones{Fore.RESET}: {phones_str}")

    # email
    email_str = contact.email if contact.email else "—"
    lines.append(f"{" "*4}{Fore.GREEN}Email{Fore.RESET}: {email_str}")

    # birthday
    bd_str = contact.birthday if contact.birthday else "—"
    lines.append(f"{" "*4}{Fore.GREEN}Birthday{Fore.RESET}: {bd_str}")

    # address
    if contact.address:
        lines.append(f"{" "*4}{Fore.GREEN}Address{Fore.RESET}: {contact.address}")

    # tags
    if contact.tags:
        tags_str = ", ".join(t for t in contact.tags)
        lines.append(f"{" "*4}{Fore.GREEN}Tags{Fore.RESET}: {tags_str}")

    # notes
    if contact.notes:
        lines.append(f"{" "*4}{Fore.GREEN}Note{Fore.RESET}: {contact.notes}")

    return "\n".join(lines)


def upcome_birthdays(args: list[str], book: AddressBook):
    if len(args) == 0:
        days = 7
    else:
        try:
            days = int(args[0])
        except ValueError:
            print(f"Invalid number of days ({days}).",
                   "Please provide a valid integer.")
            return
    bdays: list[Contact] = book.get_upcoming_birthdays(days)
    if not bdays or len(bdays) == 0:
        print(f"No upcoming birthdays next {days} days.")
        return
    print(f"You have {len(bdays)} birthdays next {days} days:")
    print("\n".join(f"{(" " * 4)}Contact {Fore.YELLOW}'{c.name}'{Fore.RESET} has birthday on {Fore.GREEN}{c.birthday}{Fore.RESET}." for c in bdays))


@input_error
def search_by(args: list[str], book: AddressBook):
    if len(args) < 1:
        raise IndexError((f"Usage: {Fore.YELLOW}find-by{Fore.RESET}",
                         "<search-by> <keywoard>"))

    field = args[0].strip().lower()
    keywoard = args[1].strip().lower()
    contacts = None
    if field == "name":
        contacts = book.search_by_name(keywoard)
    elif field == "note":
        contacts = book.find_by_notes(keywoard)
    elif field == "tag":
        contacts = book.find_by_tag(keywoard)
    elif field == "phone":
        contacts = book.find_by_phone(keywoard)

    if contacts and len(contacts) > 0:
        print(f"Your result is {len(contacts)} contacts",
               f"by searching '{keywoard}' in '{field}'")
        for c in contacts:
            print(f"{" " * 4}- {Fore.GREEN}{c.name}{Fore.RESET}")
        print(f"for details use command {Fore.YELLOW}get{Fore.RESET} <name>")
    else:
        print(f"No results for searching '{keywoard}' in '{field}'")


@input_error
def set_note(args: list[str], book: AddressBook):
    if len(args) < 1:
        raise IndexError("Usage: set-notes <name> <note text>")

    name = args[0]
    note = (" ".join(args[1:])).strip()
    if not note:
        print("Note text is empty")
        return
    try:
        if book.set_notes(name, note):
            print(f"You add notes to the '{name}'")
    except Exception as e:
        print(e)


@input_error
def delete_note(args: list[str], book: AddressBook):
    if len(args) < 1:
        raise IndexError("Usage: delete-note <name>")

    name = args[0]
    try:
        if book.delete_notes(name):
            print(f"You pop notes from the '{name}'")
    except Exception as e:
        print(e)


@input_error
def set_email(args: list[str], book: AddressBook):
    if len(args) < 1:
        raise IndexError("Usage: add <name> <email>")
    email = args[1]
    name = args[0]
    try:
        book.set_email(name, email)
    except Exception as e:
        print(e)
        return
    print(f"You set email: {email} to the '{name}'")


@input_error
def set_address(args: list[str], book: AddressBook):
    if len(args) < 1:
        raise IndexError("Usage: add <name> <email>")
    name = args[0]
    address = (" ".join(args[1:])).strip()
    try:
        book.set_address(name, address)
    except Exception as e:
        print(e)
        return
    print(f"You set address: {address} to the '{name}'")


@input_error
def add_tag(args: list[str], book: AddressBook):
    if len(args) < 1:
        raise IndexError("Usage: add <name> <tag>")
    tags = []
    name = args[0]
    for t in args[1:]:
        try:
            if book.add_tag(name, t):
                tags.append(t.strip())
        except Exception as e:
            print(e)
            return
    print(f"You add tags: {", ".join(tags)} to the '{name}'")


@input_error
def delete_tag(args: list[str], book: AddressBook):
    if len(args) < 1:
        raise IndexError("Usage: add <name> <tag>")
    tags = []
    name = args[0]
    for t in args[1:]:
        try:
            if book.delete_tag(name, t):
                tags.append(t.strip())
        except Exception as e:
            print(e)
            return
    print(f"You remove tags: {", ".join(tags)} from the '{name}'")


def print_help():
    print("Available commands:")
    print(f"{" "*4}{Fore.YELLOW}help{Fore.RESET}")
    print(f"{" "*8}Show this help message.")
    print("")
    print(f"{" "*4}{Fore.YELLOW}add{Fore.RESET}",
          "<name> [phone] [email] [birthday]")
    print(f"{" "*8}Add new contact.")
    print(f"{" "*8}birthday format: YYYY-MM-DD")
    print("")
    print(f"{" "*4}{Fore.YELLOW}get{Fore.RESET} <name>")
    print(f"{" "*8}Find contact by name.")
    print("")
    print(f"{" "*4}{Fore.YELLOW}delete{Fore.RESET} <name>")
    print(f"{" "*8}Delete contact by name.")
    print("")
    print(f"{" "*4}{Fore.YELLOW}find-by{Fore.RESET} <search-by> <keywoard>")
    print(f"{" "*8}Search in contacts by <search-by>",
          "field, can be one of the values: ")
    print(f"{" "*10}- note - to search by whole keyword")
    print(f"{" "*10}- tag - to serach in tags")
    print(f"{" "*10}- name - to search in name")
    print(f"{" "*10}- phone - to search in phones")
    print(f"{" "*8}with a <keywoard> in <search-by> field")
    print("")
    print(f"{" "*4}{Fore.YELLOW}set-email{Fore.RESET} <name> <email>")
    print(f"{" "*8}Set email <email> for a contact <name>")
    print("")
    print(f"{" "*4}{Fore.YELLOW}set-birthday{Fore.RESET} <name> <YYYY-MM-DD>")
    print(f"{" "*8}Set birthday for a contact.")
    print("")
    print(f"{" "*4}{Fore.YELLOW}set-address{Fore.RESET} <name> <address>")
    print(f"{" "*8}Set address for a contact.")
    print("")
    print(f"{" "*4}{Fore.YELLOW}upcome-birthdays{Fore.RESET} <days>")
    print(f"{" "*8}Get contacts with birthdays within <days>.")
    print("")
    print(f"{" "*4}{Fore.YELLOW}update-phone{Fore.RESET}",
          "<name> <new_phone> [old_phone]")
    print(f"{" "*8}Add or replace phone for a contact.")
    print(f"{" "*8}new_phone format: +380XXXXXXXXX")
    print(f"{" "*8}If old_phone given, it will be replaced.")
    print("")
    print(f"{" "*4}{Fore.YELLOW}set-note{Fore.RESET} <name> <note text>")
    print(f"{" "*8}Set note <note text> for a contact <name>")
    print("")
    print(f"{" "*4}{Fore.YELLOW}delete-note{Fore.RESET} <name>")
    print(f"{" "*8}Delete note from a contact <name>")
    print("")
    print(f"{" "*4}{Fore.YELLOW}add-tag{Fore.RESET} <name> <tag>")
    print(f"{" "*8}Set tag for a contact <name>")
    print("")
    print(f"{" "*4}{Fore.YELLOW}delete-tag{Fore.RESET} <name> <tag>")
    print(f"{" "*8}Delete specified <tag> from a contact <name>")
    print("")
    print(f"{" "*4}{Fore.YELLOW}exit{Fore.RESET}",
           f"| {Fore.YELLOW}quit{Fore.RESET}")
    print(f"{" "*8}Exit the program.")
    print("")


def main():
    current_dir = pathlib.Path(__file__).parent
    adressbook_path: str = str(current_dir / "addressbook.pkl")
    # Завантаження адресної книги при запуску програми
    book = AddressBook.load_data(adressbook_path)
    print("Welcome to ContactHelper CLI!")
    print(f"Varsion: {Fore.RED}{book.version}{Fore.RESET}",
          f" | Contacs avaliable: {book.count}")
    print(f"Type '{Fore.YELLOW}help{Fore.RESET}' to see available commands.\n")

    while True:
        user_input = input("Enter command: ").strip()

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        # ===== exit / quit =====
        if command in ("exit", "quit"):
            # Збереження адресної книги при виході з програми
            book.save_data(adressbook_path)
            print("Good bye!")
            break

        # ===== help =====
        elif command == "help":
            print_help()

        # ===== add =====
        elif command == "add":
            if len(args) < 1:
                print("Usage: add <name> [phone] [email] [birthday]")
                continue

            name = args[0]
            phone = args[1] if len(args) > 1 else None
            email = args[2] if len(args) > 2 else None
            birthday = args[3] if len(args) > 3 else None

            try:
                result = book.add_contact(name,
                                          phone=phone,
                                          email=email,
                                          birthday=birthday)
                if result:
                    print(f"Contact '{name}' added.")
                else:
                    print(f"Contact '{name}' was",
                          "not added (maybe already exists?).")
            except ValueError as e:
                # валідація телефона/email/дати
                print(f"Validation error: {e}")
            except Exception as e:
                print(f"Error while adding contact: {e}")

        # ===== get =====
        elif command == "get":
            if len(args) < 1:
                print("Usage: get <name>")
                continue

            name = args[0]
            try:
                contact = book.get_contact(name)
                if contact is None:
                    print(f"Contact '{name}' not found.")
                else:
                    print(format_contact(contact))
            except Exception as e:
                print(f"Error while getting contact: {e}")

        # ===== delete =====
        elif command == "delete":
            if len(args) < 1:
                print("Usage: delete <name>")
                continue

            name = args[0]
            try:
                result = book.delete_contact(name)
                if result:
                    print(f"Contact '{name}' deleted.")
                else:
                    print(f"Contact '{name}' not found.")
            except Exception as e:
                print(f"Error while deleting contact: {e}")

        # ===== set-birthday =====
        elif command == "set-birthday":
            if len(args) < 2:
                print("Usage: set-birthday <name> <YYYY-MM-DD>")
                continue

            name = args[0]
            date_str = args[1]

            try:
                result = book.set_birthday(name, date_str)
                if result:
                    print(f"Birthday for '{name}' set to {date_str}.")
                else:
                    print(f"Birthday for '{name}' was not set.")
            except ValueError as e:
                print(f"Validation error: {e}")
            except Exception as e:
                print(f"Error while setting birthday: {e}")

        elif command == "find-by":
            search_by(args, book)

        elif command == "set-email":
            set_email(args, book)

        elif command == "set-address":
            set_address(args, book)

        # ===== upcome-birthdays =====
        elif command == "upcome-birthdays":
            upcome_birthdays(args, book)

        elif command == "set-note":
            set_note(args, book)

        elif command == "delete-note":
            delete_note(args, book)

        elif command == "add-tag":
            add_tag(args, book)

        elif command == "delete-tag":
            delete_tag(args, book)

        # ===== update-phone =====
        elif command == "update-phone":
            if len(args) < 2:
                print("Usage: update-phone <name> <new_phone> [old_phone]")
                continue

            name = args[0]
            new_phone = args[1]
            old_phone = args[2] if len(args) > 2 else None

            try:
                if book.update_phone(name, new_phone, old_phone):
                    if old_phone:
                        print(f"Phone '{old_phone}' for '{name}'",
                              f"replaced with '{new_phone}'.")
                    else:
                        print(f"Phone '{new_phone}' added for '{name}'.")
                else:
                    print(f"Phone for '{name}' was not updated.")
            except ValueError as e:
                print(f"Validation error: {e}")
            except Exception as e:
                print(f"Error while updating phone: {e}")

        # ===== unknown command =====
        else:
            match = difflib.get_close_matches(command, __commands__, n=1)
            if match:
                print("Unknown command. Did you mean: ",
                       f"'{Fore.YELLOW}{match[0]}{Fore.RESET}'?")
            else:
                print("Unknown command. Type 'help'",
                      "to see available commands.")


if __name__ == "__main__":
    main()
