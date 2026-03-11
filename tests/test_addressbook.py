from ContactHelper.core import AddressBook
from ContactHelper.models.contact import Contact


def test_add_contact():
    book: AddressBook = AddressBook()
    book.add_contact(name="John")

    assert "john" in book.data
    assert book.find("John").name == "John"


def test_find_contact():
    book: AddressBook = AddressBook()
    book.add_contact(name="Anna")

    found: Contact = book.find("Anna")

    assert found is not None
    assert found.name == "Anna"


def test_delete_contact():
    book: AddressBook = AddressBook()
    book.add_contact(name="Mike")

    assert book.delete_contact("Mike") is True
    assert "mike" not in book.data


def test_add_phone():
    contact: Contact = Contact("Kate")
    contact.change_phone("123456789")

    assert len(contact.phones) == 1
    assert contact.phones[0].value == "+380123456789"

def test_incorrect_phone():
    contact: Contact = Contact("Tom")
    try:
        contact.change_phone("abc123")
    except ValueError as e:
        assert str(e) in ("Phone number must be in format +380XXXXXXXXX","Phone number must be a string")

def test_incorrect_email():
    contact: Contact = Contact("Alice")
    try:
        contact.email = "invalid_email"
    except ValueError as e:
        assert str(e) in ("Email must be in format user@example.com","Email must be a string")