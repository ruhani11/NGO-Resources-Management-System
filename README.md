# 🌱 NGO Resources Management System

A full-stack database management system to streamline resource handling for NGOs. This app helps manage volunteers, donations, and inventory efficiently with a user-friendly interface built using **Python**, **MySQL**, and **Streamlit**.

---

## 🚀 Features

- 👥 Volunteer registration and management  
- 🎁 Donation tracking (books, clothes, funds, etc.)  
- 📦 Inventory record management with stock updates  
- 🔍 Search and filter functionality  
- 📊 Real-time updates to the MySQL database  

---

## 🛠️ Tech Stack

| Layer       | Technology          |
|-------------|---------------------|
| Frontend    | Streamlit (Python)  |
| Backend     | MySQL               |
| Language    | Python 3            |
| Tools Used  | MySQL Workbench, Streamlit, VS Code / Anaconda |

---

## 📁 Project Structure

```
ngo-resources-management/
├── app.py              # Main Streamlit app
├── db_config.py        # MySQL DB connection function
├── test_connection.py  # Script to test database connectivity
├── CreateDatabase.sql  # SQL to create the database
├── Script1.sql         # Script to create all tables
├── Script2.sql         # Script to insert sample data
├── Script3.sql         # Script to create stored procedures
└── README.md           # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ruhani11/NGO-Resources-Management-System
cd ngo-resources-management
```

### 2. Set Up the MySQL Database

- Open **MySQL Workbench**
- Run the following SQL scripts in order:
  1. `CreateDatabase.sql` – to create the database
  2. `Script1.sql` – to create all required tables
  3. `Script2.sql` – to insert sample data
  4. `Script3.sql` – to define stored procedures

### 3. Configure Database Connection

Edit `db_config.py` to match your local MySQL credentials:

```python
# db_config.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ngo_database"
    )
```

### 4. Test Connection

Run the following command to test the connection:

```bash
python test_connection.py
```

If successful, you'll see:

```
✅ Connected to MySQL!
```

### 5. Launch the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

---

## 📌 Future Enhancements

- 📧 Email notifications to volunteers/donors  
- 🗃️ Export data as Excel/PDF  
- 🧑‍💼 Admin login & role-based access  
- 📱 Mobile-friendly UI  

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.
