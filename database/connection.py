from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/war.db", echo=False)

def get_engine():
    return engine
