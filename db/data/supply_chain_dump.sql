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
1	e_0	{"p_0": 37.562923912428104, "p_1": 16.44887666443045, "p_2": 57.89875371359547, "p_3": 10.634215990575502, "p_4": 65.33591760296683, "p_5": 72.99629305905654, "p_6": 1.7844133325014677, "p_7": 53.581683649687434, "p_8": 59.119273676749515, "p_9": 29.588993805743932}
2	e_1	{"p_0": 89.22415158665964, "p_1": 32.0623199184253, "p_2": 3.1356605782821974, "p_3": 70.49993442021376, "p_4": 82.99663943218361, "p_5": 51.33210885207995, "p_6": 97.06132007984797, "p_7": 69.89958194367381, "p_8": 68.65822574292143, "p_9": 27.77730628244255}
3	e_2	{"p_0": 56.090127463199636, "p_1": 38.14032877927303, "p_2": 85.86858026594469, "p_3": 61.420219961917525, "p_4": 43.25195142026833, "p_5": 69.0733122620419, "p_6": 57.24519242418489, "p_7": 40.545520496041625, "p_8": 77.59798128377808, "p_9": 88.7691723730234}
4	e_3	{"p_0": 94.03872951191934, "p_1": 81.57440008412001, "p_2": 35.35077661819054, "p_3": 46.04927386000793, "p_4": 1.5948225303125994, "p_5": 17.111790497396743, "p_6": 14.023161352783498, "p_7": 44.5797983985483, "p_8": 74.81702570851206, "p_9": 13.826680208125943}
5	e_4	{"p_0": 62.26493910889623, "p_1": 67.87042312826519, "p_2": 62.26782115549901, "p_3": 84.31100653780089, "p_4": 30.675844646851022, "p_5": 57.48145330877862, "p_6": 13.82221534738015, "p_7": 27.52858591166277, "p_8": 99.914013018829, "p_9": 1.0908953987501238}
6	e_5	{"p_0": 44.40104868335265, "p_1": 37.18227847140677, "p_2": 60.49761520795799, "p_3": 90.30973847043742, "p_4": 79.09891056564919, "p_5": 4.422549274646722, "p_6": 48.75515066913369, "p_7": 60.71038374701634, "p_8": 70.8878393349242, "p_9": 87.3599072445952}
7	e_6	{"p_0": 89.52922102018141, "p_1": 41.108664884641115, "p_2": 77.16546552354679, "p_3": 3.093389455638673, "p_4": 44.05339897475948, "p_5": 5.70623516424002, "p_6": 78.72160216634043, "p_7": 55.57302656088303, "p_8": 10.232055566892566, "p_9": 7.3870164838201315}
8	e_7	{"p_0": 31.29711162009829, "p_1": 92.96298253929483, "p_2": 14.125364437383842, "p_3": 63.23060468286924, "p_4": 80.3373049738721, "p_5": 23.914343016197872, "p_6": 84.5685861014823, "p_7": 31.487957011201274, "p_8": 69.42366059495872, "p_9": 51.389404849634055}
9	e_8	{"p_0": 12.232296300678053, "p_1": 13.539665095745956, "p_2": 2.3692897954525827, "p_3": 45.4712299257429, "p_4": 3.617860556613268, "p_5": 89.40091994819593, "p_6": 12.445328548570929, "p_7": 12.276893050411916, "p_8": 78.2389980339984, "p_9": 57.86405711878847}
10	e_9	{"p_0": 82.54245348899013, "p_1": 94.65192969981644, "p_2": 55.905948081757685, "p_3": 73.00283666964717, "p_4": 70.2897094038456, "p_5": 38.95724063774679, "p_6": 70.12766172615427, "p_7": 23.277597174207187, "p_8": 45.94751727290584, "p_9": 42.5428768004506}
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

SELECT pg_catalog.setval('public.escenario_id_seq', 10, true);


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

