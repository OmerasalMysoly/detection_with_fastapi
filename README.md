
# Intern API Project

This project is a simple test API designed for interns to learn and practice API development processes.

## Installation

Before running the project, you need to install the required packages:

```bash
pip install -r requirements.txt
```

## Running

You can use the following command to start the API:

```bash
python my_app.py
```

The application will run by default at `http://127.0.0.1:8000`.
You can access the Swagger documentation at `http://127.0.0.1:8000/docs`.

## Version History

- **0.0.1**: Initial release

## Project Structure

- **my_app.py**: The main entry point of the application. Endpoints are defined here.
- **system/middleware.py**: Middleware layer that logs requests and performs security checks.
- **view/**: Pydantic models and data schemas are located here.
- **logs.txt**: Failed or unauthorized requests are logged to this file.

## Logging

The system uses file-based logging instead of database logging.
- Non-200 OK responses
- 401 Unauthorized access attempts
- 500 Internal Server Error occurrences

These are automatically saved to the `logs.txt` file.

## Endpoints

### `GET /`
Verifies that the application is running and returns the current version information via a web interface.

### `POST /check-email`
Checks the format of the given email address using regex (regular expressions).
- **Parameters:** `secret` (string), `params` (MAIL_VALIDATION model)
- **Success (200):** If the email format is valid, returns `is_valid: "true"`.
- **Error (200):** If the email format is invalid, returns `is_valid: "false"`.
