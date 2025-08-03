# Employee Asset Management System

## Overview

The **Employee Asset Management System** is a FastAPI-based web application designed to manage employee records, company assets, and asset-employee relationships. It supports full CRUD operations, real-time asset assignment, and a dashboard view for asset distribution analysis.

---

## Features

* Add, update, delete, and retrieve employee details
* Add, update, delete, and retrieve asset records
* Assign and unassign assets to employees
* View dashboard with employee-asset distribution
* Asynchronous operations using PostgreSQL
* Full test coverage with isolated in-memory testing

---

## Tech Stack

* **Framework:** FastAPI
* **ORM:** SQLModel, SQLAlchemy
* **Database:** PostgreSQL (production), SQLite (testing)
* **Testing:** unittest, httpx
* **Language:** Python 3.10+

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/aryansinha16/python-assignment.git
cd python-assignment
```

### 2. Install Dependencies

Create a virtual environment and install the required packages.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Example `requirements.txt`:

```
fastapi
sqlmodel
asyncpg
uvicorn
httpx
sqlalchemy
```

### 3. Configure the Database

Edit the `DATABASE_URL` in `database.py`:

```python
DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/Employee_Details"
```

You can also change the username and password in `database.py` to match your local PostgreSQL credentials.

Ensure PostgreSQL is running and a database named `Employee_Details` exists.

### 4. Run the Application

```bash
uvicorn main:app --reload
```

Visit the interactive API docs at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Routes

### Employees (`/employee`)

* `POST /createemployee`
* `PATCH /editemployee/{employeeid}`
* `DELETE /deleteemployee/{employeeid}` – *Note: To delete an employee, you must first delete all asset mappings attached to that employee.*
* `GET /getemployee/{employeeid}`
* `GET /getallemployee`

### Assets (`/asset`)

* `POST /createasset`
* `PATCH /editasset/{assetid}`
* `DELETE /deleteasset/{assetid}`
* `GET /getallasset`

### Mappings (`/mapping`)

* `POST /assignassetmapping`
* `GET /getallassets/{employeeid}`
* `DELETE /removeassetmapping/{mappingid}`

### Dashboard (`/dashboard`)

* `GET /getdetails`

---

## Database Schema

The database consists of the following tables:

* **EmployeeDetails**
* **AssetDetails**
* **EmployeeAssetMapping**

These are defined in `schema.py` using SQLModel.

---

## Running Tests

Run the test suite using:

```bash
python test.py
```

Tests are written using Python’s `unittest` module and run against an isolated in-memory SQLite database.

---

## Project Structure

```
.
├── main.py              # Application entrypoint
├── database.py          # DB engine and session configuration
├── routers/             # API route modules
│   ├── employee.py      # Employee endpoints
│   ├── asset.py         # Asset endpoints
│   ├── mapping.py       # Mapping endpoints
│   ├── dashboard.py     # Dashboard logic
├── schema.py            # Data models
├── test.py              # Unit tests
└── README.md            # Project documentation
```

---

## Author

Developed by Aryan Sinha
