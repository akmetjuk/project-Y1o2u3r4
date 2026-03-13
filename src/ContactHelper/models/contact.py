from datetime import date, datetime
from colorama import Fore, init
from .fields import Email, Phone, Birthday, Address, Notes
from src.ContactHelper.utils import validate_phone_number, validate_email


class Contact:

    def __init__(self, name: str):
        self._name = name.strip()
        self._phones: list[Phone] = []
        self._birthday: Birthday = None
        self._address: Address = None
        self._email: Email = None
        self._created_at: str = date.today().strftime("%Y-%m-%d %H:%M:%S")
        self._ischanged: bool = False
        self._changed_at: str = self._created_at
        self._tags: set[str] = set()
        self._notes: Notes = None

    def __str__(self) -> str:
        init(autoreset=True)
        repres: str = f"Contact name: {Fore.YELLOW}{self.name}{Fore.RESET}"
        if self._email:
            repres += f", email: {self._email}"
        if self._phones:
            phones: str = '; '.join(p for p in self._phones).strip()
            if len(phones) > 1:
                repres += f", phones: {phones}"
        if self._birthday:
            repres += f", {self._birthday}"
        if self._address:
            repres += f", address: {self._address}"
        return repres

    def __changed(self) -> bool:
        self._changed_at = date.today().strftime("%Y-%m-%d %H:%M:%S")
        self._ischanged = True
        return True

    def table_repr(self) -> str:
        return self.__str__()

    @property
    def created_at(self) -> str:
        """Повертає дату та час створення контакту
        у форматі YYYY-MM-DD HH:MM:SS"""
        return self._created_at

    @property
    def created_date(self) -> datetime:
        """Повертає дату створення контакту у форматі YYYY-MM-DD"""
        return datetime.strptime(self._created_at, "%Y-%m-%d %H:%M:%S").date()

    @property
    def changed_at(self) -> str:
        """Повертає дату та час останнього змінення
        контакту у форматі YYYY-MM-DD HH:MM:SS"""
        return self._changed_at

    @property
    def changed_date(self) -> datetime:
        """Повертає дату останнього змінення контакту у форматі YYYY-MM-DD"""
        return datetime.strptime(self._changed_at, "%Y-%m-%d %H:%M:%S").date()

    @property
    def name(self) -> str:
        """Повертає ім'я контакту"""
        return self._name

    @property
    def birthday(self) -> str | None:
        """Повертає дату народження контакту в форматі YYYY-MM-DD
        або None, якщо дата народження не встановлена"""
        return self._birthday

    @birthday.setter
    def birthday(self, date: str) -> bool:
        '''Встановлює дату народження для контакту
        Args:
            date (str): дата народження у форматі DD.MM.YYYY
        Returns:
            bool: True, якщо дата народження оновлена успішно
        '''
        date = date.strip() if date else None
        if not date:
            return False
        self._birthday = Birthday(date)
        return self.__changed()

    @property
    def address(self) -> str | None:
        """Повертає адресу контакту або None, якщо адреса не встановлена"""
        return self._address.value if self._address else None

    @address.setter
    def address(self, value: str) -> bool:
        """Встановлює адресу контакту
        Args:
            value (str): адреса для встановлення
        """
        if not value:
            return False
        self._address = Address(value)
        return self.__changed()

    @property
    def phones(self) -> list[Phone] | None:
        """Повертає список телефонних номерів контакту або порожній список,
        якщо телефонні номери не встановлені"""
        return self._phones

    def find_phone(self, phone: str) -> Phone | None:
        """
        Пошук телефону в записі.
        Args:
            phone: Номер телефону для пошуку
        Returns:
            Знайдений об'єкт Phone або None, якщо не знайдено
        """
        try:
            phone: str = validate_phone_number(phone)
            for p in self.phones:
                if p.value == phone:
                    return p
        except:
            return None

    def remove_phone(self, phone: str) -> bool:
        '''Видаляє телефонний номер з контакту
        Args:
            phone (str): телефонний номер для видалення
        Returns:
            bool: True, якщо телефонний номер видалено, False в іншому випадку
        '''
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            return self.__changed()
        return False

    def change_phone(self, new_phone: str, phone: str = None) -> bool:
        '''Додає або оновлює телефонний номер для контакту
        Args:
            new_phone (str): новий телефонний номер
            для додавання у форматі +380XXXXXXXXX
            phone (str): телефонний номер для заміни у форматі +380XXXXXXXXX
        Returns:
            bool: True, якщо телефонний номер додано, False в іншому випадку
        Raises:
            ValueError: якщо телефонний номер не
            відповідає формату +380XXXXXXXXX
        '''
        new_phone = validate_phone_number(new_phone)
        if not new_phone:
            raise ValueError(f'Invalid phone number format: {new_phone}')

        if phone:
            phone = validate_phone_number(phone)
            if not phone:
                raise ValueError(f'Invalid phone number format: {phone}')

            for p in self._phones:
                if p.value == phone:
                    p.change_phone(new_phone)
                    return self.__changed()
            return False
        self._phones.append(Phone(new_phone))
        return self.__changed()

    @property
    def email(self) -> str | None:
        """Повертає електронну пошту контакту або None,
        якщо електронна пошта не встановлена"""
        return self._email.value if self._email else None

    @email.setter
    def email(self, value: str):
        '''Встановлює електронну пошту контакту
        Args:
            email (str): нова електронна пошта
            для додавання у форматі user@example.com
        Returns:
            bool: True, якщо електронна пошта оновлена успішно
        Raises:
            ValueError: якщо електронна пошта
            не відповідає формату user@example.com
        '''
        email = validate_email(value)
        if not email:
            raise ValueError(f'Invalid email format: {email}')
        if self._email and self._email.value == email:
            return False
        self._email = Email(email)
        return self.__changed()

    @property
    def tags(self) -> list[str]:
        return list(self._tags)

    def add_tag(self, tag: str) -> bool:
        '''Встановлює тег для контакту
        Args:
            tag (str): тег для встановлення
        Returns:
            bool: True, якщо теги оновлені успішно, False в іншому випадку
        '''
        tag = tag.lower().strip()
        if not tag.isalnum():
            return False
        if tag and tag not in self._tags:
            self._tags.add(tag)
            self._tags = set(sorted(self._tags))
            return self.__changed()
        return False

    def remove_tag(self, tag: str) -> bool:
        '''Видаляє тег з контакту
        Args:
            tag (str): тег для видалення
        Returns:
            bool: True, якщо теги видалені успішно, False в іншому випадку
        '''
        tag = tag.strip()
        if tag in self._tags:
            self._tags.remove(tag)
            return self.__changed()
        return False

    @property
    def notes(self) -> str | None:
        """Повертає нотатки контакту або None, якщо нотатки не встановлені"""
        return self._notes.value if self._notes else None

    @notes.setter
    def notes(self, value: str) -> bool:
        '''Встановлює нотатки для контакту
        Args:
            value (str): текст нотаток для встановлення
        Returns:
            bool: True, якщо нотатки оновлені успішно, False в іншому випадку
        '''
        if not value:
            return False
        self._notes = Notes(value)
        return self.__changed()

    def pop_notes(self) -> bool:
        '''Видаляє нотатки з контакту
        Returns:
            bool: True, якщо нотатки видалені успішно, False в іншому випадку
        '''
        self._notes = None
        return self.__changed()
