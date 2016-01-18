--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET search_path = public, pg_catalog;

SET default_with_oids = false;

--
-- Name: ban; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE ban (
    id text,
    nom_voie text,
    id_fantoir text,
    numero text,
    rep text,
    code_insee text,
    code_post text,
    alias text,
    nom_ld text,
    x double precision,
    y double precision,
    commune text,
    fant_voie text,
    fant_ld text,
    lat double precision,
    lon double precision,
    geom geometry
);


--
-- Name: maps; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE maps (
    id uuid DEFAULT uuid_generate_v4(),
    path text,
    address text,
    level text,
    building text,
    name text,
    geom geometry
);


--
-- Name: ban_nomap; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW ban_nomap AS
 SELECT NULL::uuid AS id,
    NULL::text AS path,
    a.id AS address,
    NULL::text AS level,
    NULL::text AS building,
    NULL::text AS name,
    a.geom,
    (((((((a.numero || a.rep) || ' '::text) || a.nom_voie) || ', '::text) || a.code_post) || ' '::text) || a.commune) AS address_label
   FROM (ban a
     LEFT JOIN maps m ON ((a.id = m.address)))
  WHERE (m.id IS NULL);


--
-- Name: log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE log (
    "time" timestamp without time zone DEFAULT now(),
    loc geometry,
    ip inet,
    map uuid
);


--
-- Name: map_info; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW map_info AS
 SELECT m.id,
    m.path,
    m.address,
    m.level,
    m.building,
    m.name,
    m.geom,
    (((((((a.numero || a.rep) || ' '::text) || a.nom_voie) || ', '::text) || a.code_post) || ' '::text) || a.commune) AS address_label
   FROM (maps m
     JOIN ban a ON ((a.id = m.address)));


--
-- Name: ban_geom; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ban_geom ON ban USING gist (geom);


--
-- Name: ban_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ban_id ON ban USING btree (id);


--
-- Name: maps_geom; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX maps_geom ON maps USING gist (geom);


--
-- Name: maps_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX maps_id ON maps USING btree (id);


--
-- PostgreSQL database dump complete
--

