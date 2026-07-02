# Personal Finance Tracker

A full-stack personal finance web application built using Flask that helps users track income and expenses, visualize spending habits, and receive personalized financial insights. The app combines data visualization and budgeting analytics to provide users with an overview of their financial health.

---

## Features

- User registration and secure authentication
- Add, edit, and delete income and expense transactions
- Search and filter transactions
- Sort transactions by date or amount
- Dashboard displaying:
  - Total income
  - Total expenses
  - Current balance
  - Transaction count
- Spending breakdown by category
- Interactive Chart.js doughnut charts
- Comparison between actual spending and recommended spending
- Automatically generated financial insights
- Financial health score based on spending habits and savings rate

---

## Technologies Used

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLAlchemy

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2 Templates
- Chart.js

### Database

- SQLite

---

## Screenshots

### Home

*<img width="1434" height="630" alt="image" src="https://github.com/user-attachments/assets/ebe12b7c-5c90-46f8-8409-0646dce45619" />*

---

### Login Page

*<img width="1433" height="625" alt="image" src="https://github.com/user-attachments/assets/c93d7777-55a9-4b91-b4ac-93c9b9a5efb8" />*

---

### Dashboard

*<img width="1435" height="623" alt="image" src="https://github.com/user-attachments/assets/f07bc44d-5cf1-4463-9e40-65dbb365f83b" />*

---

### Spending Analysis

*<img width="1434" height="626" alt="image" src="https://github.com/user-attachments/assets/30e33407-781e-406c-92a1-7bc18142260b" />*

---

### Financial Insights

*<img width="1431" height="628" alt="image" src="https://github.com/user-attachments/assets/f4a8780c-4eb4-43e1-8f5c-cbbf041c7b7a" />*

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory

```bash
cd finance-tracker
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser and navigate to

```
http://127.0.0.1:5000
```

---

## Project Structure

```
Finance Tracker
│
├── instance/
│   └── finance.db
│
├── static/
│   └── style.css
│
├── templates/
│   ├── add_transaction.html
│   ├── dashboard.html
│   ├── edit_transaction.html
│   ├── home.html
│   ├── login.html
│   └── register.html
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Financial Analytics

The dashboard calculates several financial metrics automatically, including:

- Spending percentages by category
- Recommended budget allocation comparison
- Savings rate
- Financial health score
- Category-specific spending insights

These metrics update dynamically as transactions are added, edited, or removed.

---

## Future Improvements

- AI-powered budgeting recommendations
- Monthly and yearly spending trends
- Forecast future spending
- CSV import/export
- Recurring transactions
- AWS deployment
- PostgreSQL database support
- Email spending reports

---

## What I Learned

This project strengthened my understanding of:

- Building full-stack Flask applications
- SQLAlchemy ORM and relational databases
- User authentication
- Jinja templating
- Data aggregation and analysis
- Interactive data visualization with Chart.js
- Structuring larger Flask projects
- Designing analytics dashboards from transactional data

---

## Live Demo

*(Coming soon after deployment.)*
