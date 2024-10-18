Employee Food Management System
This application is designed to manage employee attendance, medical checks, and food purchasing using QR codes. It also includes a settings page where the API connection URL can be configured. The application is built using Flet for the user interface.

Features
Attendance Management: Track when employees arrive using QR code scanning.
Medical Check: Verify employee access via daily medical checks.
Food Purchase Tracking: Manage employee food purchases using a balance limit.
Settings: Configure the API URL for backend integration.
Table of Contents
Installation
Usage
Project Structure
API Integration
Contributing
License
Installation
Prerequisites
Before you begin, ensure you have met the following requirements:

You have Python 3.9 or above installed on your machine.
You have installed the required Python packages listed in requirements.txt.
Steps
Clone the repository:

```bash
git clone git@github.com:zhandos717/accounting-system-canteens.git
```
```bash
cd accounting-system-canteens
```

Set up a virtual environment:

bash
Copy code
python3 -m venv .venv
source .venv/bin/activate  # For Windows use .venv\Scripts\activate
Install dependencies:

```bash
pip install -r requirements.txt
Run the application:
```

```bash
python main.py
```

Usage
Once the application is running, you'll be able to:

Manage Employee Attendance: Scan the employee’s QR code and register their attendance.
Medical Check: After employees pass a medical check, their access is activated for the day.
Food Purchase: Employees can purchase food within their daily limit by scanning their QR code.
Configure API URL: Use the settings page to define the backend API connection.
Main Features
Home Page:

Register employee attendance.
Navigate to medical check, food purchase, or settings pages.
Medical Check:

Scan employees' QR codes to validate their daily access.
Food Purchase:

Record food purchases and deduct the cost from the employee’s daily allowance.
Settings Page:

Specify the API URL for backend integration.
Project Structure
bash
Copy code
```
.
├── config.py                   # Handles API URL configuration loading and saving
├── main.py                     # Main application entry point
└── pages/                      # UI pages for the application
    ├── home.py                 # Home page with attendance registration
    ├── medical.py              # Medical check page
    ├── buy_food.py             # Food purchase page
    └── settings.py             # Settings page to configure the API URL
```
Explanation of Key Files
config.py: Handles loading and saving of the API URL configuration to a JSON file (config.json).
main.py: The main application file where routing between different pages occurs.
pages/: Contains all the Flet-based pages for different functionalities.
API Integration
This application connects to a backend API to track employee attendance, medical checks, and food purchases.

API URL: The base URL for the API can be configured on the settings page. By default, it's set to http://localhost:8000.
Make sure your backend API supports the following endpoints:

POST /attendance: For recording employee attendance.
POST /medical_check: For validating daily medical checks.
POST /buy_food: For tracking food purchases.
You can adjust the API URL by navigating to the settings page and entering the correct base URL for your backend.

Contributing
To contribute to this project:

License
This project is licensed under the MIT License - see the LICENSE file for details.

