'''Основий модуль для роботи з контактами'''
'''ToDO:
- додайте функцію для збереження контактів у файл формату JSON
- додайте функцію для завантаження контактів з файлу
- додайте функцію для експорту контактів у форматі vCard        '''

from collections import UserDict
from src.ContactHelper.models.contact import Contact
from src.ContactHelper.utils import validate_phone_number, validate_email


class AddressBook(UserDict):
    '''Клас для роботи з контактами'''
    def __init__(self):
        super().__init__()
        # Прапорець для відстеження змін у адресній книзі, який буде використовуватися для визначення, чи потрібно зберігати зміни при виході з програми.
        self._ischanged = False
    
    def __str__(self) -> str:
        return f'AddressBook with {len(self.data)} contacts'
 
    @property
    def ischanged(self) -> bool:
        '''Повертає True, якщо адресна книга була змінена, інакше повертає False'''
        return self._ischanged

    def add_contact(self, name: str, phone: str = None, email: str = None, birthday: str = None) -> bool:
        '''Додає контакт до адресної книги
        Args:
            name (str): ім'я контакту
            phone (str): телефонний номер контакту
            email (str): email контакту
            birthday (str): дата народження контакту у форматі YYYY-MM-DD
        Raises:
            ValueError: якщо контакт з таким ім'ям вже існує
        Returns:
            bool: True, якщо контакт додано, False в іншому випадку'''
        pass        

    def get_contact(self, name: str) -> Contact:
        '''Повертає контакт за ім'ям
        Args:
            name (str): ім'я контакту для пошуку
        Returns:
            Contact: контакт з вказаним ім'ям або None, якщо контакт не знайдено'''
        pass

    def delete_contact(self, name: str) -> bool:
        '''Видаляє контакт за ім'ям
        Args:
            name (str): ім'я контакту для видалення
        Returns:
            bool: True, якщо контакт видалено, False в іншому випадку'''
        pass

    def set_birthday(self, name: str, date: str) -> bool:
        '''Встановлює дату народження для контакту
        Args:
            name (str): ім'я контакту для якого потрібно встановити дату народження
            date (str): дата народження для встановлення у форматі YYYY-MM-DD
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено або якщо дата народження не відповідає формату YYYY-MM-DD
        Returns:
            bool: True, якщо дата народження встановлена, False в іншому випадку'''
        pass

    def update_phone(self, name: str, new_phone: str, phone: str = None) -> bool:
        '''Додає або оновлює телефонний номер для контакту
        Args:
            name (str): ім'я контакту для якого потрібно додати телефонний номер
            new_phone (str): новий телефонний номер для дoдавання у форматі +380XXXXXXXXX
            phone (str): телефонний номер для заміни у форматі +380XXXXXXXXX
        Raises:
            ValueError: якщо контакт з вказаним ім'ям не знайдено або якщо телефонний номер не відповідає формату +380XXXXXXXXX
        Returns:
            bool: True, якщо телефонний номер додано, False в іншому випадку'''
        pass