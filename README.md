# FakedPy

A Python library for generating fake data with various output formats.

## Installation

```bash
pip install fakedpy
```

## Features

- Generate various types of fake data
- Support multiple output formats (CSV, JSON, Excel, Parquet), but CSV as a default
- Support localization (including Indonesian)
- Generate related/dependent data
- Easy to use and flexible

## Basic Usage

```python
from fakedpy import FakedGenerator

# Initialize generator
generator = FakedGenerator(locale='id_ID')  # For Indonesian data
# orr
generator = FakedGenerator(locale=['id_ID', 'en_US'])  # For mixed data

# Generate simple data
df = generator.generate(
    rows=5,
    fields=["name", "email", "address"]
)

# Save to different formats
df = generator.generate(
    rows=5,
    fields=["name", "email", "job"],
    output_format="json",
    output_path="data/output"
)
```

## Available Fields

### Personal Information
- name: Full name
- first_name: First name
- last_name: Last name
- email: Email address
- phone_number: Phone number
- date: Date
- gender: Gender

### Address Information
- address: Full address
- street_address: Street address
- city: City
- state: State/Province
- country: Country
- postcode: Postal code
- latitude: Latitude
- longitude: Longitude

### Internet Information
- username: Username
- password: Password
- domain_name: Domain name
- url: URL address
- ipv4: IPv4 address
- ipv6: IPv6 address
- mac_address: MAC address

### Company Information
- company: Company name
- job: Job title

### Financial Information
- credit_card_number: Credit card number
- credit_card_provider: Credit card provider
- currency_code: Currency code

### Technology
- file_name: File name
- file_extension: File extension
- mime_type: MIME type

### Miscellaneous
- text: Text paragraph
- word: Single word
- sentence: Single sentence
- paragraph: Full paragraph
- color_name: Color name
- hex_color: HEX color code
- rgb_color: RGB color code

## Advanced Usage

### Related Data
```python
# Generate data with ID and department
df = generator.generate(
    rows=5,
    fields=["user_id", "name", "department"],
    related_fields={
        "user_id": {"type": "counter", "start": 1000},
        "department": {
            "type": "choice",
            "values": ["IT", "HR", "Finance", "Marketing"]
        }
    }
)
```

### Different Output Formats
```python
# CSV
df = generator.generate(
    rows=10,
    fields=["name", "email"],
    output_format="csv",
    output_path="data/users"
)

# JSON
df = generator.generate(
    rows=10,
    fields=["name", "email"],
    output_format="json",
    output_path="data/users"
)

# Excel
df = generator.generate(
    rows=10,
    fields=["name", "email"],
    output_format="excel",
    output_path="data/users"
)

# Parquet
df = generator.generate(
    rows=10,
    fields=["name", "email"],
    output_format="parquet",
    output_path="data/users"
)
```

## Contributing

Feel free to contribute by creating issues or pull requests in this repository.

## License

[MIT License](LICENSE)
