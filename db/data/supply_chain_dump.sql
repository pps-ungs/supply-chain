--
-- PostgreSQL database dump
--

-- Dumped from database version 14.17 (Homebrew)
-- Dumped by pg_dump version 14.17 (Homebrew)

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
-- Name: centro_de_distribucion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.centro_de_distribucion (
    id integer NOT NULL,
    nombre text,
    data text
);


ALTER TABLE public.centro_de_distribucion OWNER TO postgres;

--
-- Name: centro_de_distribucion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.centro_de_distribucion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.centro_de_distribucion_id_seq OWNER TO postgres;

--
-- Name: centro_de_distribucion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.centro_de_distribucion_id_seq OWNED BY public.centro_de_distribucion.id;


--
-- Name: centro_de_fabricacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.centro_de_fabricacion (
    id integer NOT NULL,
    nombre text,
    data text
);


ALTER TABLE public.centro_de_fabricacion OWNER TO postgres;

--
-- Name: centro_de_fabricacion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.centro_de_fabricacion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.centro_de_fabricacion_id_seq OWNER TO postgres;

--
-- Name: centro_de_fabricacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.centro_de_fabricacion_id_seq OWNED BY public.centro_de_fabricacion.id;


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


ALTER TABLE public.escenario_id_seq OWNER TO postgres;

--
-- Name: escenario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.escenario_id_seq OWNED BY public.escenario.id;


--
-- Name: punto_de_venta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.punto_de_venta (
    id integer NOT NULL,
    nombre text,
    data text
);


ALTER TABLE public.punto_de_venta OWNER TO postgres;

--
-- Name: punto_de_venta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.punto_de_venta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.punto_de_venta_id_seq OWNER TO postgres;

--
-- Name: punto_de_venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.punto_de_venta_id_seq OWNED BY public.punto_de_venta.id;


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


ALTER TABLE public.usuarie_id_seq OWNER TO postgres;

--
-- Name: usuarie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarie_id_seq OWNED BY public.usuarie.id;


--
-- Name: centro_de_distribucion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centro_de_distribucion ALTER COLUMN id SET DEFAULT nextval('public.centro_de_distribucion_id_seq'::regclass);


--
-- Name: centro_de_fabricacion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centro_de_fabricacion ALTER COLUMN id SET DEFAULT nextval('public.centro_de_fabricacion_id_seq'::regclass);


--
-- Name: escenario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.escenario ALTER COLUMN id SET DEFAULT nextval('public.escenario_id_seq'::regclass);


--
-- Name: punto_de_venta id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.punto_de_venta ALTER COLUMN id SET DEFAULT nextval('public.punto_de_venta_id_seq'::regclass);


--
-- Name: usuarie id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarie ALTER COLUMN id SET DEFAULT nextval('public.usuarie_id_seq'::regclass);


--
-- Data for Name: centro_de_distribucion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.centro_de_distribucion (id, nombre, data) FROM stdin;
1	s_0	
2	s_1	
3	s_2	
4	s_3	
5	s_4	
6	s_5	
7	s_6	
8	s_7	
9	s_8	
10	s_9	
\.


--
-- Data for Name: centro_de_fabricacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.centro_de_fabricacion (id, nombre, data) FROM stdin;
1	f_0	
2	f_1	
3	f_2	
4	f_3	
5	f_4	
6	f_5	
7	f_6	
8	f_7	
9	f_8	
10	f_9	
\.


--
-- Data for Name: escenario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.escenario (id, nombre, data) FROM stdin;
\.


--
-- Data for Name: punto_de_venta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.punto_de_venta (id, nombre, data) FROM stdin;
1	p_0	
2	p_1	
3	p_2	
4	p_3	
5	p_4	
6	p_5	
7	p_6	
8	p_7	
9	p_8	
10	p_9	
\.


--
-- Data for Name: usuarie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarie (id, nombre, apellido) FROM stdin;
626	'Diego'	'Maradona'
\.


--
-- Name: centro_de_distribucion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.centro_de_distribucion_id_seq', 10, true);


--
-- Name: centro_de_fabricacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.centro_de_fabricacion_id_seq', 10, true);


--
-- Name: escenario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.escenario_id_seq', 1, false);


--
-- Name: punto_de_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.punto_de_venta_id_seq', 10, true);


--
-- Name: usuarie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarie_id_seq', 1, false);


--
-- Name: centro_de_distribucion centro_de_distribucion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centro_de_distribucion
    ADD CONSTRAINT centro_de_distribucion_pkey PRIMARY KEY (id);


--
-- Name: centro_de_fabricacion centro_de_fabricacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centro_de_fabricacion
    ADD CONSTRAINT centro_de_fabricacion_pkey PRIMARY KEY (id);


--
-- Name: escenario escenario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.escenario
    ADD CONSTRAINT escenario_pkey PRIMARY KEY (id);


--
-- Name: punto_de_venta punto_de_venta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.punto_de_venta
    ADD CONSTRAINT punto_de_venta_pkey PRIMARY KEY (id);


--
-- Name: usuarie usuarie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarie
    ADD CONSTRAINT usuarie_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

