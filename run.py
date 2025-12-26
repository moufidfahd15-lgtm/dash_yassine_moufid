import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/war.db")

pd.read_csv("data/conflicts.csv").to_sql("conflicts", engine, if_exists="replace", index=False)
pd.read_csv("data/countries.csv").to_sql("countries", engine, if_exists="replace", index=False)
pd.read_csv("data/conflict_participants.csv").to_sql("conflict_participants", engine, if_exists="replace", index=False)
pd.read_csv("data/casualties.csv").to_sql("casualties", engine, if_exists="replace", index=False)
