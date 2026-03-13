from datetime import datetime
from src.ContactHelper.utils import validate_phone_number, validate_email
from colorama import init, Fore


class Field:
    '''Базовий клас для всіх полів контакту'''
    def __init__(self, value):
        self.value = value.strip()

    def __str__(self) -> str:
        '''Повертає рядок для відображення поля
        Returns:
            str: рядок для відображення поля
        '''
        return self.value if self.value else ''


class Phone(Field):
    def __init__(self, value: str):
        super().__init__(validate_phone_number(value))

    def change_phone(self, value: str):
        self.value = validate_phone_number(value)

    def __str__(self) -> str | None:
        if not self.value:
            return None
        init(autoreset=True)
        return self.value


class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format ({value}). Use YYYY-MM-DD")

    def __str__(self) -> str | None:
        '''Повертає дату народження у форматі YYYY-MM-DD
        Returns:
            str: дата народження у форматі YYYY-MM-DD
        '''
        if not self.value:
            return None
        init(autoreset=True)
        return f"{Fore.YELLOW}{self.value.strftime('%Y-%m-%d')}{Fore.RESET}"


class Address(Field):
    def __init__(self, value: str):
        super().__init__(value)

    def __str__(self) -> str:
        init(autoreset=True)
        return f"{Fore.CYAN}{self.value}{Fore.RESET}"


class Email(Field):
    def __init__(self, value: str):
        super().__init__(validate_email(value))

    def change_email(self, value: str):
        self.value = validate_email(value)

    def __str__(self) -> str:
        init(autoreset=True)
        return f"{Fore.MAGENTA}{self.value}{Fore.RESET}"


class Notes(Field):
    def __init__(self, value: str):
        super().__init__(value.strip())

    def __str__(self) -> str:
        init(autoreset=True)
        return f"{Fore.BLUE}{self.value}{Fore.RESET}"
