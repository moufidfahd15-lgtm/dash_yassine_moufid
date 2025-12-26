CREATE TABLE conflicts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    start_year INTEGER NOT NULL,
    end_year INTEGER,
    status TEXT CHECK(status IN ('Active','Ended')),
    conflict_type TEXT,
    region TEXT
);

CREATE TABLE countries (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    continent TEXT,
    latitude REAL,
    longitude REAL
);

CREATE TABLE conflict_participants (
    conflict_id INTEGER,
    country_id INTEGER,
    role TEXT,
    PRIMARY KEY (conflict_id, country_id)
);

CREATE TABLE casualties (
    conflict_id INTEGER,
    year INTEGER,
    civilian_deaths INTEGER,
    military_deaths INTEGER,
    PRIMARY KEY (conflict_id, year)
);
