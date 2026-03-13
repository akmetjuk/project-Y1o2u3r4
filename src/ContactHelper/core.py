from collections import UserDict
import pickle
from src.ContactHelper.models.contact import Contact
import logging


logger = logging.getLogger("ContactHelper")


class AddressBook(UserDict):
    '''Клас для роботи з контактами'''
    def __init__(self):
        super().__init__()
        self._ischanged: bool = False
        self._version: int = 1

    def __str__(self) -> str:
        return f'AddressBook with {len(self.data)} contacts'

    @property
    def ischanged(self) -> bool:
        '''Повертає True, якщо адресна книга
        була змінена, інакше повертає False'''
        return self._ischanged

    @property
    def version(self) -> int:
        '''Повертає поточну версію адресної книги'''
        return self._version

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
        if not self.data or not self._ischanged:
            return False
        if not filename:
            if self._filename:
                filename = self._filename
            else:
                raise ValueError("Filename is not specified.")

        self._version += 1
        self._ischanged = False
        with open(filename, "wb") as f:
            pickle.dump(self, f)
        logger.info(f"Successfully saved data to {filename}")

    @classmethod
    def load_data(cls, filename: str) -> 'AddressBook':
        """Завантажити з файлу або створити нову адресну книгу.
        Args:
            filename: Шлях до файлу для завантаження
        Returns:
            Завантажена адресна книга або нова,
            якщо файл не знайдено
        Raises:
            ValueError якщо файл не вказаний або
            не знайдено або виникли проблеми з читанням файлу
        """        
        if not filename:
            raise ValueError("Filename is not specified.")
        try:
            with open(filename, "rb") as f:
                book = pickle.load(f)
                book._filename = filename
                book._ischanged = False
                logger.info(f"Successfully loaded data from {filename}")
                return book
        except FileNotFoundError:
            logger.warning(f"File '{filename}' not found. Creating new AddressBook.")
            return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

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
        if birthday:
            contact.birthday = birthday
        if email:
            contact.email = email
        if address:
            contact.address = address
        n: str = str.lower(name).strip()
        self.data[n] = contact
        self._ischanged = True
        logger.info(f"added contact: {name}")
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
            logger.info(f"deleted contact: {name}")
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
        contact: Contact = self.find(n)
        if not contact:
            raise KeyError(f"Contact '{name}' not found.")
        contact.birthday = date
        logger.info(f"updated contact {contact.name}",
                    f"birthday: {contact.birthday}")
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
        logger.info(f"updated contact {contact.name} email: {contact.email}")
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
        logger.info(f"updated contact {contact.name}",
                    f"address: {contact.address}")
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
            logger.info(f"updated contact {contact.name}",
                        f"phone:{contact.phone}",
                        {f'replaced {phone}' if phone else 'added new'})
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
            logger.info(f"deleted phone {phone} from contact {contact.name}")
            self._ischanged = True
            return True
        return False

    def add_tag(self, name: str, tags: str) -> bool:
        '''Додає тег для контакту
        Args:
            name (str): ім'я контакту для якого
            потрібно додати тег
            tags (str): теги для додавання
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено
        Returns:
            bool: True, якщо тег додано, False в іншому випадку'''
        contact: Contact = self.find(name)
        if not contact:
            raise KeyError(f"Contact '{name}' not found.")
        try:
            contact.tags = set(tags.split(' '))
            logger.info(f"added tag {tags} to contact {contact.name}")
            self._ischanged = True
            return True
        except AttributeError:
            raise ValueError("Invalid tag format.")

    def delete_tag(self, name: str, tag: str) -> bool:
        '''Видаляє тег для контакту
        Args:
            name (str): ім'я контакту для якого
            потрібно видалити тег
            tag (str): тег для видалення
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено
        Returns:
            bool: True, якщо тег видалено, False в іншому випадку'''
        contact: Contact = self.find(name)
        if not contact:
            raise KeyError(f"Contact '{name}' not found.")
        if contact.remove_tag(tag):
            logger.info(f"deleted tag {tag} from contact {contact.name}")
            self._ischanged = True
            return True
        return False

    def find_by_tag(self, tag: str) -> list[Contact] | None:
        '''Знаходить контакти за тегом
        Args:
            tag (str): тег для пошуку
        Returns:
            list[Contact]: список контактів з вказаним тегом або None, якщо не знайдено'''
        return [contact for contact in self.data.values() if tag in contact.tags]

    def set_notes(self, name: str, notes: str) -> bool:
        '''Додає нотатку для контакту
        Args:
            name (str): ім'я контакту для якого
            потрібно додати нотатку
            notes (str): нотатки для додавання
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено
        Returns:
            bool: True, якщо нотатки додано, False в іншому випадку'''
        contact: Contact = self.find(name)
        if not contact:
            raise KeyError(f"Contact '{name}' not found.")
        try:
            contact.notes = notes.strip()
            logger.info(f"added notes {notes[:30]} to contact {contact.name}")
            self._ischanged = True
            return True
        except AttributeError:
            raise ValueError("Invalid notes format.")

    def delete_notes(self, name: str) -> bool:
        '''Видаляє нотатку для контакту
        Args:
            name (str): ім'я контакту для якого
            потрібно видалити нотатку
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено
        Returns:
            bool: True, якщо нотатки видалено, False в іншому випадку'''
        contact: Contact = self.find(name)
        if not contact:
            raise KeyError(f"Contact '{name}' not found.")
        if contact.remove_notes():
            logger.info(f"deleted notes from contact {contact.name}")
            self._ischanged = True
            return True
        return False

    def find_by_notes(self, keyword: str) -> list[Contact] | None:
        '''Знаходить контакти за ключовим словом в нотатках
        Args:
            keyword (str): ключове слово для пошуку в нотатках
        Returns:
            list[Contact]: список контактів з вказаним
            ключовим словом в нотатках або None, якщо не знайдено'''
        return [contact for contact in self.data.values() if contact.notes and keyword in contact.notes]
