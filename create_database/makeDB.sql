CREATE TABLE UserData (
    User_ID SERIAL PRIMARY KEY,
    Username VARCHAR(255),
    Pass VARCHAR(255),
    Langg VARCHAR(255),
    Age INT,
    Email_ID VARCHAR(255)
);

CREATE TABLE GPC (
    GPC_ID SERIAL PRIMARY KEY,
    GPC_Name VARCHAR(255),
    Email_ID VARCHAR(255) 
);

CREATE TABLE Game (
    Game_ID SERIAL PRIMARY KEY,
    Game_Name VARCHAR(255),
    Price DECIMAL(10, 2),
    GPC_ID SERIAL,
    Game_Release_Date DATE,
    Age_Limit INT,
    FOREIGN KEY (GPC_ID) REFERENCES GPC(GPC_ID)
);

CREATE TABLE Region (
    RegionID SERIAL PRIMARY KEY,
    Region_Name VARCHAR(255)
);

CREATE TABLE User_Region (
    RegionID SERIAL,
    User_Name VARCHAR(255),
    FOREIGN KEY (RegionID) REFERENCES Region(RegionID),
    PRIMARY KEY (RegionID, User_Name)
);

CREATE TABLE Game_Region (
    RegionID SERIAL,
    Game_Name VARCHAR(255),
    FOREIGN KEY (RegionID) REFERENCES Region(RegionID),
    PRIMARY KEY (RegionID, Game_Name)
);

CREATE TABLE Review (
    User_ID SERIAL,
    Game_ID SERIAL,
    Posted_Time TIMESTAMP,
    Content VARCHAR(100),
    FOREIGN KEY (User_ID) REFERENCES UserData(User_ID),
    FOREIGN KEY (Game_ID) REFERENCES Game(Game_ID),
    PRIMARY KEY (User_ID, Game_ID)
);

CREATE TABLE Genre (
    Genre_ID SERIAL PRIMARY KEY,
    Genre_Name VARCHAR(50)
);

CREATE TABLE Game_Genre (
    Genre_ID SERIAL,
    Game_ID SERIAL,
    FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID),
    FOREIGN KEY (Game_ID) REFERENCES Game(Game_ID),
    PRIMARY KEY (Genre_ID, Game_ID)
);

CREATE TABLE Lang (
    Lang_ID SERIAL PRIMARY KEY,
    Lang_Name VARCHAR(50)
);

CREATE TABLE Game_Lang (
    Lang_ID SERIAL,
    Game_ID SERIAL,
    FOREIGN KEY (Lang_ID) REFERENCES Lang(Lang_ID),
    FOREIGN KEY (Game_ID) REFERENCES Game(Game_ID),
    PRIMARY KEY (Lang_ID, Game_ID)
);

-- -- Create a function to add a genre to the Genre table if it doesn't already exist
-- CREATE OR REPLACE FUNCTION add_genre_on_game_insert()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     -- Check if the genre already exists in the Genre table
--     INSERT INTO Genre (Genre_Name)
--     VALUES (NEW.Genre_Name)
--     ON CONFLICT (Genre_Name) DO NOTHING;

--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- -- Create a trigger to call the add_genre_on_game_insert() function
-- CREATE TRIGGER before_game_insert
-- BEFORE INSERT ON Game
-- FOR EACH ROW
-- EXECUTE FUNCTION add_genre_on_game_insert();


-- -- Create a function to add a GPC to the GPC table if it doesn't already exist
-- CREATE OR REPLACE FUNCTION add_gpc_on_game_insert()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     -- Check if the GPC already exists in the GPC table
--     INSERT INTO GPC (GPC_Name, Email_ID)
--     VALUES (NEW.GPC_Name, NEW.Email_ID) --Check for email ID case with Sarvo
--     ON CONFLICT (GPC_Name) DO NOTHING;

--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- -- Create a trigger to call the add_gpc_on_game_insert() function
-- CREATE TRIGGER before_game_insert_gpc
-- BEFORE INSERT ON Game
-- FOR EACH ROW
-- EXECUTE FUNCTION add_gpc_on_game_insert();

-- COPY GPC FROM '../init_data/gpc.txt' DELIMITER ',' CSV;
-- COPY Game FROM '../init_data/game.txt' DELIMITER ',' CSV;
-- COPY Region FROM '../init_data/region.txt' DELIMITER ',' CSV;
-- COPY Genre FROM '../init_data/genre.txt' DELIMITER ',' CSV;
-- COPY Lang FROM '../init_data/language.txt' DELIMITER ',' CSV;
