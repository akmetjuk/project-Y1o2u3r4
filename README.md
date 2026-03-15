# ContactHelper

A command-line interface (CLI) tool for managing personal contacts and address book. Store and organize contact information including names, phone numbers, emails, birthdays, addresses, tags, and notes.

## Features

- **Contact Management**: Add, view, update, and delete contacts
- **Multiple Phone Numbers**: Store multiple phone numbers per contact
- **Rich Contact Information**: Support for email, birthday, address, tags, and notes
- **Search Functionality**: Find contacts by name, phone, tag, or notes
- **Birthday Reminders**: Get upcoming birthdays within a specified number of days
- **Persistent Storage**: Data is automatically saved to a local file
- **Colored Output**: Enhanced CLI experience with color-coded information
- **Validation**: Built-in validation for phone numbers, emails, and dates

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

1. Clone or download the repository
2. Navigate to the project directory
3. Install the package:

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

## Usage

After installation, run the CLI tool:

```bash
contacthelper
```

### Available Commands

#### Basic Contact Operations

- `add <name> [phone] [email] [birthday]` - Add a new contact
  - Birthday format: YYYY-MM-DD
  - Example: `add John +380501234567 john@example.com 1990-05-15`

- `get <name>` - Display detailed information about a contact
  - Example: `get John`

- `delete <name>` - Remove a contact
  - Example: `delete John`

#### Phone Management

- `update-phone <name> <new_phone> [old_phone]` - Add or replace phone number
  - Phone format: +380XXXXXXXXX
  - If old_phone is provided, it replaces the existing number
  - Example: `update-phone John +380509876543 +380501234567`

#### Contact Details

- `set-email <name> <email>` - Set email address
  - Example: `set-email John john.doe@example.com`

- `set-birthday <name> <YYYY-MM-DD>` - Set birthday
  - Example: `set-birthday John 1990-05-15`

- `set-address <name> <address>` - Set address
  - Example: `set-address John "Kyiv, Main Street 123"`

- `set-note <name> <note text>` - Add notes to a contact
  - Example: `set-note John "Met at conference"`

- `delete-note <name>` - Remove notes from a contact
  - Example: `delete-note John`

#### Tags

- `add-tag <name> <tag>` - Add a tag to a contact
  - Tags are alphanumeric and case-insensitive
  - Example: `add-tag John friend`

- `delete-tag <name> <tag>` - Remove a specific tag from a contact
  - Example: `delete-tag John friend`

#### Search and Find

- `find-by <field> <keyword>` - Search contacts by field
  - Supported fields: `name`, `note`, `tag`, `phone`
  - Example: `find-by name John`
  - Example: `find-by tag friend`
  - Example: `find-by phone +380501234567`

- `upcome-birthdays [days]` - Show upcoming birthdays
  - Default: 7 days
  - Example: `upcome-birthdays 30`

#### General

- `help` - Display all available commands with descriptions
- `exit` or `quit` - Exit the application

### Data Storage

- Contact data is automatically saved to `addressbook.pkl` in the application directory
- Data persists between sessions
- The application loads existing data on startup

### Validation Rules

- **Phone Numbers**: Must be in format +380XXXXXXXXX (12 digits starting with +380)
- **Emails**: Standard email format (user@domain.com)
- **Birthdays**: YYYY-MM-DD format
- **Tags**: Alphanumeric characters only, case-insensitive

## Examples

### Adding a Contact
```
Enter command: add Alice +380501234567 alice@example.com 1985-03-20
Contact 'Alice' added.

Enter command: set-address Alice "Kyiv, Independence Square"
You set address: Kyiv, Independence Square to the 'Alice'

Enter command: add-tag Alice friend
You add tags: friend to the 'Alice'
```

### Searching Contacts
```
Enter command: find-by tag friend
Your result is 1 contacts by searching 'friend' in 'tag'
    - Alice
for details use command get <name>

Enter command: get Alice
    Name: Alice
    Phones: +380501234567
    Email: alice@example.com
    Birthday: 1985-03-20
    Address: Kyiv, Independence Square
    Tags: friend
    Note: —
```

### Birthday Reminders
```
Enter command: upcome-birthdays 30
You have 1 birthdays next 30 days:
    Contact 'Alice' has birthday on 1985-03-20.
```

## Development

### Running Tests

```bash
pytest
```

### Project Structure

```
src/ContactHelper/
├── __init__.py
├── cli.py          # Command-line interface
├── core.py         # AddressBook class and main logic
├── logger.py       # Logging configuration
├── utils.py        # Utility functions and validation
└── models/
    ├── __init__.py
    ├── contact.py  # Contact class
    ├── enums.py    # Enums for sorting
    └── fields.py   # Field classes (Phone, Email, etc.)
```

## License

This project is part of a Heliteam assignment and follows the project's licensing terms.
