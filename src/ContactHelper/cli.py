from src.ContactHelper.core import AddressBook
from src.ContactHelper.models.contact import Contact
from src.ContactHelper.logger import setup_logger
import difflib
import pathlib

logger = setup_logger()
logger.info("Application started")

__commands__ = ["add", "get", "delete",
                "update-phone",
                "set-birthday",
                "help", "quit", "exit"]
'''List of available commands for CLI.
This is just a reference and not used in code.
The actual command handling is done in the main() function below.'''


def format_contact(contact: Contact) -> str:
    """Повертає красивий рядок з усією інформацією про контакт."""
    lines = []
    lines.append(f"Name: {contact.name}")

    # телефони
    if contact.phones:
        phones_str = ", ".join(p.value for p in contact.phones)
    else:
        phones_str = "—"
    lines.append(f"Phones: {phones_str}")

    # email
    if contact.email:
        # contact.email може бути або рядком, або полем з .value
        email_str = getattr(contact.email, "value", contact.email)
    else:
        email_str = "—"
    lines.append(f"Email: {email_str}")

    # birthday
    if contact.birthday:
        bd_str = getattr(contact.birthday, "value", contact.birthday)
    else:
        bd_str = "—"
    lines.append(f"Birthday: {bd_str}")

    # address
    if contact.address:
        addr_str = getattr(contact.address, "value", contact.address)
    else:
        addr_str = "—"
    lines.append(f"Address: {addr_str}")

    return "\n".join(lines)


def print_help():
    print("Available commands:")
    print("  help")
    print("      Show this help message.")
    print("")
    print("  add <name> [phone] [email] [birthday]")
    print("      Add new contact.")
    print("      birthday format: YYYY-MM-DD")
    print("")
    print("  get <name>")
    print("      Find contact by name.")
    print("")
    print("  delete <name>")
    print("      Delete contact by name.")
    print("")
    print("  set-birthday <name> <YYYY-MM-DD>")
    print("      Set birthday for a contact.")
    print("")
    print("  update-phone <name> <new_phone> [old_phone]")
    print("      Add or replace phone for a contact.")
    print("      new_phone format: +380XXXXXXXXX")
    print("      If old_phone given, it will be replaced.")
    print("")
    print("  exit | quit")
    print("      Exit the program.")
    print("")


def main():
    current_dir = pathlib.Path(__file__).parent
    adressbook_path: str = str(current_dir / "addressbook.pkl")

    book = AddressBook.load_data(adressbook_path)  # Завантаження адресної книги при запуску програми
    print("Welcome to ContactHelper CLI!")
    print("Type 'help' to see available commands.\n")

    while True:
        user_input = input("Enter command: ").strip()

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        # ===== exit / quit =====
        if command in ("exit", "quit"):
            book.save_data(adressbook_path)  # Збереження адресної книги при виході з програми
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

        # ===== update-phone =====
        elif command == "update-phone":
            if len(args) < 2:
                print("Usage: update-phone <name> <new_phone> [old_phone]")
                continue

            name = args[0]
            new_phone = args[1]
            old_phone = args[2] if len(args) > 2 else None

            try:
                result = book.update_phone(name, new_phone, phone=old_phone)
                if result:
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
                print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
