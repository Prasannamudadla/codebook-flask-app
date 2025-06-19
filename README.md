# Codebook Flask App

This is a simple Flask web application that uses an SQLite database to store codebook entries (DSA problems).

## How to Run

1. Create and activate a virtual environment:

`python -m venv venv`
`venv\Scripts\activate`   # For Windows


2. Install dependencies:
`pip install -r requirements.txt`

3. Run the app:
`python app.py`
Then open your browser at: `http://127.0.0.1:5000/`

## Notes
- db/ and contacts.txt are ignored using .gitignore
- All required packages are listed in requirements.txt
- Make sure to initialize the database by running init_db.py once before first use.

