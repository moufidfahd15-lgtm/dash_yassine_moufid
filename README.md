# War & Conflict Analysis Dashboard

Small Streamlit dashboard analyzing conflicts and casualties from CSV data.

## Requirements
- Python 3.8+
- Install dependencies:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Initialize database
Populate the local SQLite database from the CSV files:

```
python run.py
```

This writes `data/war.db` from the `data/*.csv` files.

## Run the app
Start the Streamlit app:

```
streamlit run app.py
```

## Notes
- Data files live in the `data/` directory.
- The app uses `streamlit`, `pandas`, `sqlalchemy`, and `plotly`.

If you want, I can also create a small Git commit for these changes.
