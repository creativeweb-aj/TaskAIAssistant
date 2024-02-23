-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.1.0-alpha1
-- PostgreSQL version: 16.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
CREATE DATABASE task_management_db;
-- ddl-end --


-- object: public.seq_user | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.seq_user CASCADE;
CREATE SEQUENCE public.seq_user
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.seq_user OWNER TO postgres;
-- ddl-end --

-- object: public.seq_customer | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.seq_customer CASCADE;
CREATE SEQUENCE public.seq_customer
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.seq_customer OWNER TO postgres;
-- ddl-end --

-- object: public."user" | type: TABLE --
-- DROP TABLE IF EXISTS public."user" CASCADE;
CREATE TABLE public."user" (
	id_user smallint NOT NULL DEFAULT nextval('public.seq_user'::regclass),
	name varchar(100),
	surname varchar(100),
	username varchar(100),
	password varchar(100),
	mail varchar(100),
	github_user varchar(100),
	date_add timestamp DEFAULT now(),
	CONSTRAINT user_pk PRIMARY KEY (id_user)
);
-- ddl-end --
ALTER TABLE public."user" OWNER TO postgres;
-- ddl-end --

-- object: public.customers | type: TABLE --
-- DROP TABLE IF EXISTS public.customers CASCADE;
CREATE TABLE public.customers (
	id_customer smallint NOT NULL DEFAULT nextval('public.seq_customer'::regclass),
	company_name varchar(100),
	date_add timestamp DEFAULT now(),
	CONSTRAINT customers_pk PRIMARY KEY (id_customer)
);
-- ddl-end --
ALTER TABLE public.customers OWNER TO postgres;
-- ddl-end --

-- object: public.seq_project | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.seq_project CASCADE;
CREATE SEQUENCE public.seq_project
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.seq_project OWNER TO postgres;
-- ddl-end --

-- object: public.seq_activity | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.seq_activity CASCADE;
CREATE SEQUENCE public.seq_activity
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.seq_activity OWNER TO postgres;
-- ddl-end --

-- object: public.project | type: TABLE --
-- DROP TABLE IF EXISTS public.project CASCADE;
CREATE TABLE public.project (
	id_project smallint NOT NULL DEFAULT nextval('public.seq_project'::regclass),
	id_customer smallint,
	project_name varchar(255),
	date_add timestamp DEFAULT now(),
	CONSTRAINT project_pk PRIMARY KEY (id_project)
);
-- ddl-end --
ALTER TABLE public.project OWNER TO postgres;
-- ddl-end --

-- object: public.activities | type: TABLE --
-- DROP TABLE IF EXISTS public.activities CASCADE;
CREATE TABLE public.activities (
	id_activity bigint NOT NULL DEFAULT nextval('public.seq_activity'::regclass),
	id_user smallint,
	id_project smallint,
	activity_name varchar(100),
	description text,
	hours smallint,
	CONSTRAINT activities_pk PRIMARY KEY (id_activity)
);
-- ddl-end --
ALTER TABLE public.activities OWNER TO postgres;
-- ddl-end --

-- object: user_fk | type: CONSTRAINT --
-- ALTER TABLE public.activities DROP CONSTRAINT IF EXISTS user_fk CASCADE;
ALTER TABLE public.activities ADD CONSTRAINT user_fk FOREIGN KEY (id_user)
REFERENCES public."user" (id_user) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: project_fk | type: CONSTRAINT --
-- ALTER TABLE public.activities DROP CONSTRAINT IF EXISTS project_fk CASCADE;
ALTER TABLE public.activities ADD CONSTRAINT project_fk FOREIGN KEY (id_project)
REFERENCES public.project (id_project) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: customers_fk | type: CONSTRAINT --
-- ALTER TABLE public.project DROP CONSTRAINT IF EXISTS customers_fk CASCADE;
ALTER TABLE public.project ADD CONSTRAINT customers_fk FOREIGN KEY (id_customer)
REFERENCES public.customers (id_customer) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --


