# Tour Cost Calculator — Flask + MySQL

A full-stack web app for calculating and saving tour costs with per-person split options.

## Requirements
- Python 3.8+
- MySQL 5.7+ or 8.0+

---

## Setup

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up the MySQL database
Log into MySQL and run the schema:
```bash
mysql -u root -p < schema.sql
```
This creates the `tour_db` database with `trips` and `tourists` tables.

### 3. Configure database connection
Either edit `app.py` directly (the `DB_CONFIG` dict), or set environment variables:
```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=tour_db
```

On Windows (Command Prompt):
```cmd
set DB_HOST=localhost
set DB_USER=root
set DB_PASSWORD=your_password
set DB_NAME=tour_db
```

### 4. Run the app
```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## Features
- Add multiple tourist names with colored avatars
- Enter 6 cost categories: Transport, Hotel, Food, Tickets, Guide, Misc
- 6 split methods: Equal, Custom %, Organizer pays, Transport split, Hotel+food split, Sponsored
- Auto-calculated per-person and per-day costs
- Save trips to MySQL with full tourist breakdown
- View saved trip history, individual details, and delete records
- Sidebar shows recent trips at a glance

## Database Schema
- **trips** — stores all trip info and cost totals
- **tourists** — linked to each trip, stores name, share %, and share amount

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/trips` | List all saved trips |
| POST | `/api/trips` | Save a new trip |
| GET | `/api/trips/<id>` | Get a single trip with tourists |
| DELETE | `/api/trips/<id>` | Delete a trip |
