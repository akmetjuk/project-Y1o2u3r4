from src.ContactHelper.core import AddressBook
from src.ContactHelper.models.contact import Contact
from src.ContactHelper.logger import setup_logger
import difflib
import pathlib
from colorama import init, Fore

init(autoreset=True)
logger = setup_logger()
logger.info("Application started")

__commands__ = ["add", "get", "delete",
                "update-phone",
                "set-birthday", "upcome-birthdays",
                "help", "quit", "exit"]
'''List of available commands for CLI.
This is just a reference and not used in code.
The actual command handling is done in the main() function below.'''


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
        tags_str = ", ".join(t.value for t in contact.tags)
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
            print(f"Invalid number of days ({days}). Please provide a valid integer.")
            return
    bdays: list[Contact] = book.get_upcoming_birthdays(days)
    if bdays == None or len(bdays) == 0:
        print(f"No upcoming birthdays next {days} days.")
        return
    print(f"You have {len(bdays)} birthdays next {days} days:")
    print("\n".join(f"{(" " * 4)}Contact {Fore.YELLOW}'{c.name}'{Fore.RESET} has birthday on {Fore.GREEN}{c.birthday}{Fore.RESET}." for c in bdays))

def print_help():
    print("Available commands:")
    print(f"  {Fore.YELLOW}help{Fore.RESET}")
    print("      Show this help message.")
    print("")
    print(f"  {Fore.YELLOW}add{Fore.RESET} <name> [phone] [email] [birthday]")
    print("      Add new contact.")
    print("      birthday format: YYYY-MM-DD")
    print("")
    print(f"  {Fore.YELLOW}get{Fore.RESET} <name>")
    print("      Find contact by name.")
    print("")
    print(f"  {Fore.YELLOW}delete{Fore.RESET} <name>")
    print("      Delete contact by name.")
    print("")
    print(f"  {Fore.YELLOW}set-birthday{Fore.RESET} <name> <YYYY-MM-DD>")
    print("      Set birthday for a contact.")
    print("")
    print(f"  {Fore.YELLOW}upcome-birthdays{Fore.RESET} <days>")
    print("      Get contacts with birthdays within <days>.")
    print("")
    print(f"  {Fore.YELLOW}update-phone{Fore.RESET} <name> <new_phone> [old_phone]")
    print("      Add or replace phone for a contact.")
    print("      new_phone format: +380XXXXXXXXX")
    print("      If old_phone given, it will be replaced.")
    print("")
    print(f"  {Fore.YELLOW}exit{Fore.RESET} | {Fore.YELLOW}quit{Fore.RESET}")
    print("      Exit the program.")
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

        # ===== upcome-birthdays =====
        elif command == "upcome-birthdays":
            upcome_birthdays(args, book)

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
                print(f"Unknown command. Did you mean '{match[0]}'?")
            else:
                print("Unknown command. Type 'help'",
                      "to see available commands.")


if __name__ == "__main__":
    main()
