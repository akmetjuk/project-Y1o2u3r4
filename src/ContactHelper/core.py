from collections import UserDict
from src.ContactHelper.models.contact import Contact


class AddressBook(UserDict):
    '''Клас для роботи з контактами'''
    def __init__(self):
        super().__init__()
        self._ischanged = False

    def __str__(self) -> str:
        return f'AddressBook with {len(self.data)} contacts'

    @property
    def ischanged(self) -> bool:
        '''Повертає True, якщо адресна книга
        була змінена, інакше повертає False'''
        return self._ischanged

    def find(self, name: str) -> Contact | None:
        """
        Знаходить запис за ім'ям.
        Args:
            name: Ім'я контакту для пошуку
        Returns:
            Знайдений об'єкт Contact або None, якщо не знайдено
        """
        return self.data.get(str.lower(name).strip())

    def save_data(self, filename: str) -> bool:
        '''Зберігає дані адресної книги у файл
        Args:
            filename (str): ім'я файлу для збереження даних
        '''
        pass

    @classmethod
    def load_data(cls, filename: str) -> 'AddressBook':
        """Завантажити з файлу або створити нову адресну книгу.
        Args:
            filename: Шлях до файлу для завантаження
        Returns:
            Завантажена адресна книга або нова, якщо файл не знайдено
        Raises:
            ValueError якщо файл не вказаний або
            не знайдено або виникли проблеми з читанням файлу
        """
        pass

    def get_upcoming_birthdays(self, days: int = 7) -> list[Contact] | None:
        """Отримати список користувачів з днями
        народження  протягом наступних days днів.
        Args:
            days: Кількість днів для перевірки
            (за замовчуванням 7) від 1 до 365
        Returns:
            Перелік співробітників для привітання
        Raises:
            ValueError: якщо days не є цілим числом від 1 до 365
        """
        if not isinstance(days, int) or not (1 <= days <= 365):
            raise ValueError("Days must be an integer between 1 and 365")
        return None

    def add_contact(self,
                    name: str,
                    phone: str = None,
                    email: str = None,
                    birthday: str = None,
                    address: str = None) -> bool:
        '''Додає контакт до адресної книги
        Args:
            name (str): ім'я контакту
            phone (str): телефонний номер контакту
            email (str): email контакту
            birthday (str): дата народження контакту у форматі YYYY-MM-DD
            address (str): адреса контакту
        Raises:
            ValueError: якщо контакт з таким ім'ям вже існує
        Returns:
            bool: True, якщо контакт додано, False в іншому випадку'''
        if self.find(name):
            raise IndexError(f"Contact '{name}' already exists.")
        contact: Contact = Contact(name)
        if phone:
            contact.change_phone(phone)
        contact.birthday = birthday
        contact.email = email
        contact.address = address
        n: str = str.lower(name).strip()
        self.data[n] = contact
        self._ischanged = True
        return True

    def get_contact(self, name: str) -> Contact | None:
        '''Повертає контакт за ім'ям
        Args:
            name (str): ім'я контакту для пошуку
        Returns:
            Contact: контакт з вказаним ім'ям або
            None, якщо контакт не знайдено'''
        n: str = str.lower(name).strip()
        if self.find(n):
            return self.data[n]
        return None

    def delete_contact(self, name: str) -> bool:
        '''Видаляє контакт за ім'ям
        Args:
            name (str): ім'я контакту для видалення
        Returns:
            bool: True, якщо контакт видалено,
            False в іншому випадку'''
        if self.data.pop(str.lower(name).strip()):
            self._ischanged = True
            return True
        return False

    def set_birthday(self, name: str, date: str) -> bool:
        '''Встановлює дату народження для контакту
        Args:
            name (str): ім'я контакту для якого потрібно
                встановити дату народження
            date (str): дата народження для встановлення у форматі YYYY-MM-DD
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено
            або якщо дата народження не відповідає формату YYYY-MM-DD
        Returns:
            bool: True, якщо дата народження встановлена,
            False в іншому випадку'''
        n: str = str.lower(name).strip()
        record: Contact = self.find(n)
        if not record:
            raise KeyError(f"Contact '{name}' not found.")
        record.birthday = date
        self._ischanged = True
        return True

    def set_email(self, name: str, email: str) -> bool:
        '''Встановлює електронну пошту для контакту
        Args:
            name (str): ім'я контакту для якого потрібно
                встановити електронну пошту
            email (str): електронна пошта для встановлення у форматі
                example@domain.com
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено
            або якщо електронна пошта не відповідає формату
        Returns:
            bool: True, якщо електронна пошта встановлена,
            False в іншому випадку'''
        contact: Contact = self.find(name)
        if not contact:
            raise KeyError(f"Contact '{name}' not found.")
        contact.email = email
        self._ischanged = True
        return True

    def set_address(self, name: str, address: str) -> bool:
        '''Встановлює адресу для контакту
        Args:
            name (str): ім'я контакту для якого потрібно
                встановити адресу
            address (str): адреса для встановлення
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено
        Returns:
            bool: True, якщо адреса встановлена,
            False в іншому випадку'''
        contact: Contact = self.find(name)
        if not contact:
            raise KeyError(f"Contact '{name}' not found.")
        contact.address = address
        self._ischanged = True
        return True

    def update_phone(self, name: str,
                     new_phone: str,
                     phone: str = None) -> bool:
        '''Додає або оновлює телефонний номер для контакту
        Args:
            name (str): ім'я контакту для якого
                потрібно додати телефонний номер
            new_phone (str): новий телефонний номер
                для дoдавання у форматі +380XXXXXXXXX
            phone (str): телефонний номер для заміни у форматі +380XXXXXXXXX
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено
            або якщо телефонний номер не відповідає формату +380XXXXXXXXX
        Returns:
            bool: True, якщо телефонний номер додано, False в іншому випадку'''
        n: str = str.lower(name).strip()
        contact: Contact = self.find(n)
        if not contact:
            raise KeyError(f"Contact '{name}' not found.")
        if contact.change_phone(new_phone, phone):
            self._ischanged = True
            return True
        return False

    def delete_phone(self, name: str, phone: str) -> bool:
        '''Видаляє телефонний номер для контакту
        Args:
            name (str): ім'я контакту для якого
            потрібно видалити телефонний номер
            phone (str): телефонний номер для
            видалення у форматі +380XXXXXXXXX
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено
            або якщо телефонний номер не відповідає формату +380XXXXXXXXX
        Returns:
            bool: True, якщо телефонний номер видалено,
            False в іншому випадку'''
        contact: Contact = self.find(name)
        if not contact:
            raise KeyError(f"Contact '{name}' not found.")
        if contact.remove_phone(phone):
            self._ischanged = True
            return True
        return False
