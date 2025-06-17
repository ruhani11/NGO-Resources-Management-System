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
├── Script1.sql         # Script to create volunteer table
├── Script2.sql         # Script to create inventory table
├── Script3.sql         # Script to create donation table
└── README.md           # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ruhani11/NGO-Resources-Management-System
cd ngo-resources-management

2. Set Up the MySQL Database
Open MySQL Workbench

Run CreateDatabase.sql to create the database

Run Script1.sql, Script2.sql, and Script3.sql to create the required tables

3. Configure Database Connection
Edit db_config.py to match your local MySQL credentials:

python
Copy code
# db_config.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ngo_database"
    )
4. Test Connection
bash
Copy code
python test_connection.py
If successful, you’ll see:

css
Copy code
✅ Connected to MySQL!
5. Launch the Application
bash
Copy code
streamlit run app.py

📌 Future Enhancements
📧 Email notifications to volunteers/donors

🗃️ Export data as Excel/PDF

🧑‍💼 Admin login & role-based access

📱 Mobile-friendly UI

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.
