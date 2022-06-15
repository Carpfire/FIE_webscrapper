DROP TABLE IF EXISTS fencers;
DROP TABLE IF EXISTS winners;
DROP TABLE IF EXISTS losers;
DROP TABLE IF EXISTS fencer;
DROP TABLE IF EXISTS bouts;
DROP TABLE IF EXISTS bouts;
DROP TABLE IF EXISTS tournaments_to_bouts;
DROP TABLE IF EXISTS tournaments;



CREATE TABLE fencers(
    id INTEGER PRIMARY KEY  AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL, 
    country TEXT NOT NULL
);


CREATE TABLE winners(
    id INTEGER PRIMARY KEY  AUTOINCREMENT,
    bout_id INTEGER NOT NULL,
    fencer_id INTEGER NOT NULL,
    FOREIGN KEY (bout_id) REFERENCES bout (id),
    FOREIGN KEY (fencer_id) REFERENCES fencer (id)
);

CREATE TABLE losers(
    id INTEGER PRIMARY KEY  AUTOINCREMENT,
    bout_id INTEGER NOT NULL,
    fencer_id INTEGER NOT NULL,
    FOREIGN KEY (bout_id) REFERENCES bout (id),
    FOREIGN KEY (fencer_id) REFERENCES fencer (id)
);

CREATE TABLE bouts(
    id TEXT PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    win_score INTEGER NOT NULL,
    lose_score INTEGER NOT NULL,
    round TEXT NOT NULL
);

CREATE TABLE tournaments_to_bouts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bout_id INTEGER NOT NULL,
    tournament_id INTEGER NOT NULL,
    FOREIGN KEY (bout_id) REFERENCES bout (id),
    FOREIGN KEY (tournament_id) REFERENCES tornament (id)
);

CREATE TABLE tournaments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL, 
    city TEXT NOT NULL, 
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL

);

