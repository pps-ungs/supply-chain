--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: escenario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.escenario (
    id integer NOT NULL,
    nombre text,
    data text
);


ALTER TABLE public.escenario OWNER TO postgres;

--
-- Name: escenario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.escenario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.escenario_id_seq OWNER TO postgres;

--
-- Name: escenario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.escenario_id_seq OWNED BY public.escenario.id;


--
-- Name: usuarie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarie (
    id integer NOT NULL,
    nombre text,
    apellido text
);


ALTER TABLE public.usuarie OWNER TO postgres;

--
-- Name: usuarie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarie_id_seq OWNER TO postgres;

--
-- Name: usuarie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarie_id_seq OWNED BY public.usuarie.id;


--
-- Name: escenario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.escenario ALTER COLUMN id SET DEFAULT nextval('public.escenario_id_seq'::regclass);


--
-- Name: usuarie id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarie ALTER COLUMN id SET DEFAULT nextval('public.usuarie_id_seq'::regclass);


--
-- Data for Name: escenario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.escenario (id, nombre, data) FROM stdin;
\.


--
-- Data for Name: usuarie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarie (id, nombre, apellido) FROM stdin;
626	'Diego'	'Maradona'
\.


--
-- Name: escenario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.escenario_id_seq', 1, false);


--
-- Name: usuarie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarie_id_seq', 1, false);


--
-- Name: escenario escenario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.escenario
    ADD CONSTRAINT escenario_pkey PRIMARY KEY (id);


--
-- Name: usuarie usuarie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarie
    ADD CONSTRAINT usuarie_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

