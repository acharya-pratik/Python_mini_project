# 🗄️ Folder: member2/ (Database & Automation)

### 📄 `schema.sql`
- **What it does:** Defines the structure of `patients`, `admissions`, and `billing` tables.
- **Reason:** Implements a 3rd Normal Form (3NF) relational model for clean storage.

### 📄 `init_db.py`
- **What it does:** Reads `schema.sql` and executes it inside MySQL.
- **Reason:** Automates the creation of the database so any new user can set up the tables with one click.

### 📄 `scheduler.py`
- **What it does:** Uses `apscheduler` to run `member1.run_ETL` automatically every day.
- **Reason:** To make the system "Production-Ready." It handles data refresh without manual interference.
