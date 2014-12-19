DROP DATABASE IF EXISTS vivcontrol;

CREATE DATABASE vivcontrol ENCODING = 'UTF8';

\c vivcontrol;

CREATE TABLE config (
    id integer NOT NULL,
    name text,
    active boolean,
    sensorpin1 integer,
    sensorpin2 integer,
    lightpin integer,
    heatpin integer,
    humpin integer,
    daytemp integer,
    nighttemp integer,
    minhum integer,
    lightcontrol integer,
    heatcontrol integer,
    humcontrol integer,
    daystart integer,
    dayend integer,
    checkinterval integer
);

CREATE SEQUENCE config_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE config_id_seq OWNED BY config.id;

ALTER TABLE ONLY config ALTER COLUMN id SET DEFAULT nextval('config_id_seq'::regclass);

ALTER TABLE ONLY config
    ADD CONSTRAINT id PRIMARY KEY (id);

CREATE TABLE log (
    logtime integer NOT NULL,
    config integer,
    heating boolean,
    light boolean,
    hum boolean,
    temp1 double precision,
    temp2 double precision,
    hum1 double precision,
    hum2 double precision
);

ALTER TABLE ONLY log
    ADD CONSTRAINT logtime PRIMARY KEY (logtime);

ALTER TABLE ONLY log
    ADD CONSTRAINT config FOREIGN KEY (config) REFERENCES config(id);
