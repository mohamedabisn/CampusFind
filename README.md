# CampusFind – Jamal Mohamed College

A Flask + SQLite campus lost-and-found platform based on the supplied UI reference.

## Features
- Login / create account before entering the app
- Unique CampusFind User ID (example: CF-A1B2C3)
- Dynamic name, email, department and year in the header
- Edit profile
- Report Lost / Found item in a modal
- Image upload
- Search
- All / Lost / Found filters
- Category, department, color and location filters
- Random item order from the API, with client-side sorting
- Details modal
- Call / WhatsApp contact
- Favorite/save items
- Notifications for possible category matches
- SQLite persistence
- No admin role
- No "Mark Returned" feature

## Setup

Python 3.10+ recommended.

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

The database is created automatically as `campusfind.db`.
