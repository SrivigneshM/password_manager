CREATE TABLE IF NOT EXISTS actor(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   password TEXT NOT NULL,
   salt TEXT NOT NULL,
   name TEXT NOT NULL,
   email TEXT NOT NULL,
   mobile TEXT
);

CREATE TABLE IF NOT EXISTS profile(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   actor_id INTEGER,
   app_name TEXT,
   user_id TEXT NOT NULL,
   user_name TEXT,
   password TEXT NOT NULL,
   password_expiry DATE,
   crn TEXT,
   profile_password TEXT,
   url TEXT,
   is_active BOOLEAN NOT NULL,
   customer_care_number TEXT,
   remarks VARCHAR(255),
   FOREIGN KEY(actor_id) REFERENCES actor(id)
);

CREATE TABLE IF NOT EXISTS card(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   profile_id INTEGER,
   actor_id INTEGER,
   number TEXT NOT NULL,
   name TEXT,
   type TEXT NOT NULL,
   category TEXT,
   expiry DATE NOT NULL,
   pin INTEGER,
   cvv INTEGER,
   issuer TEXT,
   is_active BOOLEAN NOT NULL,
   FOREIGN KEY(profile_id) REFERENCES profile(id),
   FOREIGN KEY(actor_id) REFERENCES actor(id)
);
