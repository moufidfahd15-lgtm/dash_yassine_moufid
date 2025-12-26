import pandas as pd
from .connection import get_engine

def load_conflicts():
    return pd.read_sql("SELECT * FROM conflicts", get_engine())

def load_casualties(conflict_id, year_range):
    query = f"""
    SELECT *
    FROM casualties
    WHERE conflict_id = {conflict_id}
    AND year BETWEEN {year_range[0]} AND {year_range[1]}
    """
    return pd.read_sql(query, get_engine())

def kpi_metrics():
    engine = get_engine()
    return {
        "total_conflicts": pd.read_sql(
            "SELECT COUNT(*) c FROM conflicts", engine).iloc[0]["c"],
        "active_conflicts": pd.read_sql(
            "SELECT COUNT(*) c FROM conflicts WHERE status='Active'", engine).iloc[0]["c"],
        "civilian_deaths": pd.read_sql(
            "SELECT SUM(civilian_deaths) s FROM casualties", engine).iloc[0]["s"],
        "military_deaths": pd.read_sql(
            "SELECT SUM(military_deaths) s FROM casualties", engine).iloc[0]["s"]
    }

def countries_conflict_count():
    query = """
    SELECT 
        c.name,
        c.continent,
        c.latitude,
        c.longitude,
        COUNT(cp.conflict_id) AS conflicts_count
    FROM countries c
    JOIN conflict_participants cp ON c.id = cp.country_id
    GROUP BY c.id
    """
    return pd.read_sql(query, get_engine())

def conflict_timeline():
    query = """
    SELECT 
        name,
        start_year,
        COALESCE(end_year, 2025) AS end_year,
        status,
        region
    FROM conflicts
    """
    df = pd.read_sql(query, get_engine())
    # convert numeric years to datetimes for proper timeline/Gantt plotting
    df["start"] = pd.to_datetime(df["start_year"].astype(int).astype(str) + "-01-01")
    # end_year may be float if NULLs existed; coerce to int then to year-end date
    df["end"] = pd.to_datetime(df["end_year"].fillna(2025).astype(int).astype(str) + "-12-31")
    return df

def casualties_heatmap():
    query = """
    SELECT 
        year,
        conflict_id,
        civilian_deaths + military_deaths AS total_deaths
    FROM casualties
    """
    return pd.read_sql(query, get_engine())
