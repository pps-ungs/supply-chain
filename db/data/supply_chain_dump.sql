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


ALTER SEQUENCE public.centro_de_distribucion_id_seq OWNER TO postgres;

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


ALTER SEQUENCE public.centro_de_fabricacion_id_seq OWNER TO postgres;

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
    data jsonb
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


ALTER SEQUENCE public.punto_de_venta_id_seq OWNER TO postgres;

--
-- Name: punto_de_venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.punto_de_venta_id_seq OWNED BY public.punto_de_venta.id;


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
1	e_0	{"p_0": 11.685208901236928, "p_1": 87.91097612864822, "p_2": 72.05044127917776, "p_3": 88.46948833579854, "p_4": 99.96406948178853, "p_5": 18.779520968329248, "p_6": 45.98042516731735, "p_7": 22.576787339962962, "p_8": 76.56945337679392, "p_9": 63.99579614154163}
2	e_1	{"p_0": 57.19649105288111, "p_1": 72.45471938985192, "p_2": 82.4916923387757, "p_3": 92.74840330953215, "p_4": 49.82817073735708, "p_5": 3.590916971922963, "p_6": 71.89273307416684, "p_7": 20.794087575384015, "p_8": 52.577661663322296, "p_9": 69.49969733140469}
3	e_2	{"p_0": 26.34836154636276, "p_1": 97.86418378329941, "p_2": 3.0246985554450783, "p_3": 16.373875772965278, "p_4": 8.719781979487571, "p_5": 15.290526693669003, "p_6": 13.606972859318214, "p_7": 47.85623687389053, "p_8": 53.015447996223294, "p_9": 97.57641825010639}
4	e_3	{"p_0": 4.020072658174159, "p_1": 29.121713229708522, "p_2": 10.603469553125628, "p_3": 55.25951788094882, "p_4": 36.88963974153672, "p_5": 85.33159499077847, "p_6": 89.65274685113611, "p_7": 14.69855508644184, "p_8": 68.210043737754, "p_9": 12.235901854512518}
5	e_4	{"p_0": 54.85275287285126, "p_1": 51.249547808869075, "p_2": 96.21427846041469, "p_3": 6.720809982892698, "p_4": 12.920514457443126, "p_5": 87.3056667722875, "p_6": 70.92835060102998, "p_7": 14.525076167926846, "p_8": 94.83849947877577, "p_9": 53.681823598673596}
6	e_5	{"p_0": 42.26630356280117, "p_1": 28.460352434082964, "p_2": 62.248131691377104, "p_3": 17.129327068342814, "p_4": 49.10740449496739, "p_5": 6.998780795626509, "p_6": 78.77087850503236, "p_7": 37.748438883822004, "p_8": 5.9878457186394645, "p_9": 96.97099045760285}
7	e_6	{"p_0": 47.03297585652103, "p_1": 25.60859752930668, "p_2": 37.19107090472335, "p_3": 72.95585728724764, "p_4": 53.247989040900386, "p_5": 66.71191347250536, "p_6": 48.62333840210495, "p_7": 42.56240377612156, "p_8": 14.385574049812382, "p_9": 74.75507759744075}
8	e_7	{"p_0": 36.229409166666606, "p_1": 19.14122448757921, "p_2": 36.779684045119055, "p_3": 82.24799380075025, "p_4": 18.86351482219592, "p_5": 5.798316656413306, "p_6": 13.471920176766554, "p_7": 72.37700843276956, "p_8": 21.909052377348424, "p_9": 69.77553448360783}
9	e_8	{"p_0": 56.14244284430698, "p_1": 19.23994714147006, "p_2": 84.3212278610222, "p_3": 53.44231433619944, "p_4": 56.417050200656895, "p_5": 85.21619025766266, "p_6": 65.64072799973195, "p_7": 17.917032911328224, "p_8": 55.072723824297505, "p_9": 82.47031737029185}
10	e_9	{"p_0": 89.94761160844268, "p_1": 60.536258139023175, "p_2": 74.68778792722358, "p_3": 64.05478153343388, "p_4": 62.88377059539734, "p_5": 4.2971366631746, "p_6": 54.761009812120236, "p_7": 24.107780608922546, "p_8": 85.68979903020983, "p_9": 6.959593044423634}
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

SELECT pg_catalog.setval('public.escenario_id_seq', 10, true);


--
-- Name: punto_de_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.punto_de_venta_id_seq', 10, true);


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
-- PostgreSQL database dump complete
--

