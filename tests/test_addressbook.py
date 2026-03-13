from ContactHelper.core import AddressBook
from ContactHelper.models.contact import Contact


def test_logger_setup():
    from ContactHelper.logger import setup_logger
    logger = setup_logger()
    assert logger.name == "ContactHelper"
    assert logger.level == 20  # INFO level

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

def test_update_phone():
    contact: Contact = Contact("Kate")
    contact.change_phone("123456789")
    assert contact.phones[0].value == "+380123456789"

    contact.change_phone("987654321", "123456789")

    assert len(contact.phones) == 1
    assert contact.phones[0].value == "+380987654321"

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

def test_set_email():
    contact: Contact = Contact("Bob")
    contact.email = "bob@example.com"
    assert contact.email == "bob@example.com"   

def test_set_birthday():
    contact: Contact = Contact("Charlie")
    contact.birthday = "1990-08-15"
    assert contact.birthday.value.strftime("%d.%m.%Y") == "15.08.1990"

def test_set_address():
    contact: Contact = Contact("Charlie")
    contact.address = "Kyiv, Pryvokzalna str., 1A"
    assert contact.address == "Kyiv, Pryvokzalna str., 1A"


def test_add_tags():
    contact: Contact = Contact("Charlie")
    assert contact.add_tag("friend")
    assert contact.add_tag("colleague")

    assert contact.tags.index("colleague") == 1
    assert contact.tags.index("friend") == 0

def test_remove_tags():
    contact: Contact = Contact("Diana")
    assert contact.add_tag("family")
    assert contact.add_tag("gym")

    assert contact.tags.index("gym") >= 0
    assert contact.tags.index("family") >= 1

    contact.remove_tag("gym")
    assert contact.tags.index("family") == 0

def test_add_note():
    contact: Contact = Contact("Eve")
    contact.notes = "Likes hiking"

    assert contact.notes == "Likes hiking"
    contact.notes = "Also likes swimming"
    assert contact.notes == "Also likes swimming"

def test_notes_empty():
    contact: Contact = Contact("Frank")
    contact.pop_notes()
    assert not contact.notes
