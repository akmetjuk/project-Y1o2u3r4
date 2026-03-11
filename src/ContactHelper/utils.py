'''
ToDo:
- додайте функцію валідації телефонного номера, яка буде перевіряти чи номер
телефону відповідає формату +380XXXXXXXXX, де X - це цифра від 0 до 9. Якщо
номер телефону не відповідає цьому формату, функція повинна виводити
повідомлення про помилку.
- додайте функцію валідації електронної пошти, яка буде перевіряти чи
електронна пошта відповідає формату user@example.com
'''
import re


def validate_phone_number(phone_number: str) -> str:
    """Повертає телефонний номер, якщо його можна вважати валідним або
    повертає помилку
    Args:
    phone_number (str): телефонний номер у форматі +380XXXXXXXXX
    Returns:
        str: телефонний номер, якщо він валідний
    Raises:
        ValueError: якщо телефонний номер не відповідає формату +380XXXXXXXXX
    """
    if not isinstance(phone_number, str):
        raise ValueError("Phone number must be a string")

    digits = re.sub(r"\D", "", phone_number)

    if re.fullmatch(r"380\d{9}", digits):
        return f"+{digits}"

    if re.fullmatch(r"0\d{9}", digits):
        return f"+38{digits}"

    if re.fullmatch(r"\d{9}", digits):
        return f"+380{digits}"

    raise ValueError("Phone number must be in format +380XXXXXXXXX")


def validate_email(email: str) -> str:
    """Повертає електронну пошту, якщо її можна вважати валідною або
    повертає помилку
    Args:
    email (str): електронна пошта у форматі user@example.com
    Returns:
        str: електронна пошта, якщо вона валідна
    Raises:
        ValueError: якщо електронна пошта не відповідає формату
        user@example.com
    """
    if not isinstance(email, str):
        raise ValueError("Email must be a string")

    email = email.strip()

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.fullmatch(pattern, email):
        raise ValueError("Email must be in format user@example.com")

    return email
