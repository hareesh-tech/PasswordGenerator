# PassFort: Simple, Secure, Unbreachable Password Fortress

PassFort is a cross-platform, secure password generator with an enterprise-level UI, built with Python and Kivy. It allows users to generate strong, cryptographically secure passwords, save them locally in a hashed format, and manage them with a unique ID.


## Features

- **Secure Password Generation**: Uses `secrets` module for generating cryptographically strong random passwords.
- **Customizable Options**:
    - Set password length (between 8 and 64 characters).
    - Include/exclude symbols.
    - Generate text-only or numbers-only passwords.
- **Local Storage**: Save generated passwords with a Unique ID (UID) to a local SQLite database (`pass_fort.db`).
- **Secure Hashing**: Passwords are not stored in plain text. They are hashed using SHA-256 before being saved.
- **Activity Logging**: All major events, such as password generation and storage, are logged to `pass_fort.log` for auditing purposes.
- **Modern UI**: A clean and modern UI built with Kivy, featuring animations and a professional look.

## Project Structure

The project is structured into separate modules for clarity and maintainability:

```

├── app/
│   ├── __init__.py
│   ├── backend.py      # Handles database and password generation logic
|   └── frontend.py     # Contains the Kivy UI and application logic
|── Output
|   ├── pass_fort.db    # SQLite database for storing passwords
|   └── pass_fort.log   # Log file for application events
|── main.py             # Main entry point for the application
└── requirements.txt    # Python dependencies

```

## Getting Started

### Prerequisites

- Python 3.6+
- `pip` for installing packages

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hareesh-tech/PasswordGenerator.git
    cd PasswordGenerator
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To start PassFort, run the `main.py` script:

```bash
python main.py
```

## How to Use

1.  **Generate a Password**:
    - Adjust the slider or type in the input box to set the desired password length.
    - Use the checkboxes to customize the character set.
    - Click the "GENERATE PASSWORD" button.

2.  **Copy or Save the Password**:
    - A popup will appear with your new password.
    - Click "Copy" to copy the password to your clipboard.
    - Click "Save" to store the password. You will be prompted to enter a Unique ID (UID) to associate with the password.

3.  **View Logs and Database**:
    - The `pass_fort.log` file contains a history of all generated and saved passwords (including the plain text password for recovery, so handle this file with care).
    - The `pass_fort.db` file is an SQLite database containing the UIDs and their corresponding hashed passwords.

## Contributing

Contributions are welcome! If you have ideas for new features or have found a bug, please open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
