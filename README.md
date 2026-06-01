# Bible Study Companion

This Web App is a Django FullStack App specifically for Reading The Bible in a year! Features wise it is pretty simple by design using a Django-first methodology. It allows you to select a translation of the bible to read, select a book, then a verse. This app also tracks your progress if you are logged in showing a percentage of what you've read as well as the ability to save verses to a selection!

---

## Tech Stack

**Django 5.2** — Chosen as the backend framework for its batteries-included approach: the ORM, admin interface, and class-based views let us move quickly without wiring up a lot of boilerplate.

**SQLite** — Used as the development database. It requires zero configuration and keeps everything in a single file, which is ideal while the data model is still taking shape. If this app ever scales to more usersss we could quickly change over to Postgres.

**NIV Bible JSON (jsdelivr CDN)** — Verse data is pulled from a free, publicly hosted JSON dataset via a custom Django management command (`load_bible`). This keeps the repo small and lets us re-import or swap translations without storing large data files in version control.

**Future - ESV Bible (ESV.org API)** — Verse data is pulled from a free, API from the ESV.org API maintained by the Crossway team. In the future we could 'fetch on demand' from this API and build in our own system to avoid rate limiting or over fetching.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git

### Setup

```bash
# Clone the repo
git clone https://github.com/your-username/bible-study-companion.git
cd bible-study-companion

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install django

# Apply migrations
python manage.py migrate

# Import the NIV Bible (~31,000 verses — takes about a minute)
python manage.py load_bible

# Start the development server
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000`.

### Optional: clear and re-import verses

```bash
python manage.py load_bible --clear
```

### Create an admin user

```bash
python manage.py createsuperuser
```

Admin panel: `http://127.0.0.1:8000/admin/`

---

## URL Structure

| URL | Description |
|-----|-------------|
| `/read/` | Browse all books |
| `/read/<book>/` | List chapters in a book |
| `/read/<book>/<chapter>/` | Read verses (10 per page, `?start=N` to paginate) |
| `/admin/` | Django admin |
