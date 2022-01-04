DROP DATABASE projet;
CREATE DATABASE projet;
\c projet
DROP TABLE vehicle;
CREATE TABLE vehicle (
    route_I NUMERIC PRIMARY KEY,
    route_name TEXT,
    route_TYPE NUMERIC
);
DROP TABLE ITINERARY;
DROP TABLE STOPS;
CREATE TABLE stops (
    stop_I NUMERIC PRIMARY KEY,
    name TEXT,
    geo_point_2d VARCHAR(50)
);

CREATE TABLE itinerary (
    route_I NUMERIC,
    route_type NUMERIC,
    duration NUMERIC,
    d NUMERIC,
    from_stop_I NUMERIC REFERENCES stops(stop_I),
    to_stop_I NUMERIC REFERENCES stops(stop_I)
);

DROP TABLE p_history;
DROP TABLE p_users;
CREATE TABLE p_users (
    id SERIAL PRIMARY KEY,
    username TEXT
);

CREATE TABLE p_history (
	id SERIAL REFERENCES p_users(id),
	element TEXT,
	PRIMARY KEY (id, element)
);


INSERT INTO p_users(username) values ('anonymous');

/* ----------------------------------------- */
