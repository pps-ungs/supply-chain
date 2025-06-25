CREATE TABLE public.experimento_hill_climbing (
    id integer NOT NULL,
    experimento text,
    x_inicial text,
    obj_inicial numeric(15,2),
    step numeric(15,2),
    cant_iteraciones integer,
    iteracion integer,
    x_optimo text,
    obj numeric(15,2),
    tiempo numeric(15,2),
    motivo_parada text,
    estrategia text,
    distribucion text
);

ALTER TABLE public.experimento_hill_climbing OWNER TO postgres;

CREATE SEQUENCE public.experimento_hill_climbing_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.experimento_hill_climbing_id_seq OWNER TO postgres;

ALTER SEQUENCE public.experimento_hill_climbing_id_seq OWNED BY public.experimento_hill_climbing.id;

CREATE TABLE public.experimento_random_restart (
    id integer NOT NULL,
    modelo text,
    experimento text,
    x_inicial text,
    obj_inicial numeric(15,2),
    step numeric(15,2),
    cant_iteraciones integer,
    iteracion integer,
    cant_iteraciones_sin_mejora_max integer,
    cant_iteraciones_sin_mejora integer,
    cant_reinicios_max integer,
    cant_reinicios integer,
    x_optimo text,
    obj numeric(15,2),
    tiempo numeric(15,2),
    motivo_parada text,
    estrategia text,
    distribucion text
);

ALTER TABLE public.experimento_random_restart OWNER TO postgres;

CREATE SEQUENCE public.experimento_random_restart_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.experimento_random_restart_id_seq OWNER TO postgres;

ALTER SEQUENCE public.experimento_random_restart_id_seq OWNED BY public.experimento_random_restart.id;

ALTER TABLE ONLY public.experimento_hill_climbing ALTER COLUMN id SET DEFAULT nextval('public.experimento_hill_climbing_id_seq'::regclass);

ALTER TABLE ONLY public.experimento_random_restart ALTER COLUMN id SET DEFAULT nextval('public.experimento_random_restart_id_seq'::regclass);

COPY public.experimento_hill_climbing (id, experimento, x_inicial, obj_inicial, step, cant_iteraciones, iteracion, x_optimo, obj, tiempo, motivo_parada, estrategia, distribucion) FROM stdin;
1	100_it_steps_based_on_900	[8430, 10537, 16860, 27397]	8401544.14	900.00	100	100	[330, 637, 660, 54397]	8503994.53	21.98	Maximum number of iterations	minimal_1_8430	normal
2	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	30.00	100	100	[5430, 10537, 16860, 27397]	8428104.19	14.83	Maximum number of iterations	minimal_1_8430	normal
3	100_it_900_step	[4089, 5111, 8178, 13289]	7646794.56	935.00	100	100	[349, 436, 698, 54429]	8504210.92	12.33	Maximum number of iterations	minimal_3*3_4089	normal
4	100_it_940_945_step	[8430, 8430, 8430, 8430]	7865580.14	940.00	100	100	[910, 910, 910, 53550]	8501521.93	12.43	Maximum number of iterations	most_probable_scenario	normal
5	100_it_steps_based_on_915	[8467, 10583, 16934, 27517]	8398967.62	936.00	100	100	[43, 287, 86, 55597]	8506604.08	25.69	Maximum number of iterations	minimal_2_8467	normal
6	100_it_steps_based_on_500	[1363, 1703, 2726, 4429]	3120307.78	530.00	100	100	[2953, 1703, 2726, 48419]	8490871.79	22.53	Maximum number of iterations	minimal_3_1363	normal
7	100_it_all_x	[1363, 1363, 1363, 1363]	1504268.24	16.00	100	100	[2963, 1363, 1363, 1363]	2050905.71	22.34	Maximum number of iterations	based_on_demand	normal
8	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	45.00	100	100	[3967, 10583, 16934, 27517]	8436724.38	14.93	Maximum number of iterations	minimal_2_8467	normal
9	100_it_all_x	[8475, 8458, 8470, 8472]	7875731.04	18.00	100	100	[8475, 8458, 8470, 10272]	7986671.33	23.10	Maximum number of iterations	hybrid_demand_probabilistic	normal
10	100_it_all_x	[8430, 8430, 8430, 8430]	7865580.14	16.00	100	100	[8430, 8430, 8430, 10030]	7966638.79	22.98	Maximum number of iterations	most_probable_scenario	normal
11	100_it_steps_based_on_915	[8467, 8468, 8469, 8470]	7875668.58	933.00	100	100	[70, 71, 72, 56053]	8506995.42	27.56	Maximum number of iterations	uniform	normal
12	1000_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	10.00	1000	1000	[0, 10537, 16520, 28627]	8451628.45	230.08	Maximum number of iterations	minimal_1_8430	normal
13	100_it_all_x	[8475, 8458, 8470, 8472]	7875731.04	10.00	100	100	[8475, 8458, 8470, 9472]	7939767.96	23.74	Maximum number of iterations	hybrid_demand_probabilistic	normal
14	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	930.00	100	100	[97, 97, 97, 55897]	8506828.77	27.69	Maximum number of iterations	weighted_by_scenario_prob	normal
15	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	20.00	100	100	[8467, 8467, 8467, 10467]	7997464.10	23.03	Maximum number of iterations	average_demand	normal
16	100_it_936_945_step	[8475, 8458, 8470, 8472]	7875731.04	936.00	100	100	[51, 34, 46, 56208]	8507157.97	12.44	Maximum number of iterations	hybrid_demand_probabilistic	normal
17	100_it_steps_based_on_500	[8467, 10583, 16934, 27517]	8398967.62	515.00	100	100	[227, 5433, 454, 49147]	8494878.10	47.88	Maximum number of iterations	minimal_2_8467	normal
18	100_it_900_step	[8475, 8458, 8470, 8472]	7875731.04	935.00	100	100	[60, 43, 55, 56157]	8507103.47	2982.87	Maximum number of iterations	hybrid_demand_probabilistic	normal
19	100_it_steps_based_on_915	[8430, 10537, 16860, 27397]	8401544.14	936.00	100	100	[6, 241, 12, 55477]	8506825.12	25.76	Maximum number of iterations	minimal_1_8430	normal
20	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	60.00	100	100	[8430, 8430, 8430, 14430]	8178739.21	192.90	Maximum number of iterations	most_probable_scenario	normal
21	100_it_steps_based_on_900	[8430, 10537, 16860, 27397]	8401544.14	930.00	100	100	[60, 307, 120, 55297]	8506359.92	20.77	Maximum number of iterations	minimal_1_8430	normal
22	100_it_900_step	[8477, 8472, 8473, 8476]	7877227.30	920.00	100	100	[197, 192, 193, 55396]	8506161.04	12.59	Maximum number of iterations	pseudorandom_5	normal
23	100_it_936_945_step	[8467, 10583, 16934, 27517]	8398967.62	945.00	100	100	[907, 188, 869, 53977]	8502935.83	12.14	Maximum number of iterations	minimal_2_8467	normal
24	100_it_steps_based_on_900	[1363, 1703, 2726, 4429]	3120307.78	930.00	100	100	[433, 773, 866, 53719]	8502941.26	19.94	Maximum number of iterations	minimal_3_1363	normal
25	100_it_steps_based_on_900	[8467, 8468, 8469, 8470]	7875668.58	975.00	100	100	[667, 668, 669, 54295]	8503099.36	19.18	Maximum number of iterations	uniform	normal
26	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	45.00	100	100	[8477, 8472, 8473, 12976]	8123189.21	15.11	Maximum number of iterations	pseudorandom_5	normal
27	100_it_steps_based_on_900	[8467, 10583, 16934, 27517]	8398967.62	930.00	100	100	[97, 353, 194, 55417]	8506123.24	18.89	Maximum number of iterations	minimal_2_8467	normal
28	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	115.00	100	100	[8467, 8467, 8467, 19967]	8345257.44	14.71	Maximum number of iterations	average_demand	normal
29	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	45.00	100	100	[8467, 8467, 8467, 12967]	8121910.69	2036.52	Maximum number of iterations	weighted_by_scenario_prob	normal
30	100_it_900_step	[8475, 8458, 8470, 8472]	7875731.04	940.00	100	100	[15, 938, 10, 55472]	8505584.63	1965.98	Maximum number of iterations	hybrid_demand_probabilistic	normal
31	100_it_steps_based_on_915	[2726, 3407, 5452, 8859]	6130430.30	927.00	100	100	[872, 626, 817, 54282]	8502261.34	25.74	Maximum number of iterations	minimal_3*2_2726	normal
32	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	12.00	100	100	[8467, 8467, 8467, 9667]	7951461.77	22.59	Maximum number of iterations	average_demand	normal
33	100_it_steps_based_on_500	[8475, 8458, 8470, 8472]	7875731.04	575.00	100	100	[425, 6733, 420, 48147]	8492483.78	24.01	Maximum number of iterations	hybrid_demand_probabilistic	normal
34	100_it_900_step	[9389, 8487, 7744, 8099]	7864039.05	920.00	100	100	[189, 207, 384, 55019]	8505670.02	12.78	Maximum number of iterations	cost_sensitive	normal
35	100_it_steps_based_on_500	[8430, 8430, 8430, 8430]	7865580.14	530.00	100	100	[480, 8430, 1010, 46060]	8487996.68	22.29	Maximum number of iterations	most_probable_scenario	normal
36	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	939.00	100	100	[16, 16, 16, 56356]	8507326.77	12.62	Maximum number of iterations	average_demand	normal
37	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	30.00	100	100	[5467, 10583, 16934, 27517]	8426342.64	14.82	Maximum number of iterations	minimal_2_8467	normal
38	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	960.00	100	100	[787, 787, 787, 53587]	8502271.89	26.81	Maximum number of iterations	weighted_by_scenario_prob	normal
39	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	500.00	100	100	[467, 8467, 2467, 44467]	8484768.30	23.19	Maximum number of iterations	average_demand	normal
40	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	30.00	100	100	[8475, 8458, 8470, 11472]	8050928.37	15.08	Maximum number of iterations	hybrid_demand_probabilistic	normal
41	100_it_all_x	[8477, 8472, 8473, 8476]	7877227.30	14.00	100	100	[8477, 8472, 8473, 9876]	7965021.76	28.65	Maximum number of iterations	pseudorandom_5	normal
42	100_it_steps_based_on_936	[8430, 8430, 8430, 8430]	7865580.14	938.00	100	100	[926, 926, 926, 53454]	8501418.80	20.24	Maximum number of iterations	most_probable_scenario	normal
43	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	30.00	100	100	[5430, 10537, 16860, 27397]	8428104.19	14.80	Maximum number of iterations	minimal_1_8430	normal
44	100_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	20.00	100	100	[6430, 10537, 16860, 27397]	8420234.06	23.46	Maximum number of iterations	minimal_1_8430	normal
45	100_it_steps_based_on_915	[8467, 10583, 16934, 27517]	8398967.62	930.00	100	100	[97, 353, 194, 55417]	8506123.24	24.94	Maximum number of iterations	minimal_2_8467	normal
46	100_it_all_x	[8467, 8468, 8469, 8470]	7875668.58	20.00	100	100	[8467, 8468, 8469, 10470]	7997789.37	23.09	Maximum number of iterations	uniform	normal
47	100_it_all_x	[8475, 8458, 8470, 8472]	7875731.04	20.00	100	100	[8475, 8458, 8470, 10472]	7997840.09	23.15	Maximum number of iterations	hybrid_demand_probabilistic	normal
48	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	45.00	100	100	[8467, 8468, 8469, 12970]	8122170.79	14.94	Maximum number of iterations	uniform	normal
49	100_it_steps_based_on_915	[9389, 8487, 7744, 8099]	7864039.05	921.00	100	100	[179, 198, 376, 55070]	8505741.33	27.76	Maximum number of iterations	cost_sensitive	normal
50	100_it_steps_based_on_915	[8430, 10537, 16860, 27397]	8401544.14	933.00	100	100	[33, 274, 66, 55387]	8506592.78	25.61	Maximum number of iterations	minimal_1_8430	normal
51	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	921.00	100	100	[178, 178, 178, 55438]	8506265.33	26.29	Maximum number of iterations	average_demand	normal
52	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	575.00	100	100	[417, 6742, 417, 48142]	8492487.56	22.27	Maximum number of iterations	weighted_by_scenario_prob	normal
53	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	545.00	100	100	[292, 8467, 292, 46617]	8489724.56	23.81	Maximum number of iterations	weighted_by_scenario_prob	normal
54	100_it_steps_based_on_500	[8430, 10537, 16860, 27397]	8401544.14	575.00	100	100	[380, 2487, 185, 52122]	8500609.88	67.03	Maximum number of iterations	minimal_1_8430	normal
55	1000_it_940_step	[8467, 8467, 8467, 8467]	7875273.42	940.00	1000	1000	[7, 7, 7, 56407]	8507377.71	96.85	Maximum number of iterations	weighted_by_scenario_prob	normal
56	1000_it_940_step	[8467, 10583, 16934, 27517]	8398967.62	940.00	1000	1000	[7, 243, 14, 55717]	8506922.35	95.58	Maximum number of iterations	minimal_2_8467	normal
57	100_it_900_step	[1363, 1703, 2726, 4429]	3120307.78	925.00	100	100	[438, 778, 876, 54379]	8502975.75	13.48	Maximum number of iterations	minimal_3_1363	normal
58	1000_it_940_step	[2726, 3407, 5452, 8859]	6130430.30	940.00	1000	1000	[846, 587, 752, 53979]	8502632.39	96.47	Maximum number of iterations	minimal_3*2_2726	normal
59	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	115.00	100	100	[35, 10537, 15710, 29352]	8453224.88	14.24	Maximum number of iterations	minimal_1_8430	normal
60	100_it_all_x	[1363, 1363, 1363, 1363]	1504268.24	18.00	100	100	[3163, 1363, 1363, 1363]	2119124.69	22.66	Maximum number of iterations	based_on_demand	normal
61	100_it_936_945_step	[9389, 8487, 7744, 8099]	7864039.05	939.00	100	100	[938, 36, 232, 55049]	8504566.23	12.48	Maximum number of iterations	cost_sensitive	normal
62	100_it_steps_based_on_900	[1363, 1703, 2726, 4429]	3120307.78	960.00	100	100	[403, 743, 806, 54349]	8503318.24	20.35	Maximum number of iterations	minimal_3_1363	normal
63	100_it_steps_based_on_900	[8477, 8472, 8473, 8476]	7877227.30	900.00	100	100	[377, 372, 373, 55276]	8504995.99	19.68	Maximum number of iterations	pseudorandom_5	normal
64	1000_it_940_step	[8467, 8467, 8467, 8467]	7875273.42	940.00	1000	1000	[7, 7, 7, 56407]	8507377.71	104.29	Maximum number of iterations	average_demand	normal
65	100_it_steps_based_on_500	[8430, 8430, 8430, 8430]	7865580.14	575.00	100	100	[380, 6705, 380, 48105]	8492590.96	22.01	Maximum number of iterations	most_probable_scenario	normal
66	100_it_900_step	[9389, 8487, 7744, 8099]	7864039.05	930.00	100	100	[89, 117, 304, 55529]	8506352.33	12.65	Maximum number of iterations	cost_sensitive	normal
67	100_it_steps_based_on_900	[8475, 8458, 8470, 8472]	7875731.04	960.00	100	100	[795, 778, 790, 53592]	8502265.17	19.29	Maximum number of iterations	hybrid_demand_probabilistic	normal
68	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	115.00	100	100	[8467, 8468, 8469, 19970]	8345377.74	15.30	Maximum number of iterations	uniform	normal
69	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	115.00	100	100	[8477, 8472, 8473, 19976]	8345838.63	15.26	Maximum number of iterations	pseudorandom_5	normal
70	100_it_steps_based_on_936	[8475, 8458, 8470, 8472]	7875731.04	937.00	100	100	[42, 25, 37, 56259]	8507211.57	19.86	Maximum number of iterations	hybrid_demand_probabilistic	normal
71	100_it_900_step	[8467, 10583, 16934, 27517]	8398967.62	920.00	100	100	[187, 463, 374, 55117]	8505314.41	11.51	Maximum number of iterations	minimal_2_8467	normal
72	100_it_steps_based_on_915	[8430, 8430, 8430, 8430]	7865580.14	939.00	100	100	[918, 918, 918, 53502]	8501470.79	27.51	Maximum number of iterations	most_probable_scenario	normal
73	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	45.00	100	100	[3930, 10537, 16860, 27397]	8438028.44	14.90	Maximum number of iterations	minimal_1_8430	normal
74	100_it_steps_based_on_915	[8467, 10583, 16934, 27517]	8398967.62	924.00	100	100	[151, 419, 302, 55237]	8505639.07	25.13	Maximum number of iterations	minimal_2_8467	normal
75	100_it_steps_based_on_936	[8467, 8467, 8467, 8467]	7875273.42	936.00	100	100	[43, 43, 43, 56203]	8507168.39	20.10	Maximum number of iterations	weighted_by_scenario_prob	normal
76	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	45.00	100	100	[2726, 3407, 5452, 13359]	6981247.22	191.18	Maximum number of iterations	minimal_3*2_2726	normal
77	100_it_steps_based_on_900	[4089, 5111, 8178, 13289]	7646794.56	930.00	100	100	[369, 461, 738, 54209]	8503963.60	54.92	Maximum number of iterations	minimal_3*3_4089	normal
78	100_it_940_945_step	[8467, 10583, 16934, 27517]	8398967.62	944.00	100	100	[915, 199, 886, 53949]	8502861.33	11.35	Maximum number of iterations	minimal_2_8467	normal
79	100_it_steps_based_on_936	[8475, 8458, 8470, 8472]	7875731.04	939.00	100	100	[24, 7, 19, 56361]	8507315.44	19.92	Maximum number of iterations	hybrid_demand_probabilistic	normal
80	1000_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	16.00	1000	1000	[14, 10537, 13500, 31621]	8458073.30	217.80	Maximum number of iterations	minimal_1_8430	normal
81	100_it_steps_based_on_915	[9389, 8487, 7744, 8099]	7864039.05	930.00	100	100	[89, 117, 304, 55529]	8506352.33	27.91	Maximum number of iterations	cost_sensitive	normal
82	100_it_steps_based_on_900	[8475, 8458, 8470, 8472]	7875731.04	900.00	100	100	[375, 358, 370, 55272]	8505039.49	19.97	Maximum number of iterations	hybrid_demand_probabilistic	normal
83	100_it_steps_based_on_900	[8430, 8430, 8430, 8430]	7865580.14	960.00	100	100	[750, 750, 750, 53550]	8502446.79	19.35	Maximum number of iterations	most_probable_scenario	normal
84	100_it_steps_based_on_900	[8430, 8430, 8430, 8430]	7865580.14	930.00	100	100	[60, 60, 60, 55860]	8507056.34	19.16	Maximum number of iterations	most_probable_scenario	normal
85	100_it_940_945_step	[1363, 1703, 2726, 4429]	3120307.78	942.00	100	100	[421, 761, 842, 54355]	8503149.77	12.91	Maximum number of iterations	minimal_3_1363	normal
86	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	115.00	100	100	[72, 10583, 15669, 29357]	8453185.43	14.26	Maximum number of iterations	minimal_2_8467	normal
87	100_it_940_945_step	[8467, 10583, 16934, 27517]	8398967.62	941.00	100	100	[939, 232, 937, 53865]	8502637.51	11.38	Maximum number of iterations	minimal_2_8467	normal
88	100_it_all_x	[266, 266, 266, 266]	5601.25	20.00	100	100	[2266, 266, 266, 266]	690853.60	24.88	Maximum number of iterations	higher_demand	normal
89	100_it_steps_based_on_500	[8467, 8468, 8469, 8470]	7875668.58	560.00	100	100	[67, 7908, 69, 47110]	8491191.43	22.47	Maximum number of iterations	uniform	normal
90	100_it_940_945_step	[8477, 8472, 8473, 8476]	7877227.30	943.00	100	100	[933, 928, 929, 53740]	8501330.77	12.43	Maximum number of iterations	pseudorandom_5	normal
91	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	30.00	100	100	[4363, 1703, 2726, 4429]	4110026.60	15.18	Maximum number of iterations	minimal_3_1363	normal
92	100_it_900_step	[4089, 5111, 8178, 13289]	7646794.56	925.00	100	100	[389, 486, 778, 54914]	8503819.21	12.11	Maximum number of iterations	minimal_3*3_4089	normal
93	100_it_all_x	[1363, 1703, 2726, 4429]	3120307.78	10.00	100	100	[2363, 1703, 2726, 4429]	3454900.65	23.08	Maximum number of iterations	minimal_3_1363	normal
94	100_it_all_x	[8467, 10583, 16934, 27517]	8398967.62	10.00	100	100	[7467, 10583, 16934, 27517]	8409044.50	23.05	Maximum number of iterations	minimal_2_8467	normal
95	100_it_steps_based_on_915	[8477, 8472, 8473, 8476]	7877227.30	921.00	100	100	[188, 183, 184, 55447]	8506227.38	27.86	Maximum number of iterations	pseudorandom_5	normal
96	100_it_900_step	[2726, 3407, 5452, 8859]	6130430.30	935.00	100	100	[856, 602, 777, 53739]	8502482.90	12.40	Maximum number of iterations	minimal_3*2_2726	normal
97	100_it_all_x	[4089, 5111, 8178, 13289]	7646794.56	18.00	100	100	[4089, 5111, 8178, 15089]	7796199.80	22.79	Maximum number of iterations	minimal_3*3_4089	normal
98	100_it_900_step	[8430, 8430, 8430, 8430]	7865580.14	930.00	100	100	[60, 60, 60, 55860]	8507056.34	12.78	Maximum number of iterations	most_probable_scenario	normal
99	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	30.00	100	100	[8477, 8472, 8473, 11476]	8052050.15	14.98	Maximum number of iterations	pseudorandom_5	normal
100	100_it_936_945_step	[8475, 8458, 8470, 8472]	7875731.04	944.00	100	100	[923, 906, 918, 53784]	8501420.32	12.21	Maximum number of iterations	hybrid_demand_probabilistic	normal
101	1000_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	18.00	1000	1000	[6, 10537, 12504, 32617]	8460225.86	217.17	Maximum number of iterations	minimal_1_8430	normal
102	100_it_940_945_step	[2726, 3407, 5452, 8859]	6130430.30	943.00	100	100	[840, 578, 737, 54123]	8502696.91	12.08	Maximum number of iterations	minimal_3*2_2726	normal
103	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	75.00	100	100	[930, 10537, 16860, 27397]	8448598.85	14.88	Maximum number of iterations	minimal_1_8430	normal
104	100_it_900_step	[8430, 10537, 16860, 27397]	8401544.14	940.00	100	100	[910, 197, 880, 54657]	8502815.77	11.38	Maximum number of iterations	minimal_1_8430	normal
105	100_it_steps_based_on_500	[8467, 10583, 16934, 27517]	8398967.62	530.00	100	100	[517, 4753, 504, 50307]	8496038.66	29.06	Maximum number of iterations	minimal_2_8467	normal
106	100_it_steps_based_on_915	[8467, 10583, 16934, 27517]	8398967.62	939.00	100	100	[16, 254, 32, 55687]	8506842.82	25.66	Maximum number of iterations	minimal_2_8467	normal
107	100_it_940_945_step	[9389, 8487, 7744, 8099]	7864039.05	944.00	100	100	[893, 935, 192, 54355]	8503042.52	12.47	Maximum number of iterations	cost_sensitive	normal
108	5000_it_steps_936_939	[8467, 8467, 8467, 8467]	7875273.42	939.00	5000	5000	[16, 16, 16, 56356]	8507326.77	756.73	Maximum number of iterations	average_demand	normal
109	100_it_steps_based_on_936	[8467, 8468, 8469, 8470]	7875668.58	937.00	100	100	[34, 35, 36, 56257]	8507214.80	20.41	Maximum number of iterations	uniform	normal
110	100_it_936_945_step	[8430, 8430, 8430, 8430]	7865580.14	942.00	100	100	[894, 894, 894, 53646]	8501622.24	12.32	Maximum number of iterations	most_probable_scenario	normal
111	100_it_all_x	[1363, 1703, 2726, 4429]	3120307.78	16.00	100	100	[2963, 1703, 2726, 4429]	3653680.72	23.17	Maximum number of iterations	minimal_3_1363	normal
112	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	940.00	100	100	[7, 7, 7, 56407]	8507377.71	12.65	Maximum number of iterations	weighted_by_scenario_prob	normal
113	100_it_940_945_step	[9389, 8487, 7744, 8099]	7864039.05	945.00	100	100	[884, 927, 184, 54404]	8503092.04	12.46	Maximum number of iterations	cost_sensitive	normal
114	100_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	14.00	100	100	[7030, 10537, 16860, 27397]	8415021.23	29.45	Maximum number of iterations	minimal_1_8430	normal
115	100_it_steps_based_on_500	[1363, 1703, 2726, 4429]	3120307.78	545.00	100	100	[1908, 1703, 2726, 48574]	8492344.88	22.97	Maximum number of iterations	minimal_3_1363	normal
116	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	530.00	100	100	[517, 8467, 517, 45567]	8487869.58	23.96	Maximum number of iterations	weighted_by_scenario_prob	normal
117	100_it_steps_based_on_500	[8475, 8458, 8470, 8472]	7875731.04	530.00	100	100	[525, 8458, 520, 45572]	8487872.06	23.39	Maximum number of iterations	hybrid_demand_probabilistic	normal
118	1000_it_940_step	[8475, 8458, 8470, 8472]	7875731.04	940.00	1000	1000	[15, 938, 10, 55472]	8505584.63	96.72	Maximum number of iterations	hybrid_demand_probabilistic	normal
119	100_it_steps_based_on_936	[8467, 8468, 8469, 8470]	7875668.58	939.00	100	100	[16, 17, 18, 56359]	8507318.74	20.28	Maximum number of iterations	uniform	normal
120	100_it_steps_based_on_915	[8477, 8472, 8473, 8476]	7877227.30	918.00	100	100	[215, 210, 211, 55294]	8506027.17	27.74	Maximum number of iterations	pseudorandom_5	normal
121	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	60.00	100	100	[2430, 10537, 16860, 27397]	8444880.29	14.86	Maximum number of iterations	minimal_1_8430	normal
122	100_it_900_step	[8467, 10583, 16934, 27517]	8398967.62	940.00	100	100	[7, 243, 14, 55717]	8506922.35	11.51	Maximum number of iterations	minimal_2_8467	normal
123	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	935.00	100	100	[52, 52, 52, 56152]	8507113.76	772.20	Maximum number of iterations	average_demand	normal
124	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	942.00	100	100	[931, 931, 931, 53683]	8501346.18	12.35	Maximum number of iterations	average_demand	normal
125	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	575.00	100	100	[417, 6742, 417, 48142]	8492487.56	22.01	Maximum number of iterations	average_demand	normal
126	100_it_940_945_step	[8430, 10537, 16860, 27397]	8401544.14	944.00	100	100	[878, 153, 812, 54773]	8503140.90	11.34	Maximum number of iterations	minimal_1_8430	normal
127	100_it_steps_based_on_915	[2726, 3407, 5452, 8859]	6130430.30	915.00	100	100	[896, 662, 877, 53694]	8502093.86	26.89	Maximum number of iterations	minimal_3*2_2726	normal
128	100_it_900_step	[8430, 10537, 16860, 27397]	8401544.14	930.00	100	100	[60, 307, 120, 55297]	8506359.92	11.51	Maximum number of iterations	minimal_1_8430	normal
129	multi_change_900_step	[8430, 8430, 8430, 8430]	7865580.14	936.00	100	100	[6, 6, 6, 56166]	8507422.61	121.38	Maximum number of iterations	most_probable_scenario	normal
130	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	100.00	100	100	[9389, 8487, 7744, 18099]	8305794.03	15.41	Maximum number of iterations	cost_sensitive	normal
131	100_it_steps_based_on_936	[8467, 8468, 8469, 8470]	7875668.58	936.00	100	100	[43, 44, 45, 56206]	8507161.14	20.28	Maximum number of iterations	uniform	normal
132	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	100.00	100	100	[8467, 8467, 8467, 18467]	8310663.26	2906.28	Maximum number of iterations	weighted_by_scenario_prob	normal
133	100_it_steps_based_on_936	[8477, 8472, 8473, 8476]	7877227.30	937.00	100	100	[44, 39, 40, 56263]	8507167.90	20.09	Maximum number of iterations	pseudorandom_5	normal
134	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	115.00	100	100	[8467, 8467, 8467, 19967]	8345257.44	3073.54	Maximum number of iterations	weighted_by_scenario_prob	normal
135	100_it_steps_based_on_915	[8475, 8458, 8470, 8472]	7875731.04	936.00	100	100	[51, 34, 46, 56208]	8507157.97	27.92	Maximum number of iterations	hybrid_demand_probabilistic	normal
136	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	100.00	100	100	[67, 10583, 16434, 28617]	8451574.61	14.75	Maximum number of iterations	minimal_2_8467	normal
137	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	945.00	100	100	[907, 907, 907, 53827]	8501474.61	12.26	Maximum number of iterations	average_demand	normal
138	100_it_steps_based_on_900	[8467, 8468, 8469, 8470]	7875668.58	900.00	100	100	[367, 368, 369, 55270]	8505042.72	20.06	Maximum number of iterations	uniform	normal
139	100_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	10.00	100	100	[7430, 10537, 16860, 27397]	8411352.97	35.65	Maximum number of iterations	minimal_1_8430	normal
140	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	115.00	100	100	[6883, 1703, 2726, 10409]	6407258.43	1615.65	Maximum number of iterations	minimal_3_1363	normal
141	100_it_steps_based_on_500	[4089, 5111, 8178, 13289]	7646794.56	530.00	100	100	[379, 2461, 228, 51979]	8500371.61	22.24	Maximum number of iterations	minimal_3*3_4089	normal
142	100_it_900_step	[4089, 5111, 8178, 13289]	7646794.56	920.00	100	100	[409, 511, 818, 54689]	8503691.95	12.26	Maximum number of iterations	minimal_3*3_4089	normal
143	100_it_900_step	[8477, 8472, 8473, 8476]	7877227.30	940.00	100	100	[17, 12, 13, 56416]	8507320.52	1980.89	Maximum number of iterations	pseudorandom_5	normal
144	100_it_steps_based_on_936	[8477, 8472, 8473, 8476]	7877227.30	939.00	100	100	[26, 21, 22, 56365]	8507270.07	19.80	Maximum number of iterations	pseudorandom_5	normal
145	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	30.00	100	100	[8477, 8472, 8473, 11476]	8052050.15	15.04	Maximum number of iterations	pseudorandom_5	normal
146	100_it_more_600	[8430, 10537, 16860, 27397]	8401544.14	600.00	100	100	[30, 2137, 60, 53797]	8503171.40	13.55	Maximum number of iterations	minimal_1_8430	normal
147	100_it_steps_based_on_500	[8475, 8458, 8470, 8472]	7875731.04	560.00	100	100	[75, 7898, 70, 47112]	8491189.87	23.52	Maximum number of iterations	hybrid_demand_probabilistic	normal
148	100_it_steps_based_on_915	[8477, 8472, 8473, 8476]	7877227.30	936.00	100	100	[53, 48, 49, 56212]	8507115.25	27.52	Maximum number of iterations	pseudorandom_5	normal
149	100_it_steps_based_on_900	[8430, 10537, 16860, 27397]	8401544.14	975.00	100	100	[630, 787, 285, 54697]	8503770.58	18.28	Maximum number of iterations	minimal_1_8430	normal
150	100_it_steps_based_on_500	[8430, 10537, 16860, 27397]	8401544.14	530.00	100	100	[480, 4707, 430, 50187]	8496254.66	88.16	Maximum number of iterations	minimal_1_8430	normal
151	100_it_900_step	[1363, 1703, 2726, 4429]	3120307.78	940.00	100	100	[423, 763, 846, 54249]	8503146.77	13.04	Maximum number of iterations	minimal_3_1363	normal
152	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	75.00	100	100	[930, 10537, 16860, 27397]	8448598.85	14.84	Maximum number of iterations	minimal_1_8430	normal
153	100_it_steps_based_on_915	[8475, 8458, 8470, 8472]	7875731.04	918.00	100	100	[213, 196, 208, 55290]	8506056.69	27.63	Maximum number of iterations	hybrid_demand_probabilistic	normal
154	100_it_all_x	[9389, 8487, 7744, 8099]	7864039.05	12.00	100	100	[9389, 8487, 7744, 9299]	7941252.24	22.79	Maximum number of iterations	cost_sensitive	normal
155	100_it_steps_based_on_500	[9389, 8487, 7744, 8099]	7864039.05	515.00	100	100	[119, 8487, 2079, 44664]	8485907.18	22.37	Maximum number of iterations	cost_sensitive	normal
156	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	45.00	100	100	[9389, 8487, 7744, 12599]	8114035.77	14.64	Maximum number of iterations	cost_sensitive	normal
157	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	939.00	100	100	[16, 16, 16, 56356]	8507326.77	12.63	Maximum number of iterations	weighted_by_scenario_prob	normal
158	100_it_steps_based_on_500	[2726, 3407, 5452, 8859]	6130430.30	545.00	100	100	[1, 1772, 2, 53549]	8503533.51	22.56	Maximum number of iterations	minimal_3*2_2726	normal
159	100_it_steps_based_on_500	[9389, 8487, 7744, 8099]	7864039.05	500.00	100	100	[389, 8487, 2744, 44099]	8484219.90	22.34	Maximum number of iterations	cost_sensitive	normal
160	100_it_940_945_step	[2726, 3407, 5452, 8859]	6130430.30	944.00	100	100	[838, 575, 732, 54171]	8502715.03	12.19	Maximum number of iterations	minimal_3*2_2726	normal
161	100_it_940_945_step	[8430, 10537, 16860, 27397]	8401544.14	943.00	100	100	[886, 164, 829, 54744]	8503059.70	11.36	Maximum number of iterations	minimal_1_8430	normal
162	100_it_steps_based_on_915	[2726, 3407, 5452, 8859]	6130430.30	930.00	100	100	[866, 617, 802, 53499]	8502290.03	25.86	Maximum number of iterations	minimal_3*2_2726	normal
163	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	45.00	100	100	[8467, 8467, 8467, 12967]	8121910.69	2932.52	Maximum number of iterations	average_demand	normal
164	100_it_900_step	[2726, 3407, 5452, 8859]	6130430.30	940.00	100	100	[846, 587, 752, 53979]	8502632.39	12.22	Maximum number of iterations	minimal_3*2_2726	normal
165	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	935.00	100	100	[52, 52, 52, 56152]	8507113.76	12.62	Maximum number of iterations	weighted_by_scenario_prob	normal
166	1000_it_940_step	[8430, 10537, 16860, 27397]	8401544.14	940.00	1000	1000	[910, 197, 880, 54657]	8502815.77	95.51	Maximum number of iterations	minimal_1_8430	normal
167	100_it_all_x	[8467, 10583, 16934, 27517]	8398967.62	12.00	100	100	[7267, 10583, 16934, 27517]	8410942.50	23.40	Maximum number of iterations	minimal_2_8467	normal
168	5000_it_steps_936_939	[8467, 8467, 8467, 8467]	7875273.42	936.00	5000	5000	[43, 43, 43, 56203]	8507168.39	6553.86	Maximum number of iterations	average_demand	normal
169	100_it_936_945_step	[8475, 8458, 8470, 8472]	7875731.04	945.00	100	100	[915, 898, 910, 53832]	8501462.56	12.20	Maximum number of iterations	hybrid_demand_probabilistic	normal
170	100_it_all_x	[1363, 1703, 2726, 4429]	3120307.78	20.00	100	100	[3363, 1703, 2726, 4429]	3785306.57	22.38	Maximum number of iterations	minimal_3_1363	normal
171	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	115.00	100	100	[9389, 8487, 7744, 19599]	8340993.17	15.46	Maximum number of iterations	cost_sensitive	normal
172	100_it_936_945_step	[8467, 10583, 16934, 27517]	8398967.62	942.00	100	100	[931, 221, 920, 53893]	8502712.18	11.47	Maximum number of iterations	minimal_2_8467	normal
173	100_it_940_945_step	[8430, 8430, 8430, 8430]	7865580.14	942.00	100	100	[894, 894, 894, 53646]	8501622.24	12.33	Maximum number of iterations	most_probable_scenario	normal
174	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	100.00	100	100	[9389, 8487, 7744, 18099]	8305794.03	14.62	Maximum number of iterations	cost_sensitive	normal
175	100_it_steps_based_on_936	[9389, 8487, 7744, 8099]	7864039.05	939.00	100	100	[938, 36, 232, 55049]	8504566.23	20.07	Maximum number of iterations	cost_sensitive	normal
176	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	918.00	100	100	[205, 205, 205, 55285]	8506063.22	46.14	Maximum number of iterations	weighted_by_scenario_prob	normal
177	100_it_steps_based_on_900	[8477, 8472, 8473, 8476]	7877227.30	930.00	100	100	[107, 102, 103, 55906]	8506781.48	20.02	Maximum number of iterations	pseudorandom_5	normal
178	100_it_steps_based_on_900	[8467, 10583, 16934, 27517]	8398967.62	945.00	100	100	[907, 188, 869, 53977]	8502935.83	18.46	Maximum number of iterations	minimal_2_8467	normal
179	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	940.00	100	100	[7, 7, 7, 56407]	8507377.71	12.59	Maximum number of iterations	weighted_by_scenario_prob	normal
180	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	30.00	100	100	[8430, 8430, 8430, 11430]	8043298.19	1254.71	Maximum number of iterations	most_probable_scenario	normal
181	1000_it_steps_936_939	[8467, 8467, 8467, 8467]	7875273.42	939.00	1000	1000	[16, 16, 16, 56356]	8507326.77	197.22	Maximum number of iterations	average_demand	normal
182	100_it_steps_based_on_915	[8430, 8430, 8430, 8430]	7865580.14	930.00	100	100	[60, 60, 60, 55860]	8507056.34	27.65	Maximum number of iterations	most_probable_scenario	normal
183	100_it_steps_based_on_900	[8467, 10583, 16934, 27517]	8398967.62	900.00	100	100	[367, 683, 734, 54517]	8503675.61	18.54	Maximum number of iterations	minimal_2_8467	normal
184	100_it_940_945_step	[8467, 10583, 16934, 27517]	8398967.62	945.00	100	100	[907, 188, 869, 53977]	8502935.83	11.40	Maximum number of iterations	minimal_2_8467	normal
185	100_it_900_step	[8477, 8472, 8473, 8476]	7877227.30	925.00	100	100	[152, 147, 148, 55651]	8506482.57	955.66	Maximum number of iterations	pseudorandom_5	normal
186	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	100.00	100	100	[67, 10583, 16434, 28617]	8451574.61	14.46	Maximum number of iterations	minimal_2_8467	normal
187	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	60.00	100	100	[4089, 5111, 8178, 19289]	8061736.47	14.69	Maximum number of iterations	minimal_3*3_4089	normal
188	100_it_900_step	[8475, 8458, 8470, 8472]	7875731.04	925.00	100	100	[150, 133, 145, 55647]	8506517.30	2983.57	Maximum number of iterations	hybrid_demand_probabilistic	normal
189	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	100.00	100	100	[6863, 1703, 2726, 8929]	6081723.19	14.96	Maximum number of iterations	minimal_3_1363	normal
190	100_it_all_x	[1363, 1363, 1363, 1363]	1504268.24	10.00	100	100	[2363, 1363, 1363, 1363]	1846104.09	22.08	Maximum number of iterations	based_on_demand	normal
191	100_it_steps_based_on_915	[8467, 8468, 8469, 8470]	7875668.58	921.00	100	100	[178, 179, 180, 55441]	8506261.06	27.57	Maximum number of iterations	uniform	normal
192	100_it_940_945_step	[8430, 8430, 8430, 8430]	7865580.14	944.00	100	100	[878, 878, 878, 53742]	8501718.77	12.27	Maximum number of iterations	most_probable_scenario	normal
193	100_it_steps_based_on_500	[8430, 10537, 16860, 27397]	8401544.14	515.00	100	100	[190, 5902, 380, 49542]	8494908.25	88.11	Maximum number of iterations	minimal_1_8430	normal
194	multi_change	[8430, 8430, 8430, 8430]	7865580.14	939.00	100	100	[918, 918, 918, 53502]	8501470.79	119.01	Maximum number of iterations	most_probable_scenario	normal
195	100_it_steps_based_on_500	[8477, 8472, 8473, 8476]	7877227.30	515.00	100	100	[237, 8472, 1778, 45041]	8486512.87	22.55	Maximum number of iterations	pseudorandom_5	normal
196	100_it_900_step	[8467, 10583, 16934, 27517]	8398967.62	925.00	100	100	[142, 408, 284, 55267]	8505719.90	11.54	Maximum number of iterations	minimal_2_8467	normal
197	100_it_940_945_step	[8467, 10583, 16934, 27517]	8398967.62	942.00	100	100	[931, 221, 920, 53893]	8502712.18	11.36	Maximum number of iterations	minimal_2_8467	normal
198	100_it_900_step	[2726, 3407, 5452, 8859]	6130430.30	930.00	100	100	[866, 617, 802, 53499]	8502290.03	12.59	Maximum number of iterations	minimal_3*2_2726	normal
199	100_it_900_step	[9389, 8487, 7744, 8099]	7864039.05	940.00	100	100	[929, 27, 224, 55099]	8504621.20	12.77	Maximum number of iterations	cost_sensitive	normal
200	100_it_all_x	[266, 266, 266, 266]	5601.25	12.00	100	100	[1466, 266, 266, 266]	416786.29	22.74	Maximum number of iterations	higher_demand	normal
201	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	45.00	100	100	[5863, 1703, 2726, 4429]	4582828.77	14.60	Maximum number of iterations	minimal_3_1363	normal
202	100_it_all_x	[8430, 8430, 8430, 8430]	7865580.14	14.00	100	100	[8430, 8430, 8430, 9830]	7954846.14	22.90	Maximum number of iterations	most_probable_scenario	normal
203	100_it_steps_based_on_936	[8430, 8430, 8430, 8430]	7865580.14	939.00	100	100	[918, 918, 918, 53502]	8501470.79	19.91	Maximum number of iterations	most_probable_scenario	normal
204	100_it_steps_based_on_915	[8467, 8468, 8469, 8470]	7875668.58	936.00	100	100	[43, 44, 45, 56206]	8507161.14	27.28	Maximum number of iterations	uniform	normal
205	100_it_936_945_step	[8475, 8458, 8470, 8472]	7875731.04	939.00	100	100	[24, 7, 19, 56361]	8507315.44	12.63	Maximum number of iterations	hybrid_demand_probabilistic	normal
206	100_it_steps_based_on_900	[8467, 8468, 8469, 8470]	7875668.58	960.00	100	100	[787, 788, 789, 53590]	8502267.85	18.94	Maximum number of iterations	uniform	normal
207	100_it_steps_based_on_915	[8467, 8468, 8469, 8470]	7875668.58	939.00	100	100	[16, 17, 18, 56359]	8507318.74	27.06	Maximum number of iterations	uniform	normal
208	100_it_steps_based_on_900	[8475, 8458, 8470, 8472]	7875731.04	930.00	100	100	[105, 88, 100, 55902]	8506819.61	19.97	Maximum number of iterations	hybrid_demand_probabilistic	normal
209	100_it_steps_based_on_915	[8475, 8458, 8470, 8472]	7875731.04	930.00	100	100	[105, 88, 100, 55902]	8506819.61	27.43	Maximum number of iterations	hybrid_demand_probabilistic	normal
210	100_it_936_945_step	[9389, 8487, 7744, 8099]	7864039.05	942.00	100	100	[911, 9, 208, 55199]	8504729.04	12.48	Maximum number of iterations	cost_sensitive	normal
211	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	939.00	100	100	[16, 16, 16, 56356]	8507326.77	93.04	Maximum number of iterations	average_demand	normal
212	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	100.00	100	100	[8467, 8468, 8469, 18470]	8310806.47	14.92	Maximum number of iterations	uniform	normal
213	100_it_936_945_step	[4089, 5111, 8178, 13289]	7646794.56	945.00	100	100	[309, 386, 618, 54869]	8504636.83	11.90	Maximum number of iterations	minimal_3*3_4089	normal
214	100_it_940_945_step	[8477, 8472, 8473, 8476]	7877227.30	940.00	100	100	[17, 12, 13, 56416]	8507320.52	12.91	Maximum number of iterations	pseudorandom_5	normal
215	100_it_all_x	[9389, 8487, 7744, 8099]	7864039.05	10.00	100	100	[9389, 8487, 7744, 9099]	7928967.02	22.99	Maximum number of iterations	cost_sensitive	normal
216	100_it_steps_based_on_915	[8430, 8430, 8430, 8430]	7865580.14	918.00	100	100	[168, 168, 168, 55248]	8506234.19	27.89	Maximum number of iterations	most_probable_scenario	normal
217	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	900.00	100	100	[367, 367, 367, 55267]	8505050.29	19.56	Maximum number of iterations	average_demand	normal
218	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	115.00	100	100	[8477, 8472, 8473, 19976]	8345838.63	14.74	Maximum number of iterations	pseudorandom_5	normal
219	100_it_all_x	[8430, 8430, 8430, 8430]	7865580.14	18.00	100	100	[8430, 8430, 8430, 10230]	7978177.48	22.95	Maximum number of iterations	most_probable_scenario	normal
220	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	75.00	100	100	[2726, 3407, 5452, 16359]	7383153.62	15.69	Maximum number of iterations	minimal_3*2_2726	normal
221	100_it_all_x	[8477, 8472, 8473, 8476]	7877227.30	12.00	100	100	[8477, 8472, 8473, 9676]	7953199.88	27.92	Maximum number of iterations	pseudorandom_5	normal
222	100_it_steps_based_on_915	[8467, 8468, 8469, 8470]	7875668.58	918.00	100	100	[205, 206, 207, 55288]	8506059.35	27.34	Maximum number of iterations	uniform	normal
223	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	115.00	100	100	[8430, 8430, 8430, 19930]	8342367.83	14.79	Maximum number of iterations	most_probable_scenario	normal
224	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	75.00	100	100	[8475, 8458, 8470, 15972]	8238350.95	14.72	Maximum number of iterations	hybrid_demand_probabilistic	normal
225	100_it_steps_based_on_900	[8467, 8468, 8469, 8470]	7875668.58	915.00	100	100	[232, 233, 234, 55135]	8505852.24	19.80	Maximum number of iterations	uniform	normal
226	100_it_steps_based_on_900	[8475, 8458, 8470, 8472]	7875731.04	975.00	100	100	[675, 658, 670, 54297]	8503096.26	19.20	Maximum number of iterations	hybrid_demand_probabilistic	normal
227	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	10.00	100	100	[8467, 8467, 8467, 9467]	7939351.21	23.03	Maximum number of iterations	weighted_by_scenario_prob	normal
228	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	100.00	100	100	[8467, 8467, 8467, 18467]	8310663.26	14.66	Maximum number of iterations	weighted_by_scenario_prob	normal
229	100_it_all_x	[8430, 8430, 8430, 8430]	7865580.14	12.00	100	100	[8430, 8430, 8430, 9630]	7942801.88	22.82	Maximum number of iterations	most_probable_scenario	normal
230	100_it_steps_based_on_500	[4089, 5111, 8178, 13289]	7646794.56	515.00	100	100	[484, 3051, 453, 51399]	8498971.95	22.01	Maximum number of iterations	minimal_3*3_4089	normal
231	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	75.00	100	100	[8467, 8468, 8469, 15970]	8238322.14	14.94	Maximum number of iterations	uniform	normal
232	100_it_all_x	[2726, 3407, 5452, 8859]	6130430.30	12.00	100	100	[2726, 3407, 5452, 10059]	6390214.73	23.08	Maximum number of iterations	minimal_3*2_2726	normal
233	100_it_all_x	[2726, 3407, 5452, 8859]	6130430.30	10.00	100	100	[2726, 3407, 5452, 9859]	6348651.25	22.91	Maximum number of iterations	minimal_3*2_2726	normal
234	100_it_940_945_step	[8475, 8458, 8470, 8472]	7875731.04	942.00	100	100	[939, 922, 934, 53688]	8501334.75	13.87	Maximum number of iterations	hybrid_demand_probabilistic	normal
235	100_it_all_x	[9389, 8487, 7744, 8099]	7864039.05	14.00	100	100	[9389, 8487, 7744, 9499]	7953294.91	22.60	Maximum number of iterations	cost_sensitive	normal
236	100_it_936_945_step	[8430, 8430, 8430, 8430]	7865580.14	936.00	100	100	[6, 6, 6, 56166]	8507422.61	12.67	Maximum number of iterations	most_probable_scenario	normal
237	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	515.00	100	100	[227, 8467, 1772, 45032]	8486525.92	1595.90	Maximum number of iterations	weighted_by_scenario_prob	normal
238	100_it_936_945_step	[8475, 8458, 8470, 8472]	7875731.04	942.00	100	100	[939, 922, 934, 53688]	8501334.75	12.36	Maximum number of iterations	hybrid_demand_probabilistic	normal
239	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	925.00	100	100	[142, 142, 142, 55642]	8506525.36	1573.08	Maximum number of iterations	average_demand	normal
240	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	30.00	100	100	[8467, 8468, 8469, 11470]	8050882.21	14.96	Maximum number of iterations	uniform	normal
241	100_it_steps_based_on_915	[2726, 3407, 5452, 8859]	6130430.30	921.00	100	100	[884, 644, 847, 53988]	8502216.97	26.79	Maximum number of iterations	minimal_3*2_2726	normal
242	100_it_all_x	[8430, 8430, 8430, 8430]	7865580.14	20.00	100	100	[8430, 8430, 8430, 10430]	7989492.19	22.99	Maximum number of iterations	most_probable_scenario	normal
243	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	945.00	100	100	[907, 907, 907, 53827]	8501474.61	20.84	Maximum number of iterations	average_demand	normal
244	multi_change_500_step	[8430, 8430, 8430, 8430]	7865580.14	500.00	100	100	[430, 430, 430, 54930]	8504655.71	120.64	Maximum number of iterations	most_probable_scenario	normal
245	100_it_steps_based_on_500	[1363, 1703, 2726, 4429]	3120307.78	575.00	100	100	[213, 1703, 2726, 50429]	8496911.78	23.12	Maximum number of iterations	minimal_3_1363	normal
246	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	915.00	100	100	[232, 232, 232, 55132]	8505855.51	19.63	Maximum number of iterations	average_demand	normal
247	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	100.00	100	100	[8430, 8430, 8430, 18430]	8307210.00	15.47	Maximum number of iterations	most_probable_scenario	normal
248	100_it_all_x	[4089, 5111, 8178, 13289]	7646794.56	16.00	100	100	[4089, 5111, 8178, 14889]	7780752.27	23.15	Maximum number of iterations	minimal_3*3_4089	normal
249	100_it_steps_based_on_936	[8430, 10537, 16860, 27397]	8401544.14	936.00	100	100	[6, 241, 12, 55477]	8506825.12	17.19	Maximum number of iterations	minimal_1_8430	normal
250	100_it_all_x	[8467, 8468, 8469, 8470]	7875668.58	18.00	100	100	[8467, 8468, 8469, 10270]	7986619.60	388.41	Maximum number of iterations	uniform	normal
251	100_it_all_x	[9389, 8487, 7744, 8099]	7864039.05	16.00	100	100	[9389, 8487, 7744, 9699]	7965085.87	22.65	Maximum number of iterations	cost_sensitive	normal
252	100_it_steps_based_on_915	[8477, 8472, 8473, 8476]	7877227.30	927.00	100	100	[134, 129, 130, 55753]	8506604.12	27.76	Maximum number of iterations	pseudorandom_5	normal
253	100_it_steps_based_on_900	[8475, 8458, 8470, 8472]	7875731.04	945.00	100	100	[915, 898, 910, 53832]	8501462.56	19.27	Maximum number of iterations	hybrid_demand_probabilistic	normal
254	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	75.00	100	100	[8430, 8430, 8430, 15930]	8233434.96	14.71	Maximum number of iterations	most_probable_scenario	normal
255	100_it_940_945_step	[4089, 5111, 8178, 13289]	7646794.56	943.00	100	100	[317, 396, 634, 54781]	8504560.54	11.92	Maximum number of iterations	minimal_3*3_4089	normal
256	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	944.00	100	100	[915, 915, 915, 53779]	8501432.33	12.24	Maximum number of iterations	weighted_by_scenario_prob	normal
257	100_it_steps_based_on_915	[8430, 8430, 8430, 8430]	7865580.14	924.00	100	100	[114, 114, 114, 55554]	8506657.29	27.74	Maximum number of iterations	most_probable_scenario	normal
258	100_it_steps_based_on_500	[4089, 5111, 8178, 13289]	7646794.56	560.00	100	100	[169, 1191, 338, 53609]	8503481.13	21.42	Maximum number of iterations	minimal_3*3_4089	normal
259	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	75.00	100	100	[4089, 5111, 8178, 20789]	8134279.25	15.19	Maximum number of iterations	minimal_3*3_4089	normal
260	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	945.00	100	100	[907, 907, 907, 53827]	8501474.61	26.83	Maximum number of iterations	weighted_by_scenario_prob	normal
261	100_it_all_x	[8467, 8468, 8469, 8470]	7875668.58	14.00	100	100	[8467, 8468, 8469, 9870]	7963667.63	22.82	Maximum number of iterations	uniform	normal
262	100_it_steps_based_on_915	[2726, 3407, 5452, 8859]	6130430.30	924.00	100	100	[878, 635, 832, 54135]	8502249.04	25.64	Maximum number of iterations	minimal_3*2_2726	normal
263	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	941.00	100	100	[939, 939, 939, 53635]	8501301.83	12.41	Maximum number of iterations	average_demand	normal
264	100_it_steps_based_on_936	[2726, 3407, 5452, 8859]	6130430.30	938.00	100	100	[850, 593, 762, 53883]	8502579.41	19.30	Maximum number of iterations	minimal_3*2_2726	normal
265	100_it_900_step	[8467, 10583, 16934, 27517]	8398967.62	935.00	100	100	[52, 298, 104, 55567]	8506524.36	11.58	Maximum number of iterations	minimal_2_8467	normal
266	100_it_steps_based_on_915	[2726, 3407, 5452, 8859]	6130430.30	939.00	100	100	[848, 590, 757, 53931]	8502607.05	25.11	Maximum number of iterations	minimal_3*2_2726	normal
267	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	60.00	100	100	[6883, 1703, 2726, 4909]	5033404.85	15.12	Maximum number of iterations	minimal_3_1363	normal
268	100_it_steps_based_on_936	[8475, 8458, 8470, 8472]	7875731.04	938.00	100	100	[33, 16, 28, 56310]	8507264.15	19.98	Maximum number of iterations	hybrid_demand_probabilistic	normal
269	100_it_steps_based_on_915	[8430, 10537, 16860, 27397]	8401544.14	927.00	100	100	[87, 340, 174, 55207]	8506126.27	25.45	Maximum number of iterations	minimal_1_8430	normal
270	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	75.00	100	100	[967, 10583, 16934, 27517]	8448487.79	14.65	Maximum number of iterations	minimal_2_8467	normal
271	100_it_steps_based_on_936	[8477, 8472, 8473, 8476]	7877227.30	938.00	100	100	[35, 30, 31, 56314]	8507219.25	20.03	Maximum number of iterations	pseudorandom_5	normal
272	100_it_940_945_step	[4089, 5111, 8178, 13289]	7646794.56	945.00	100	100	[309, 386, 618, 54869]	8504636.83	11.96	Maximum number of iterations	minimal_3*3_4089	normal
273	100_it_steps_based_on_900	[8430, 10537, 16860, 27397]	8401544.14	945.00	100	100	[870, 142, 795, 54802]	8503221.97	19.86	Maximum number of iterations	minimal_1_8430	normal
274	100_it_940_945_step	[8430, 8430, 8430, 8430]	7865580.14	941.00	100	100	[902, 902, 902, 53598]	8501572.45	12.36	Maximum number of iterations	most_probable_scenario	normal
275	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	75.00	100	100	[8467, 8467, 8467, 15967]	8238129.39	14.75	Maximum number of iterations	weighted_by_scenario_prob	normal
276	1000_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	12.00	1000	1000	[6, 10537, 15516, 29629]	8453776.38	223.80	Maximum number of iterations	minimal_1_8430	normal
277	100_it_940_945_step	[4089, 5111, 8178, 13289]	7646794.56	944.00	100	100	[313, 391, 626, 54825]	8504599.06	11.95	Maximum number of iterations	minimal_3*3_4089	normal
278	100_it_steps_based_on_936	[8467, 8468, 8469, 8470]	7875668.58	938.00	100	100	[25, 26, 27, 56308]	8507267.41	20.47	Maximum number of iterations	uniform	normal
279	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	100.00	100	100	[8467, 8468, 8469, 18470]	8310806.47	14.64	Maximum number of iterations	uniform	normal
280	100_it_steps_based_on_900	[2726, 3407, 5452, 8859]	6130430.30	945.00	100	100	[836, 572, 727, 54219]	8502731.07	17.63	Maximum number of iterations	minimal_3*2_2726	normal
281	100_it_900_step	[8430, 8430, 8430, 8430]	7865580.14	920.00	100	100	[150, 150, 150, 55350]	8506378.81	12.62	Maximum number of iterations	most_probable_scenario	normal
282	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	975.00	100	100	[667, 667, 667, 54292]	8503106.06	27.18	Maximum number of iterations	weighted_by_scenario_prob	normal
283	100_it_900_step	[8467, 10583, 16934, 27517]	8398967.62	930.00	100	100	[97, 353, 194, 55417]	8506123.24	11.53	Maximum number of iterations	minimal_2_8467	normal
284	100_it_936_945_step	[8430, 10537, 16860, 27397]	8401544.14	936.00	100	100	[6, 241, 12, 55477]	8506825.12	11.41	Maximum number of iterations	minimal_1_8430	normal
285	multi_change_900_step	[8430, 8430, 8430, 8430]	7865580.14	940.00	100	100	[910, 910, 910, 53550]	8501521.93	119.20	Maximum number of iterations	most_probable_scenario	normal
286	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	75.00	100	100	[8467, 8467, 8467, 15967]	8238129.39	2381.23	Maximum number of iterations	average_demand	normal
287	100_it_936_945_step	[8477, 8472, 8473, 8476]	7877227.30	939.00	100	100	[26, 21, 22, 56365]	8507270.07	12.56	Maximum number of iterations	pseudorandom_5	normal
288	100_it_steps_based_on_936	[9389, 8487, 7744, 8099]	7864039.05	937.00	100	100	[19, 54, 248, 55886]	8506780.71	20.38	Maximum number of iterations	cost_sensitive	normal
289	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	115.00	100	100	[4089, 5111, 8178, 24789]	8284525.92	14.69	Maximum number of iterations	minimal_3*3_4089	normal
290	100_it_steps_based_on_900	[8430, 10537, 16860, 27397]	8401544.14	915.00	100	100	[195, 472, 390, 54847]	8505183.99	18.54	Maximum number of iterations	minimal_1_8430	normal
291	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	60.00	100	100	[8467, 8468, 8469, 14470]	8184448.13	15.16	Maximum number of iterations	uniform	normal
292	100_it_all_x	[8467, 10583, 16934, 27517]	8398967.62	20.00	100	100	[6467, 10583, 16934, 27517]	8418194.92	23.56	Maximum number of iterations	minimal_2_8467	normal
293	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	945.00	100	100	[907, 907, 907, 53827]	8501474.61	12.24	Maximum number of iterations	average_demand	normal
294	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	930.00	100	100	[97, 97, 97, 55897]	8506828.77	30.71	Maximum number of iterations	average_demand	normal
295	100_it_steps_based_on_900	[8467, 8468, 8469, 8470]	7875668.58	945.00	100	100	[907, 908, 909, 53830]	8501465.96	19.47	Maximum number of iterations	uniform	normal
296	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	60.00	100	100	[4089, 5111, 8178, 19289]	8061736.47	15.25	Maximum number of iterations	minimal_3*3_4089	normal
297	100_it_all_x	[2726, 3407, 5452, 8859]	6130430.30	14.00	100	100	[2726, 3407, 5452, 10259]	6431123.43	23.28	Maximum number of iterations	minimal_3*2_2726	normal
298	100_it_900_step	[1363, 1703, 2726, 4429]	3120307.78	935.00	100	100	[428, 768, 856, 53984]	8503084.06	13.21	Maximum number of iterations	minimal_3_1363	normal
299	100_it_steps_based_on_915	[9389, 8487, 7744, 8099]	7864039.05	915.00	100	100	[239, 252, 424, 55679]	8505373.48	28.07	Maximum number of iterations	cost_sensitive	normal
300	100_it_936_945_step	[8467, 8468, 8469, 8470]	7875668.58	942.00	100	100	[931, 932, 933, 53686]	8501338.07	12.66	Maximum number of iterations	uniform	normal
301	100_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	18.00	100	100	[6630, 10537, 16860, 27397]	8418540.85	23.28	Maximum number of iterations	minimal_1_8430	normal
302	100_it_steps_based_on_915	[9389, 8487, 7744, 8099]	7864039.05	927.00	100	100	[119, 144, 328, 55376]	8506153.91	27.79	Maximum number of iterations	cost_sensitive	normal
303	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	30.00	100	100	[9389, 8487, 7744, 11099]	8041749.62	15.44	Maximum number of iterations	cost_sensitive	normal
304	5000_it_steps_936_939	[8430, 8430, 8430, 8430]	7865580.14	939.00	5000	5000	[918, 918, 918, 53502]	8501470.79	12714.27	Maximum number of iterations	most_probable_scenario	normal
305	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	10.00	100	100	[8467, 8467, 8467, 9467]	7939351.21	22.73	Maximum number of iterations	average_demand	normal
306	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	100.00	100	100	[8467, 8467, 8467, 18467]	8310663.26	14.76	Maximum number of iterations	average_demand	normal
307	100_it_940_945_step	[8430, 10537, 16860, 27397]	8401544.14	945.00	100	100	[870, 142, 795, 54802]	8503221.97	11.39	Maximum number of iterations	minimal_1_8430	normal
308	1000_it_steps_936_939	[8430, 8430, 8430, 8430]	7865580.14	939.00	1000	1000	[918, 918, 918, 53502]	8501470.79	148.61	Maximum number of iterations	most_probable_scenario	normal
309	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	45.00	100	100	[2726, 3407, 5452, 13359]	6981247.22	15.38	Maximum number of iterations	minimal_3*2_2726	normal
310	100_it_steps_based_on_936	[2726, 3407, 5452, 8859]	6130430.30	939.00	100	100	[848, 590, 757, 53931]	8502607.05	19.36	Maximum number of iterations	minimal_3*2_2726	normal
311	100_it_940_945_step	[2726, 3407, 5452, 8859]	6130430.30	945.00	100	100	[836, 572, 727, 54219]	8502731.07	12.18	Maximum number of iterations	minimal_3*2_2726	normal
312	100_it_steps_based_on_500	[8467, 10583, 16934, 27517]	8398967.62	545.00	100	100	[292, 4588, 39, 50952]	8497829.75	28.85	Maximum number of iterations	minimal_2_8467	normal
313	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	115.00	100	100	[9389, 8487, 7744, 19599]	8340993.17	14.64	Maximum number of iterations	cost_sensitive	normal
314	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	45.00	100	100	[4089, 5111, 8178, 17789]	7978775.31	15.04	Maximum number of iterations	minimal_3*3_4089	normal
315	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	75.00	100	100	[9389, 8487, 7744, 15599]	8231954.31	14.69	Maximum number of iterations	cost_sensitive	normal
316	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	100.00	100	100	[8475, 8458, 8470, 18472]	8310827.21	14.95	Maximum number of iterations	hybrid_demand_probabilistic	normal
317	100_it_steps_based_on_915	[8467, 10583, 16934, 27517]	8398967.62	915.00	100	100	[232, 518, 464, 54967]	8504907.16	25.59	Maximum number of iterations	minimal_2_8467	normal
318	1000_it_940_step	[8467, 8468, 8469, 8470]	7875668.58	940.00	1000	1000	[7, 8, 9, 56410]	8507369.54	100.87	Maximum number of iterations	uniform	normal
319	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	45.00	100	100	[3930, 10537, 16860, 27397]	8438028.44	15.00	Maximum number of iterations	minimal_1_8430	normal
320	100_it_steps_based_on_900	[8467, 10583, 16934, 27517]	8398967.62	975.00	100	100	[667, 833, 359, 54817]	8503304.88	17.75	Maximum number of iterations	minimal_2_8467	normal
321	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	60.00	100	100	[2430, 10537, 16860, 27397]	8444880.29	14.81	Maximum number of iterations	minimal_1_8430	normal
322	100_it_steps_based_on_500	[8430, 8430, 8430, 8430]	7865580.14	500.00	100	100	[430, 8430, 2430, 44430]	8484901.54	22.53	Maximum number of iterations	most_probable_scenario	normal
323	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	30.00	100	100	[5430, 10537, 16860, 27397]	8428104.19	14.84	Maximum number of iterations	minimal_1_8430	normal
324	100_it_steps_based_on_900	[2726, 3407, 5452, 8859]	6130430.30	930.00	100	100	[866, 617, 802, 53499]	8502290.03	2880.46	Maximum number of iterations	minimal_3*2_2726	normal
325	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	115.00	100	100	[8467, 8468, 8469, 19970]	8345377.74	14.62	Maximum number of iterations	uniform	normal
326	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	60.00	100	100	[8477, 8472, 8473, 14476]	8185327.01	15.05	Maximum number of iterations	pseudorandom_5	normal
327	100_it_all_x	[1363, 1363, 1363, 1363]	1504268.24	20.00	100	100	[3363, 1363, 1363, 1363]	2187293.92	23.05	Maximum number of iterations	based_on_demand	normal
328	100_it_steps_based_on_900	[8430, 8430, 8430, 8430]	7865580.14	900.00	100	100	[330, 330, 330, 55230]	8505308.26	27.93	Maximum number of iterations	most_probable_scenario	normal
329	100_it_940_945_step	[8467, 8468, 8469, 8470]	7875668.58	942.00	100	100	[931, 932, 933, 53686]	8501338.07	12.41	Maximum number of iterations	uniform	normal
330	100_it_steps_based_on_915	[8477, 8472, 8473, 8476]	7877227.30	933.00	100	100	[80, 75, 76, 56059]	8506951.83	27.32	Maximum number of iterations	pseudorandom_5	normal
331	100_it_steps_based_on_500	[9389, 8487, 7744, 8099]	7864039.05	545.00	100	100	[124, 8487, 659, 46249]	8489163.83	22.37	Maximum number of iterations	cost_sensitive	normal
332	100_it_all_x	[8475, 8458, 8470, 8472]	7875731.04	16.00	100	100	[8475, 8458, 8470, 10072]	7975308.92	23.97	Maximum number of iterations	hybrid_demand_probabilistic	normal
333	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	30.00	100	100	[8477, 8472, 8473, 11476]	8052050.15	14.75	Maximum number of iterations	pseudorandom_5	normal
334	100_it_steps_based_on_500	[8477, 8472, 8473, 8476]	7877227.30	575.00	100	100	[427, 6747, 423, 48151]	8492463.17	22.44	Maximum number of iterations	pseudorandom_5	normal
335	100_it_all_x	[266, 266, 266, 266]	5601.25	16.00	100	100	[1866, 266, 266, 266]	553821.79	23.00	Maximum number of iterations	higher_demand	normal
336	100_it_all_x	[4089, 5111, 8178, 13289]	7646794.56	20.00	100	100	[4089, 5111, 8178, 15289]	7811355.17	22.65	Maximum number of iterations	minimal_3*3_4089	normal
337	100_it_all_x	[4089, 5111, 8178, 13289]	7646794.56	12.00	100	100	[4089, 5111, 8178, 14489]	7749097.12	5995.80	Maximum number of iterations	minimal_3*3_4089	normal
338	100_it_all_x	[8467, 10583, 16934, 27517]	8398967.62	14.00	100	100	[7067, 10583, 16934, 27517]	8412809.25	23.75	Maximum number of iterations	minimal_2_8467	normal
339	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	45.00	100	100	[5863, 1703, 2726, 4429]	4582828.77	15.02	Maximum number of iterations	minimal_3_1363	normal
340	100_it_steps_based_on_500	[8467, 8468, 8469, 8470]	7875668.58	530.00	100	100	[517, 8468, 519, 45570]	8487873.51	22.45	Maximum number of iterations	uniform	normal
341	100_it_all_x	[266, 266, 266, 266]	5601.25	14.00	100	100	[1666, 266, 266, 266]	485305.89	22.51	Maximum number of iterations	higher_demand	normal
342	multi_change	[8430, 8430, 8430, 8430]	7865580.14	939.00	100	100	[918, 918, 918, 53502]	8501470.79	119.21	Maximum number of iterations	most_probable_scenario	normal
343	100_it_940_945_step	[8467, 8468, 8469, 8470]	7875668.58	943.00	100	100	[923, 924, 925, 53734]	8501381.22	12.37	Maximum number of iterations	uniform	normal
344	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	100.00	100	100	[4089, 5111, 8178, 23289]	8235094.56	14.74	Maximum number of iterations	minimal_3*3_4089	normal
345	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	75.00	100	100	[2726, 3407, 5452, 16359]	7383153.62	14.87	Maximum number of iterations	minimal_3*2_2726	normal
346	100_it_940_945_step	[1363, 1703, 2726, 4429]	3120307.78	941.00	100	100	[422, 762, 844, 54302]	8503150.02	12.89	Maximum number of iterations	minimal_3_1363	normal
347	100_it_900_step	[2726, 3407, 5452, 8859]	6130430.30	920.00	100	100	[886, 647, 852, 53939]	8502201.36	12.34	Maximum number of iterations	minimal_3*2_2726	normal
348	100_it_all_x	[8475, 8458, 8470, 8472]	7875731.04	14.00	100	100	[8475, 8458, 8470, 9872]	7963721.60	23.90	Maximum number of iterations	hybrid_demand_probabilistic	normal
349	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	45.00	100	100	[8475, 8458, 8470, 12972]	8122210.71	14.98	Maximum number of iterations	hybrid_demand_probabilistic	normal
350	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	30.00	100	100	[8430, 8430, 8430, 11430]	8043298.19	189.09	Maximum number of iterations	most_probable_scenario	normal
351	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	960.00	100	100	[787, 787, 787, 53587]	8502271.89	19.68	Maximum number of iterations	average_demand	normal
352	100_it_940_945_step	[9389, 8487, 7744, 8099]	7864039.05	941.00	100	100	[920, 18, 216, 55149]	8504675.56	12.44	Maximum number of iterations	cost_sensitive	normal
353	100_it_steps_based_on_900	[4089, 5111, 8178, 13289]	7646794.56	945.00	100	100	[309, 386, 618, 54869]	8504636.83	52.31	Maximum number of iterations	minimal_3*3_4089	normal
354	100_it_900_step	[8467, 8468, 8469, 8470]	7875668.58	935.00	100	100	[52, 53, 54, 56155]	8507106.62	1991.00	Maximum number of iterations	uniform	normal
355	100_it_steps_based_on_915	[8467, 8468, 8469, 8470]	7875668.58	915.00	100	100	[232, 233, 234, 55135]	8505852.24	27.65	Maximum number of iterations	uniform	normal
356	100_it_steps_based_on_500	[2726, 3407, 5452, 8859]	6130430.30	575.00	100	100	[426, 532, 277, 54859]	8504791.46	43.19	Maximum number of iterations	minimal_3*2_2726	normal
357	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	30.00	100	100	[8467, 8467, 8467, 11467]	8050584.36	2952.21	Maximum number of iterations	average_demand	normal
358	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	100.00	100	100	[67, 10583, 16434, 28617]	8451574.61	2985.07	Maximum number of iterations	minimal_2_8467	normal
359	100_it_steps_based_on_900	[1363, 1703, 2726, 4429]	3120307.78	915.00	100	100	[448, 788, 896, 53839]	8502889.60	20.43	Maximum number of iterations	minimal_3_1363	normal
360	100_it_steps_based_on_500	[8430, 10537, 16860, 27397]	8401544.14	560.00	100	100	[30, 3817, 60, 51477]	8499486.53	30.75	Maximum number of iterations	minimal_1_8430	normal
361	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	100.00	100	100	[8477, 8472, 8473, 18476]	8311357.50	14.96	Maximum number of iterations	pseudorandom_5	normal
362	100_it_steps_based_on_915	[8467, 10583, 16934, 27517]	8398967.62	918.00	100	100	[205, 485, 410, 55057]	8505151.71	25.35	Maximum number of iterations	minimal_2_8467	normal
363	100_it_936_945_step	[8477, 8472, 8473, 8476]	7877227.30	942.00	100	100	[941, 936, 937, 53692]	8501288.27	12.21	Maximum number of iterations	pseudorandom_5	normal
364	100_it_all_x	[1363, 1703, 2726, 4429]	3120307.78	12.00	100	100	[2563, 1703, 2726, 4429]	3521322.54	23.55	Maximum number of iterations	minimal_3_1363	normal
365	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	944.00	100	100	[915, 915, 915, 53779]	8501432.33	12.30	Maximum number of iterations	average_demand	normal
366	100_it_940_945_step	[8430, 10537, 16860, 27397]	8401544.14	941.00	100	100	[902, 186, 863, 54686]	8502897.21	11.47	Maximum number of iterations	minimal_1_8430	normal
367	100_it_936_945_step	[8430, 10537, 16860, 27397]	8401544.14	942.00	100	100	[894, 175, 846, 54715]	8502978.51	11.42	Maximum number of iterations	minimal_1_8430	normal
368	100_it_steps_based_on_936	[8467, 8467, 8467, 8467]	7875273.42	938.00	100	100	[25, 25, 25, 56305]	8507275.21	20.05	Maximum number of iterations	weighted_by_scenario_prob	normal
369	100_it_more_600	[8430, 10537, 16860, 27397]	8401544.14	900.00	100	100	[330, 637, 660, 54397]	8503994.53	11.71	Maximum number of iterations	minimal_1_8430	normal
370	1000_it_940_step	[4089, 5111, 8178, 13289]	7646794.56	940.00	1000	1000	[329, 411, 658, 54649]	8504437.82	96.51	Maximum number of iterations	minimal_3*3_4089	normal
371	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	75.00	100	100	[930, 10537, 16860, 27397]	8448598.85	14.85	Maximum number of iterations	minimal_1_8430	normal
372	100_it_steps_based_on_915	[8475, 8458, 8470, 8472]	7875731.04	921.00	100	100	[186, 169, 181, 55443]	8506258.34	27.91	Maximum number of iterations	hybrid_demand_probabilistic	normal
373	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	115.00	100	100	[35, 10537, 15710, 29352]	8453224.88	14.44	Maximum number of iterations	minimal_1_8430	normal
374	5000_it_940_step	[8467, 8467, 8467, 8467]	7875273.42	940.00	5000	5000	[7, 7, 7, 56407]	8507377.71	466.51	Maximum number of iterations	average_demand	normal
375	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	920.00	100	100	[187, 187, 187, 55387]	8506198.54	1706.13	Maximum number of iterations	average_demand	normal
376	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	75.00	100	100	[9389, 8487, 7744, 15599]	8231954.31	15.13	Maximum number of iterations	cost_sensitive	normal
377	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	939.00	100	100	[16, 16, 16, 56356]	8507326.77	27.61	Maximum number of iterations	weighted_by_scenario_prob	normal
378	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	60.00	100	100	[8467, 8467, 8467, 14467]	8184223.00	14.66	Maximum number of iterations	weighted_by_scenario_prob	normal
379	100_it_steps_based_on_915	[8430, 10537, 16860, 27397]	8401544.14	918.00	100	100	[168, 439, 336, 54937]	8505420.41	25.61	Maximum number of iterations	minimal_1_8430	normal
380	100_it_steps_based_on_936	[8467, 8467, 8467, 8467]	7875273.42	939.00	100	100	[16, 16, 16, 56356]	8507326.77	20.01	Maximum number of iterations	average_demand	normal
381	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	944.00	100	100	[915, 915, 915, 53779]	8501432.33	12.39	Maximum number of iterations	average_demand	normal
382	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	515.00	100	100	[227, 8467, 1772, 45032]	8486525.92	22.30	Maximum number of iterations	average_demand	normal
383	100_it_936_945_step	[8467, 8468, 8469, 8470]	7875668.58	944.00	100	100	[915, 916, 917, 53782]	8501423.71	12.25	Maximum number of iterations	uniform	normal
384	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	75.00	100	100	[4089, 5111, 8178, 20789]	8134279.25	14.89	Maximum number of iterations	minimal_3*3_4089	normal
385	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	30.00	100	100	[9389, 8487, 7744, 11099]	8041749.62	14.74	Maximum number of iterations	cost_sensitive	normal
386	100_it_steps_based_on_936	[2726, 3407, 5452, 8859]	6130430.30	936.00	100	100	[854, 599, 772, 53787]	8502516.73	19.38	Maximum number of iterations	minimal_3*2_2726	normal
387	100_it_steps_based_on_936	[8430, 8430, 8430, 8430]	7865580.14	937.00	100	100	[934, 934, 934, 53406]	8501366.33	20.13	Maximum number of iterations	most_probable_scenario	normal
388	100_it_steps_based_on_915	[8430, 10537, 16860, 27397]	8401544.14	930.00	100	100	[60, 307, 120, 55297]	8506359.92	25.46	Maximum number of iterations	minimal_1_8430	normal
389	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	45.00	100	100	[8430, 8430, 8430, 12930]	8115567.60	14.83	Maximum number of iterations	most_probable_scenario	normal
390	100_it_steps_based_on_500	[1363, 1703, 2726, 4429]	3120307.78	500.00	100	100	[4363, 1703, 2726, 46429]	8486656.25	23.10	Maximum number of iterations	minimal_3_1363	normal
391	100_it_900_step	[8430, 8430, 8430, 8430]	7865580.14	940.00	100	100	[910, 910, 910, 53550]	8501521.93	12.35	Maximum number of iterations	most_probable_scenario	normal
392	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	115.00	100	100	[8467, 8467, 8467, 19967]	8345257.44	1925.43	Maximum number of iterations	average_demand	normal
393	100_it_steps_based_on_900	[9389, 8487, 7744, 8099]	7864039.05	960.00	100	100	[749, 807, 64, 54179]	8503812.09	56.71	Maximum number of iterations	cost_sensitive	normal
394	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	45.00	100	100	[4089, 5111, 8178, 17789]	7978775.31	15.19	Maximum number of iterations	minimal_3*3_4089	normal
395	100_it_all_x	[1363, 1363, 1363, 1363]	1504268.24	12.00	100	100	[2563, 1363, 1363, 1363]	1914392.82	22.03	Maximum number of iterations	based_on_demand	normal
396	100_it_900_step	[8475, 8458, 8470, 8472]	7875731.04	930.00	100	100	[105, 88, 100, 55902]	8506819.61	1942.98	Maximum number of iterations	hybrid_demand_probabilistic	normal
397	100_it_936_945_step	[8467, 10583, 16934, 27517]	8398967.62	936.00	100	100	[43, 287, 86, 55597]	8506604.08	11.99	Maximum number of iterations	minimal_2_8467	normal
398	100_it_936_945_step	[8467, 10583, 16934, 27517]	8398967.62	939.00	100	100	[16, 254, 32, 55687]	8506842.82	11.98	Maximum number of iterations	minimal_2_8467	normal
399	100_it_936_945_step	[8477, 8472, 8473, 8476]	7877227.30	945.00	100	100	[917, 912, 913, 53836]	8501414.10	12.24	Maximum number of iterations	pseudorandom_5	normal
400	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	941.00	100	100	[939, 939, 939, 53635]	8501301.83	12.39	Maximum number of iterations	weighted_by_scenario_prob	normal
401	100_it_936_945_step	[9389, 8487, 7744, 8099]	7864039.05	944.00	100	100	[893, 935, 192, 54355]	8503042.52	12.49	Maximum number of iterations	cost_sensitive	normal
402	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	75.00	100	100	[8477, 8472, 8473, 15976]	8239072.04	14.95	Maximum number of iterations	pseudorandom_5	normal
403	100_it_936_945_step	[9389, 8487, 7744, 8099]	7864039.05	945.00	100	100	[884, 927, 184, 54404]	8503092.04	12.34	Maximum number of iterations	cost_sensitive	normal
404	100_it_steps_based_on_500	[8477, 8472, 8473, 8476]	7877227.30	530.00	100	100	[527, 8472, 523, 45576]	8487872.38	22.20	Maximum number of iterations	pseudorandom_5	normal
405	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	14.00	100	100	[8467, 8467, 8467, 9867]	7963322.67	23.36	Maximum number of iterations	weighted_by_scenario_prob	normal
406	100_it_steps_based_on_900	[4089, 5111, 8178, 13289]	7646794.56	915.00	100	100	[429, 536, 858, 54464]	8503536.71	55.25	Maximum number of iterations	minimal_3*3_4089	normal
407	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	30.00	100	100	[4089, 5111, 8178, 16289]	7882966.26	14.77	Maximum number of iterations	minimal_3*3_4089	normal
408	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	18.00	100	100	[8467, 8467, 8467, 10267]	7986288.32	22.77	Maximum number of iterations	average_demand	normal
409	100_it_940_945_step	[8477, 8472, 8473, 8476]	7877227.30	941.00	100	100	[8, 3, 4, 56467]	8507369.63	210.38	Maximum number of iterations	pseudorandom_5	normal
410	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	924.00	100	100	[151, 151, 151, 55591]	8506462.37	25.54	Maximum number of iterations	average_demand	normal
411	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	75.00	100	100	[8467, 8467, 8467, 15967]	8238129.39	2115.36	Maximum number of iterations	weighted_by_scenario_prob	normal
412	100_it_all_x	[8430, 8430, 8430, 8430]	7865580.14	10.00	100	100	[8430, 8430, 8430, 9430]	7930514.31	22.88	Maximum number of iterations	most_probable_scenario	normal
413	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	930.00	100	100	[97, 97, 97, 55897]	8506828.77	1956.12	Maximum number of iterations	average_demand	normal
414	100_it_936_945_step	[4089, 5111, 8178, 13289]	7646794.56	939.00	100	100	[333, 416, 666, 54605]	8504393.97	11.99	Maximum number of iterations	minimal_3*3_4089	normal
415	100_it_steps_based_on_936	[8467, 10583, 16934, 27517]	8398967.62	937.00	100	100	[34, 276, 68, 55627]	8506683.72	18.72	Maximum number of iterations	minimal_2_8467	normal
416	multi_change	[8430, 8430, 8430, 8430]	7865580.14	936.00	100	100	[6, 6, 6, 56166]	8507422.61	119.64	Maximum number of iterations	most_probable_scenario	normal
417	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	915.00	100	100	[232, 232, 232, 55132]	8505855.51	90.37	Maximum number of iterations	weighted_by_scenario_prob	normal
418	100_it_steps_based_on_915	[8467, 8468, 8469, 8470]	7875668.58	930.00	100	100	[97, 98, 99, 55900]	8506822.61	27.48	Maximum number of iterations	uniform	normal
419	100_it_900_step	[8430, 10537, 16860, 27397]	8401544.14	935.00	100	100	[15, 252, 30, 55447]	8506747.78	11.50	Maximum number of iterations	minimal_1_8430	normal
420	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	115.00	100	100	[35, 10537, 15710, 29352]	8453224.88	14.47	Maximum number of iterations	minimal_1_8430	normal
421	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	936.00	100	100	[43, 43, 43, 56203]	8507168.39	69.16	Maximum number of iterations	average_demand	normal
422	100_it_steps_based_on_500	[8467, 10583, 16934, 27517]	8398967.62	500.00	100	100	[467, 6083, 434, 48517]	8493373.97	89.07	Maximum number of iterations	minimal_2_8467	normal
423	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	930.00	100	100	[97, 97, 97, 55897]	8506828.77	12.93	Maximum number of iterations	weighted_by_scenario_prob	normal
424	100_it_900_step	[9389, 8487, 7744, 8099]	7864039.05	925.00	100	100	[139, 162, 344, 55274]	8506018.87	12.77	Maximum number of iterations	cost_sensitive	normal
425	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	115.00	100	100	[8467, 8467, 8467, 19967]	8345257.44	14.67	Maximum number of iterations	weighted_by_scenario_prob	normal
426	100_it_940_945_step	[1363, 1703, 2726, 4429]	3120307.78	944.00	100	100	[419, 759, 838, 54461]	8503138.19	12.87	Maximum number of iterations	minimal_3_1363	normal
427	100_it_steps_based_on_500	[9389, 8487, 7744, 8099]	7864039.05	560.00	100	100	[429, 7927, 464, 47299]	8490307.29	22.42	Maximum number of iterations	cost_sensitive	normal
428	100_it_940_945_step	[4089, 5111, 8178, 13289]	7646794.56	942.00	100	100	[321, 401, 642, 54737]	8504520.65	11.97	Maximum number of iterations	minimal_3*3_4089	normal
429	100_it_936_945_step	[8430, 10537, 16860, 27397]	8401544.14	945.00	100	100	[870, 142, 795, 54802]	8503221.97	11.46	Maximum number of iterations	minimal_1_8430	normal
430	100_it_936_945_step	[2726, 3407, 5452, 8859]	6130430.30	936.00	100	100	[854, 599, 772, 53787]	8502516.73	12.43	Maximum number of iterations	minimal_3*2_2726	normal
431	100_it_900_step	[1363, 1703, 2726, 4429]	3120307.78	920.00	100	100	[443, 783, 886, 54109]	8502975.84	13.18	Maximum number of iterations	minimal_3_1363	normal
432	100_it_steps_based_on_500	[8467, 8468, 8469, 8470]	7875668.58	545.00	100	100	[292, 8468, 294, 46620]	8489723.95	22.48	Maximum number of iterations	uniform	normal
433	100_it_steps_based_on_500	[9389, 8487, 7744, 8099]	7864039.05	575.00	100	100	[189, 7337, 269, 47774]	8492097.32	22.25	Maximum number of iterations	cost_sensitive	normal
434	1000_it_940_step	[9389, 8487, 7744, 8099]	7864039.05	940.00	1000	1000	[929, 27, 224, 55099]	8504621.20	98.10	Maximum number of iterations	cost_sensitive	normal
435	100_it_936_945_step	[8430, 8430, 8430, 8430]	7865580.14	945.00	100	100	[870, 870, 870, 53790]	8501765.82	12.37	Maximum number of iterations	most_probable_scenario	normal
436	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	500.00	100	100	[467, 8467, 2467, 44467]	8484768.30	22.91	Maximum number of iterations	weighted_by_scenario_prob	normal
437	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	60.00	100	100	[2430, 10537, 16860, 27397]	8444880.29	15.14	Maximum number of iterations	minimal_1_8430	normal
438	100_it_936_945_step	[8467, 8468, 8469, 8470]	7875668.58	936.00	100	100	[43, 44, 45, 56206]	8507161.14	12.59	Maximum number of iterations	uniform	normal
439	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	45.00	100	100	[3967, 10583, 16934, 27517]	8436724.38	14.91	Maximum number of iterations	minimal_2_8467	normal
440	100_it_940_945_step	[8467, 8468, 8469, 8470]	7875668.58	940.00	100	100	[7, 8, 9, 56410]	8507369.54	12.70	Maximum number of iterations	uniform	normal
441	100_it_steps_based_on_900	[9389, 8487, 7744, 8099]	7864039.05	930.00	100	100	[89, 117, 304, 55529]	8506352.33	65.60	Maximum number of iterations	cost_sensitive	normal
442	multi_change_900_step	[8430, 8430, 8430, 8430]	7865580.14	939.00	100	100	[918, 918, 918, 53502]	8501470.79	135.12	Maximum number of iterations	most_probable_scenario	normal
443	100_it_steps_based_on_915	[8475, 8458, 8470, 8472]	7875731.04	939.00	100	100	[24, 7, 19, 56361]	8507315.44	27.41	Maximum number of iterations	hybrid_demand_probabilistic	normal
444	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	60.00	100	100	[9389, 8487, 7744, 14099]	8177231.12	14.66	Maximum number of iterations	cost_sensitive	normal
445	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	45.00	100	100	[3930, 10537, 16860, 27397]	8438028.44	14.70	Maximum number of iterations	minimal_1_8430	normal
446	100_it_all_x	[1363, 1363, 1363, 1363]	1504268.24	14.00	100	100	[2763, 1363, 1363, 1363]	1982661.19	22.34	Maximum number of iterations	based_on_demand	normal
447	100_it_steps_based_on_936	[8467, 8467, 8467, 8467]	7875273.42	938.00	100	100	[25, 25, 25, 56305]	8507275.21	19.98	Maximum number of iterations	average_demand	normal
448	100_it_steps_based_on_936	[8467, 10583, 16934, 27517]	8398967.62	938.00	100	100	[25, 265, 50, 55657]	8506763.28	18.47	Maximum number of iterations	minimal_2_8467	normal
449	100_it_steps_based_on_900	[2726, 3407, 5452, 8859]	6130430.30	915.00	100	100	[896, 662, 877, 53694]	8502093.86	58.53	Maximum number of iterations	minimal_3*2_2726	normal
450	100_it_steps_based_on_900	[8477, 8472, 8473, 8476]	7877227.30	960.00	100	100	[797, 792, 793, 53596]	8502234.97	19.64	Maximum number of iterations	pseudorandom_5	normal
451	100_it_steps_based_on_915	[8430, 8430, 8430, 8430]	7865580.14	915.00	100	100	[195, 195, 195, 56010]	8506079.01	27.43	Maximum number of iterations	most_probable_scenario	normal
452	100_it_steps_based_on_915	[8477, 8472, 8473, 8476]	7877227.30	939.00	100	100	[26, 21, 22, 56365]	8507270.07	27.63	Maximum number of iterations	pseudorandom_5	normal
453	100_it_steps_based_on_915	[9389, 8487, 7744, 8099]	7864039.05	924.00	100	100	[149, 171, 352, 55223]	8505950.45	27.70	Maximum number of iterations	cost_sensitive	normal
454	100_it_940_945_step	[8467, 10583, 16934, 27517]	8398967.62	943.00	100	100	[923, 210, 903, 53921]	8502786.78	11.32	Maximum number of iterations	minimal_2_8467	normal
455	100_it_steps_based_on_936	[8430, 8430, 8430, 8430]	7865580.14	936.00	100	100	[6, 6, 6, 56166]	8507422.61	20.49	Maximum number of iterations	most_probable_scenario	normal
456	100_it_940_945_step	[8430, 10537, 16860, 27397]	8401544.14	942.00	100	100	[894, 175, 846, 54715]	8502978.51	11.44	Maximum number of iterations	minimal_1_8430	normal
457	100_it_all_x	[8477, 8472, 8473, 8476]	7877227.30	16.00	100	100	[8477, 8472, 8473, 10076]	7976584.13	24.32	Maximum number of iterations	pseudorandom_5	normal
458	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	60.00	100	100	[8475, 8458, 8470, 14472]	8184482.26	493.14	Maximum number of iterations	hybrid_demand_probabilistic	normal
459	100_it_936_945_step	[8477, 8472, 8473, 8476]	7877227.30	944.00	100	100	[925, 920, 921, 53788]	8501373.03	12.21	Maximum number of iterations	pseudorandom_5	normal
460	100_it_900_step	[1363, 1703, 2726, 4429]	3120307.78	930.00	100	100	[433, 773, 866, 53719]	8502941.26	13.31	Maximum number of iterations	minimal_3_1363	normal
461	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	75.00	100	100	[8477, 8472, 8473, 15976]	8239072.04	14.96	Maximum number of iterations	pseudorandom_5	normal
462	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	940.00	100	100	[7, 7, 7, 56407]	8507377.71	12.61	Maximum number of iterations	average_demand	normal
463	100_it_steps_based_on_915	[8430, 8430, 8430, 8430]	7865580.14	933.00	100	100	[33, 33, 33, 56013]	8507243.13	28.03	Maximum number of iterations	most_probable_scenario	normal
464	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	60.00	100	100	[6883, 1703, 2726, 4909]	5033404.85	14.61	Maximum number of iterations	minimal_3_1363	normal
465	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	115.00	100	100	[8475, 8458, 8470, 19972]	8345394.78	14.90	Maximum number of iterations	hybrid_demand_probabilistic	normal
466	100_it_936_945_step	[2726, 3407, 5452, 8859]	6130430.30	939.00	100	100	[848, 590, 757, 53931]	8502607.05	12.25	Maximum number of iterations	minimal_3*2_2726	normal
467	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	45.00	100	100	[8475, 8458, 8470, 12972]	8122210.71	14.99	Maximum number of iterations	hybrid_demand_probabilistic	normal
468	100_it_940_945_step	[9389, 8487, 7744, 8099]	7864039.05	940.00	100	100	[929, 27, 224, 55099]	8504621.20	12.47	Maximum number of iterations	cost_sensitive	normal
469	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	115.00	100	100	[8477, 8472, 8473, 19976]	8345838.63	14.96	Maximum number of iterations	pseudorandom_5	normal
470	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	45.00	100	100	[8477, 8472, 8473, 12976]	8123189.21	33.67	Maximum number of iterations	pseudorandom_5	normal
471	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	30.00	100	100	[2726, 3407, 5452, 11859]	6734029.53	663.61	Maximum number of iterations	minimal_3*2_2726	normal
472	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	60.00	100	100	[2467, 10583, 16934, 27517]	8444192.76	14.56	Maximum number of iterations	minimal_2_8467	normal
473	1000_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	20.00	1000	1000	[10, 10537, 11500, 33617]	8462373.99	20210.42	Maximum number of iterations	minimal_1_8430	normal
474	100_it_900_step	[8430, 10537, 16860, 27397]	8401544.14	920.00	100	100	[150, 417, 300, 54997]	8505577.74	11.46	Maximum number of iterations	minimal_1_8430	normal
475	100_it_steps_based_on_500	[1363, 1703, 2726, 4429]	3120307.78	515.00	100	100	[3423, 1703, 2726, 47689]	8489454.73	339.49	Maximum number of iterations	minimal_3_1363	normal
476	100_it_936_945_step	[4089, 5111, 8178, 13289]	7646794.56	944.00	100	100	[313, 391, 626, 54825]	8504599.06	11.98	Maximum number of iterations	minimal_3*3_4089	normal
477	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	75.00	100	100	[8467, 8468, 8469, 15970]	8238322.14	14.73	Maximum number of iterations	uniform	normal
478	100_it_more_600	[8430, 10537, 16860, 27397]	8401544.14	700.00	100	100	[30, 37, 60, 56097]	8507188.14	12.75	Maximum number of iterations	minimal_1_8430	normal
479	100_it_steps_based_on_915	[9389, 8487, 7744, 8099]	7864039.05	936.00	100	100	[29, 63, 256, 55835]	8506721.57	27.96	Maximum number of iterations	cost_sensitive	normal
480	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	30.00	100	100	[8475, 8458, 8470, 11472]	8050928.37	14.72	Maximum number of iterations	hybrid_demand_probabilistic	normal
481	100_it_936_945_step	[4089, 5111, 8178, 13289]	7646794.56	942.00	100	100	[321, 401, 642, 54737]	8504520.65	11.88	Maximum number of iterations	minimal_3*3_4089	normal
482	100_it_steps_based_on_900	[8475, 8458, 8470, 8472]	7875731.04	915.00	100	100	[240, 223, 235, 55137]	8505849.68	20.63	Maximum number of iterations	hybrid_demand_probabilistic	normal
483	100_it_steps_based_on_915	[8430, 8430, 8430, 8430]	7865580.14	927.00	100	100	[87, 87, 87, 55707]	8506859.47	27.37	Maximum number of iterations	most_probable_scenario	normal
484	100_it_steps_based_on_915	[8475, 8458, 8470, 8472]	7875731.04	924.00	100	100	[159, 142, 154, 55596]	8506454.53	28.04	Maximum number of iterations	hybrid_demand_probabilistic	normal
485	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	945.00	100	100	[907, 907, 907, 53827]	8501474.61	12.29	Maximum number of iterations	weighted_by_scenario_prob	normal
486	100_it_steps_based_on_936	[8467, 10583, 16934, 27517]	8398967.62	939.00	100	100	[16, 254, 32, 55687]	8506842.82	18.27	Maximum number of iterations	minimal_2_8467	normal
487	100_it_940_945_step	[2726, 3407, 5452, 8859]	6130430.30	940.00	100	100	[846, 587, 752, 53979]	8502632.39	12.22	Maximum number of iterations	minimal_3*2_2726	normal
488	100_it_900_step	[8430, 8430, 8430, 8430]	7865580.14	925.00	100	100	[105, 105, 105, 55605]	8506725.30	12.67	Maximum number of iterations	most_probable_scenario	normal
489	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	45.00	100	100	[8467, 8467, 8467, 12967]	8121910.69	14.70	Maximum number of iterations	weighted_by_scenario_prob	normal
490	100_it_steps_based_on_900	[8477, 8472, 8473, 8476]	7877227.30	975.00	100	100	[677, 672, 673, 54301]	8503055.70	19.37	Maximum number of iterations	pseudorandom_5	normal
491	100_it_936_945_step	[8430, 10537, 16860, 27397]	8401544.14	939.00	100	100	[918, 208, 897, 54628]	8502734.24	11.60	Maximum number of iterations	minimal_1_8430	normal
492	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	60.00	100	100	[8467, 8467, 8467, 14467]	8184223.00	1047.49	Maximum number of iterations	average_demand	normal
493	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	60.00	100	100	[2467, 10583, 16934, 27517]	8444192.76	15.22	Maximum number of iterations	minimal_2_8467	normal
494	100_it_900_step	[8430, 8430, 8430, 8430]	7865580.14	935.00	100	100	[15, 15, 15, 56115]	8507363.34	12.57	Maximum number of iterations	most_probable_scenario	normal
495	100_it_936_945_step	[8467, 8468, 8469, 8470]	7875668.58	939.00	100	100	[16, 17, 18, 56359]	8507318.74	12.63	Maximum number of iterations	uniform	normal
496	1000_it_940_step	[1363, 1703, 2726, 4429]	3120307.78	940.00	1000	1000	[423, 763, 846, 54249]	8503146.77	97.37	Maximum number of iterations	minimal_3_1363	normal
497	100_it_940_945_step	[1363, 1703, 2726, 4429]	3120307.78	943.00	100	100	[420, 760, 840, 54408]	8503145.34	12.89	Maximum number of iterations	minimal_3_1363	normal
498	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	933.00	100	100	[70, 70, 70, 56050]	8507002.21	28.69	Maximum number of iterations	weighted_by_scenario_prob	normal
499	100_it_936_945_step	[8467, 8468, 8469, 8470]	7875668.58	945.00	100	100	[907, 908, 909, 53830]	8501465.96	12.28	Maximum number of iterations	uniform	normal
500	100_it_all_x	[8477, 8472, 8473, 8476]	7877227.30	20.00	100	100	[8477, 8472, 8473, 10476]	7999067.46	23.73	Maximum number of iterations	pseudorandom_5	normal
501	100_it_940_945_step	[8477, 8472, 8473, 8476]	7877227.30	944.00	100	100	[925, 920, 921, 53788]	8501373.03	13.30	Maximum number of iterations	pseudorandom_5	normal
502	100_it_900_step	[9389, 8487, 7744, 8099]	7864039.05	935.00	100	100	[39, 72, 264, 55784]	8506661.89	12.67	Maximum number of iterations	cost_sensitive	normal
503	100_it_steps_based_on_915	[8430, 8430, 8430, 8430]	7865580.14	936.00	100	100	[6, 6, 6, 56166]	8507422.61	27.71	Maximum number of iterations	most_probable_scenario	normal
504	100_it_steps_based_on_500	[2726, 3407, 5452, 8859]	6130430.30	515.00	100	100	[151, 2892, 302, 52119]	8500528.21	22.64	Maximum number of iterations	minimal_3*2_2726	normal
505	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	940.00	100	100	[7, 7, 7, 56407]	8507377.71	1888.13	Maximum number of iterations	average_demand	normal
506	100_it_936_945_step	[8430, 8430, 8430, 8430]	7865580.14	944.00	100	100	[878, 878, 878, 53742]	8501718.77	12.39	Maximum number of iterations	most_probable_scenario	normal
507	100_it_900_step	[4089, 5111, 8178, 13289]	7646794.56	930.00	100	100	[369, 461, 738, 54209]	8503963.60	12.34	Maximum number of iterations	minimal_3*3_4089	normal
508	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	30.00	100	100	[8475, 8458, 8470, 11472]	8050928.37	14.98	Maximum number of iterations	hybrid_demand_probabilistic	normal
509	100_it_940_945_step	[2726, 3407, 5452, 8859]	6130430.30	941.00	100	100	[844, 584, 747, 54027]	8502655.62	12.13	Maximum number of iterations	minimal_3*2_2726	normal
510	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	945.00	100	100	[907, 907, 907, 53827]	8501474.61	12.34	Maximum number of iterations	weighted_by_scenario_prob	normal
511	100_it_more_600	[8430, 10537, 16860, 27397]	8401544.14	800.00	100	100	[430, 137, 60, 55397]	8505984.42	12.32	Maximum number of iterations	minimal_1_8430	normal
512	100_it_steps_based_on_900	[8467, 10583, 16934, 27517]	8398967.62	915.00	100	100	[232, 518, 464, 54967]	8504907.16	19.34	Maximum number of iterations	minimal_2_8467	normal
513	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	16.00	100	100	[8467, 8467, 8467, 10067]	7974918.24	22.90	Maximum number of iterations	weighted_by_scenario_prob	normal
514	100_it_steps_based_on_915	[8477, 8472, 8473, 8476]	7877227.30	915.00	100	100	[242, 237, 238, 55141]	8505821.81	27.73	Maximum number of iterations	pseudorandom_5	normal
515	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	16.00	100	100	[8467, 8467, 8467, 10067]	7974918.24	22.39	Maximum number of iterations	average_demand	normal
516	100_it_steps_based_on_500	[8477, 8472, 8473, 8476]	7877227.30	560.00	100	100	[77, 7912, 73, 47116]	8491187.45	22.84	Maximum number of iterations	pseudorandom_5	normal
517	100_it_all_x	[9389, 8487, 7744, 8099]	7864039.05	20.00	100	100	[9389, 8487, 7744, 10099]	7987939.22	22.61	Maximum number of iterations	cost_sensitive	normal
518	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	115.00	100	100	[8475, 8458, 8470, 19972]	8345394.78	14.98	Maximum number of iterations	hybrid_demand_probabilistic	normal
519	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	115.00	100	100	[2726, 3407, 5452, 20359]	7769173.16	14.86	Maximum number of iterations	minimal_3*2_2726	normal
520	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	100.00	100	100	[30, 10537, 16460, 28597]	8451612.51	14.47	Maximum number of iterations	minimal_1_8430	normal
521	100_it_steps_based_on_915	[8467, 8468, 8469, 8470]	7875668.58	924.00	100	100	[151, 152, 153, 55594]	8506457.39	27.63	Maximum number of iterations	uniform	normal
522	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	45.00	100	100	[3967, 10583, 16934, 27517]	8436724.38	14.58	Maximum number of iterations	minimal_2_8467	normal
523	100_it_936_945_step	[8467, 10583, 16934, 27517]	8398967.62	944.00	100	100	[915, 199, 886, 53949]	8502861.33	11.37	Maximum number of iterations	minimal_2_8467	normal
524	100_it_all_x	[8477, 8472, 8473, 8476]	7877227.30	10.00	100	100	[8477, 8472, 8473, 9476]	7941128.40	28.87	Maximum number of iterations	pseudorandom_5	normal
525	100_it_steps_based_on_936	[8475, 8458, 8470, 8472]	7875731.04	936.00	100	100	[51, 34, 46, 56208]	8507157.97	19.99	Maximum number of iterations	hybrid_demand_probabilistic	normal
526	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	100.00	100	100	[30, 10537, 16460, 28597]	8451612.51	14.66	Maximum number of iterations	minimal_1_8430	normal
527	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	115.00	100	100	[2726, 3407, 5452, 20359]	7769173.16	15.30	Maximum number of iterations	minimal_3*2_2726	normal
528	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	30.00	100	100	[5467, 10583, 16934, 27517]	8426342.64	14.58	Maximum number of iterations	minimal_2_8467	normal
529	100_it_steps_based_on_500	[8477, 8472, 8473, 8476]	7877227.30	545.00	100	100	[302, 8472, 298, 46626]	8489704.04	22.59	Maximum number of iterations	pseudorandom_5	normal
530	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	45.00	100	100	[8467, 8468, 8469, 12970]	8122170.79	14.65	Maximum number of iterations	uniform	normal
531	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	60.00	100	100	[8467, 8467, 8467, 14467]	8184223.00	3052.34	Maximum number of iterations	weighted_by_scenario_prob	normal
532	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	75.00	100	100	[8467, 8467, 8467, 15967]	8238129.39	14.82	Maximum number of iterations	average_demand	normal
533	100_it_steps_based_on_900	[9389, 8487, 7744, 8099]	7864039.05	975.00	100	100	[614, 687, 919, 53924]	8502659.60	56.42	Maximum number of iterations	cost_sensitive	normal
534	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	100.00	100	100	[8477, 8472, 8473, 18476]	8311357.50	14.95	Maximum number of iterations	pseudorandom_5	normal
535	100_it_900_step	[8467, 8468, 8469, 8470]	7875668.58	930.00	100	100	[97, 98, 99, 55900]	8506822.61	1968.93	Maximum number of iterations	uniform	normal
536	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	975.00	100	100	[667, 667, 667, 54292]	8503106.06	19.41	Maximum number of iterations	average_demand	normal
537	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	936.00	100	100	[43, 43, 43, 56203]	8507168.39	12.61	Maximum number of iterations	weighted_by_scenario_prob	normal
538	100_it_steps_based_on_500	[8430, 10537, 16860, 27397]	8401544.14	500.00	100	100	[430, 6037, 360, 48397]	8493354.26	71.39	Maximum number of iterations	minimal_1_8430	normal
539	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	920.00	100	100	[187, 187, 187, 55387]	8506198.54	1048.93	Maximum number of iterations	weighted_by_scenario_prob	normal
540	100_it_steps_based_on_900	[1363, 1703, 2726, 4429]	3120307.78	900.00	100	100	[463, 803, 26, 54829]	8504725.68	20.62	Maximum number of iterations	minimal_3_1363	normal
541	100_it_steps_based_on_900	[2726, 3407, 5452, 8859]	6130430.30	960.00	100	100	[806, 527, 652, 53979]	8503015.20	18.16	Maximum number of iterations	minimal_3*2_2726	normal
542	100_it_steps_based_on_500	[4089, 5111, 8178, 13289]	7646794.56	545.00	100	100	[274, 2386, 3, 53074]	8502078.01	21.73	Maximum number of iterations	minimal_3*3_4089	normal
543	100_it_900_step	[8467, 8468, 8469, 8470]	7875668.58	920.00	100	100	[187, 188, 189, 55390]	8506194.36	2015.18	Maximum number of iterations	uniform	normal
544	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	75.00	100	100	[967, 10583, 16934, 27517]	8448487.79	14.85	Maximum number of iterations	minimal_2_8467	normal
545	100_it_900_step	[8467, 8467, 8467, 8467]	7875273.42	925.00	100	100	[142, 142, 142, 55642]	8506525.36	468.59	Maximum number of iterations	weighted_by_scenario_prob	normal
546	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	930.00	100	100	[97, 97, 97, 55897]	8506828.77	19.98	Maximum number of iterations	average_demand	normal
547	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	560.00	100	100	[67, 7907, 67, 47107]	8491188.12	22.86	Maximum number of iterations	average_demand	normal
548	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	45.00	100	100	[8475, 8458, 8470, 12972]	8122210.71	15.16	Maximum number of iterations	hybrid_demand_probabilistic	normal
549	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	60.00	100	100	[8477, 8472, 8473, 14476]	8185327.01	14.94	Maximum number of iterations	pseudorandom_5	normal
550	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	45.00	100	100	[8467, 8467, 8467, 12967]	8121910.69	14.70	Maximum number of iterations	average_demand	normal
551	100_it_steps_based_on_900	[4089, 5111, 8178, 13289]	7646794.56	975.00	100	100	[189, 236, 378, 55214]	8505712.46	51.70	Maximum number of iterations	minimal_3*3_4089	normal
552	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	942.00	100	100	[931, 931, 931, 53683]	8501346.18	12.42	Maximum number of iterations	average_demand	normal
553	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	115.00	100	100	[8430, 8430, 8430, 19930]	8342367.83	15.39	Maximum number of iterations	most_probable_scenario	normal
554	100_it_steps_based_on_936	[9389, 8487, 7744, 8099]	7864039.05	936.00	100	100	[29, 63, 256, 55835]	8506721.57	20.33	Maximum number of iterations	cost_sensitive	normal
555	100_it_steps_based_on_900	[8430, 8430, 8430, 8430]	7865580.14	975.00	100	100	[630, 630, 630, 54255]	8503347.56	19.37	Maximum number of iterations	most_probable_scenario	normal
556	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	100.00	100	100	[30, 10537, 16460, 28597]	8451612.51	14.78	Maximum number of iterations	minimal_1_8430	normal
557	100_it_steps_based_on_936	[8430, 10537, 16860, 27397]	8401544.14	937.00	100	100	[934, 230, 931, 54570]	8502570.92	17.55	Maximum number of iterations	minimal_1_8430	normal
558	100_it_steps_based_on_936	[2726, 3407, 5452, 8859]	6130430.30	937.00	100	100	[852, 596, 767, 53835]	8502549.81	19.27	Maximum number of iterations	minimal_3*2_2726	normal
559	100_it_steps_based_on_915	[8430, 10537, 16860, 27397]	8401544.14	915.00	100	100	[195, 472, 390, 54847]	8505183.99	25.44	Maximum number of iterations	minimal_1_8430	normal
560	100_it_940_945_step	[8467, 8468, 8469, 8470]	7875668.58	941.00	100	100	[939, 940, 0, 54579]	8503307.84	12.48	Maximum number of iterations	uniform	normal
561	100_it_steps_based_on_915	[2726, 3407, 5452, 8859]	6130430.30	933.00	100	100	[860, 608, 787, 53643]	8502411.44	25.71	Maximum number of iterations	minimal_3*2_2726	normal
562	100_it_steps_based_on_915	[8430, 10537, 16860, 27397]	8401544.14	939.00	100	100	[918, 208, 897, 54628]	8502734.24	25.57	Maximum number of iterations	minimal_1_8430	normal
563	100_it_all_x	[2726, 3407, 5452, 8859]	6130430.30	18.00	100	100	[2726, 3407, 5452, 10659]	6510959.64	23.25	Maximum number of iterations	minimal_3*2_2726	normal
564	100_it_steps_based_on_500	[2726, 3407, 5452, 8859]	6130430.30	500.00	100	100	[226, 3407, 452, 51359]	8499007.64	22.64	Maximum number of iterations	minimal_3*2_2726	normal
565	100_it_940_945_step	[1363, 1703, 2726, 4429]	3120307.78	940.00	100	100	[423, 763, 846, 54249]	8503146.77	12.81	Maximum number of iterations	minimal_3_1363	normal
566	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	30.00	100	100	[8467, 8468, 8469, 11470]	8050882.21	14.74	Maximum number of iterations	uniform	normal
567	100_it_936_945_step	[8477, 8472, 8473, 8476]	7877227.30	936.00	100	100	[53, 48, 49, 56212]	8507115.25	12.52	Maximum number of iterations	pseudorandom_5	normal
568	100_it_936_945_step	[8430, 10537, 16860, 27397]	8401544.14	944.00	100	100	[878, 153, 812, 54773]	8503140.90	11.66	Maximum number of iterations	minimal_1_8430	normal
569	5000_it_steps_936_939	[8430, 8430, 8430, 8430]	7865580.14	936.00	5000	5000	[6, 6, 6, 56166]	8507422.61	724.79	Maximum number of iterations	most_probable_scenario	normal
570	100_it_940_945_step	[4089, 5111, 8178, 13289]	7646794.56	940.00	100	100	[329, 411, 658, 54649]	8504437.82	11.99	Maximum number of iterations	minimal_3*3_4089	normal
571	100_it_all_x	[8467, 8468, 8469, 8470]	7875668.58	10.00	100	100	[8467, 8468, 8469, 9470]	7939711.41	23.17	Maximum number of iterations	uniform	normal
572	100_it_steps_based_on_915	[8430, 8430, 8430, 8430]	7865580.14	921.00	100	100	[141, 141, 141, 55401]	8506449.65	27.62	Maximum number of iterations	most_probable_scenario	normal
573	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	927.00	100	100	[124, 124, 124, 55744]	8506649.29	28.27	Maximum number of iterations	average_demand	normal
574	100_it_940_945_step	[8475, 8458, 8470, 8472]	7875731.04	940.00	100	100	[15, 938, 10, 55472]	8505584.63	14.06	Maximum number of iterations	hybrid_demand_probabilistic	normal
575	1000_it_steps_936_939	[8430, 8430, 8430, 8430]	7865580.14	936.00	1000	1000	[6, 6, 6, 56166]	8507422.61	151.25	Maximum number of iterations	most_probable_scenario	normal
576	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	60.00	100	100	[8477, 8472, 8473, 14476]	8185327.01	14.70	Maximum number of iterations	pseudorandom_5	normal
577	100_it_steps_based_on_915	[9389, 8487, 7744, 8099]	7864039.05	933.00	100	100	[59, 90, 280, 55682]	8506540.77	27.82	Maximum number of iterations	cost_sensitive	normal
578	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	100.00	100	100	[4089, 5111, 8178, 23289]	8235094.56	15.55	Maximum number of iterations	minimal_3*3_4089	normal
579	100_it_steps_based_on_900	[9389, 8487, 7744, 8099]	7864039.05	900.00	100	100	[389, 387, 544, 54899]	8504595.01	20.94	Maximum number of iterations	cost_sensitive	normal
580	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	115.00	100	100	[72, 10583, 15669, 29357]	8453185.43	14.44	Maximum number of iterations	minimal_2_8467	normal
581	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	30.00	100	100	[4363, 1703, 2726, 4429]	4110026.60	14.51	Maximum number of iterations	minimal_3_1363	normal
582	100_it_steps_based_on_915	[8430, 10537, 16860, 27397]	8401544.14	921.00	100	100	[141, 406, 282, 55027]	8505656.40	25.54	Maximum number of iterations	minimal_1_8430	normal
583	100_it_all_x	[266, 266, 266, 266]	5601.25	10.00	100	100	[1266, 266, 266, 266]	348260.44	23.07	Maximum number of iterations	higher_demand	normal
584	100_it_all_x	[4089, 5111, 8178, 13289]	7646794.56	10.00	100	100	[4089, 5111, 8178, 14289]	7732828.54	22.92	Maximum number of iterations	minimal_3*3_4089	normal
585	100_it_all_x	[8467, 8468, 8469, 8470]	7875668.58	16.00	100	100	[8467, 8468, 8469, 10070]	7975256.09	1434.03	Maximum number of iterations	uniform	normal
586	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	100.00	100	100	[8477, 8472, 8473, 18476]	8311357.50	14.79	Maximum number of iterations	pseudorandom_5	normal
587	100_it_940_945_step	[8430, 8430, 8430, 8430]	7865580.14	945.00	100	100	[870, 870, 870, 53790]	8501765.82	12.41	Maximum number of iterations	most_probable_scenario	normal
588	100_it_steps_lower_100	[8430, 10537, 16860, 27397]	8401544.14	30.00	100	100	[5430, 10537, 16860, 27397]	8428104.19	14.92	Maximum number of iterations	minimal_1_8430	normal
589	100_it_more_600	[8430, 10537, 16860, 27397]	8401544.14	1000.00	100	100	[430, 537, 860, 54397]	8503531.20	11.53	Maximum number of iterations	minimal_1_8430	normal
590	100_it_steps_based_on_900	[9389, 8487, 7744, 8099]	7864039.05	945.00	100	100	[884, 927, 184, 54404]	8503092.04	57.17	Maximum number of iterations	cost_sensitive	normal
591	100_it_steps_based_on_500	[8467, 10583, 16934, 27517]	8398967.62	560.00	100	100	[67, 3863, 134, 51597]	8499434.06	24.16	Maximum number of iterations	minimal_2_8467	normal
592	100_it_steps_based_on_500	[4089, 5111, 8178, 13289]	7646794.56	575.00	100	100	[64, 1086, 128, 54689]	8504925.01	21.36	Maximum number of iterations	minimal_3*3_4089	normal
593	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	60.00	100	100	[2726, 3407, 5452, 14859]	7196729.58	14.89	Maximum number of iterations	minimal_3*2_2726	normal
594	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	12.00	100	100	[8467, 8467, 8467, 9667]	7951461.77	23.10	Maximum number of iterations	weighted_by_scenario_prob	normal
595	100_it_steps_based_on_936	[8430, 10537, 16860, 27397]	8401544.14	938.00	100	100	[926, 219, 914, 54599]	8502652.59	17.75	Maximum number of iterations	minimal_1_8430	normal
596	100_it_940_945_step	[2726, 3407, 5452, 8859]	6130430.30	942.00	100	100	[842, 581, 742, 54075]	8502677.17	12.15	Maximum number of iterations	minimal_3*2_2726	normal
597	100_it_all_x	[1363, 1703, 2726, 4429]	3120307.78	18.00	100	100	[3163, 1703, 2726, 4429]	3719591.95	23.07	Maximum number of iterations	minimal_3_1363	normal
598	100_it_steps_based_on_500	[9389, 8487, 7744, 8099]	7864039.05	530.00	100	100	[379, 8487, 1384, 45729]	8487337.25	22.39	Maximum number of iterations	cost_sensitive	normal
599	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	60.00	100	100	[9389, 8487, 7744, 14099]	8177231.12	15.22	Maximum number of iterations	cost_sensitive	normal
600	100_it_steps_based_on_900	[1363, 1703, 2726, 4429]	3120307.78	975.00	100	100	[388, 728, 776, 54154]	8503434.15	19.71	Maximum number of iterations	minimal_3_1363	normal
601	100_it_steps_based_on_500	[8430, 8430, 8430, 8430]	7865580.14	515.00	100	100	[190, 8430, 1735, 44995]	8486579.04	22.29	Maximum number of iterations	most_probable_scenario	normal
602	100_it_steps_based_on_900	[8477, 8472, 8473, 8476]	7877227.30	915.00	100	100	[242, 237, 238, 55141]	8505821.81	19.57	Maximum number of iterations	pseudorandom_5	normal
603	100_it_940_945_step	[1363, 1703, 2726, 4429]	3120307.78	945.00	100	100	[418, 758, 836, 54514]	8503127.14	12.82	Maximum number of iterations	minimal_3_1363	normal
604	100_it_940_945_step	[9389, 8487, 7744, 8099]	7864039.05	943.00	100	100	[902, 0, 200, 55249]	8504781.86	12.46	Maximum number of iterations	cost_sensitive	normal
605	100_it_940_945_step	[8430, 8430, 8430, 8430]	7865580.14	943.00	100	100	[886, 886, 886, 53694]	8501671.11	12.39	Maximum number of iterations	most_probable_scenario	normal
606	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	921.00	100	100	[178, 178, 178, 55438]	8506265.33	27.80	Maximum number of iterations	weighted_by_scenario_prob	normal
607	100_it_steps_based_on_500	[8475, 8458, 8470, 8472]	7875731.04	515.00	100	100	[235, 8458, 1775, 45037]	8486524.73	22.44	Maximum number of iterations	hybrid_demand_probabilistic	normal
608	100_it_steps_based_on_500	[8467, 10583, 16934, 27517]	8398967.62	575.00	100	100	[417, 2533, 259, 52242]	8500625.55	19.57	Maximum number of iterations	minimal_2_8467	normal
609	100_it_900_step	[2726, 3407, 5452, 8859]	6130430.30	925.00	100	100	[876, 632, 827, 54184]	8502255.32	12.27	Maximum number of iterations	minimal_3*2_2726	normal
610	100_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	16.00	100	100	[6830, 10537, 16860, 27397]	8416803.12	22.56	Maximum number of iterations	minimal_1_8430	normal
611	100_it_900_step	[8467, 8468, 8469, 8470]	7875668.58	940.00	100	100	[7, 8, 9, 56410]	8507369.54	956.05	Maximum number of iterations	uniform	normal
612	100_it_steps_based_on_900	[8430, 8430, 8430, 8430]	7865580.14	915.00	100	100	[195, 195, 195, 56010]	8506079.01	26.18	Maximum number of iterations	most_probable_scenario	normal
613	100_it_steps_based_on_936	[9389, 8487, 7744, 8099]	7864039.05	938.00	100	100	[9, 45, 240, 55937]	8506839.20	20.15	Maximum number of iterations	cost_sensitive	normal
614	100_it_steps_based_on_915	[9389, 8487, 7744, 8099]	7864039.05	918.00	100	100	[209, 225, 400, 54917]	8505524.33	28.15	Maximum number of iterations	cost_sensitive	normal
615	100_it_steps_based_on_500	[4089, 5111, 8178, 13289]	7646794.56	500.00	100	100	[89, 4611, 178, 50789]	8497858.81	22.15	Maximum number of iterations	minimal_3*3_4089	normal
616	100_it_steps_lower_100	[9389, 8487, 7744, 8099]	7864039.05	45.00	100	100	[9389, 8487, 7744, 12599]	8114035.77	69.33	Maximum number of iterations	cost_sensitive	normal
617	100_it_all_x	[2726, 3407, 5452, 8859]	6130430.30	20.00	100	100	[2726, 3407, 5452, 10859]	6549888.93	23.30	Maximum number of iterations	minimal_3*2_2726	normal
618	100_it_all_x	[8467, 10583, 16934, 27517]	8398967.62	18.00	100	100	[6667, 10583, 16934, 27517]	8416436.94	23.60	Maximum number of iterations	minimal_2_8467	normal
619	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	915.00	100	100	[232, 232, 232, 55132]	8505855.51	4243.50	Maximum number of iterations	average_demand	normal
620	1000_it_940_step	[8430, 8430, 8430, 8430]	7865580.14	940.00	1000	1000	[910, 910, 910, 53550]	8501521.93	97.52	Maximum number of iterations	most_probable_scenario	normal
621	100_it_all_x	[266, 266, 266, 266]	5601.25	18.00	100	100	[2066, 266, 266, 266]	622337.70	817.77	Maximum number of iterations	higher_demand	normal
622	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	75.00	100	100	[967, 10583, 16934, 27517]	8448487.79	1933.43	Maximum number of iterations	minimal_2_8467	normal
623	100_it_900_step	[8477, 8472, 8473, 8476]	7877227.30	935.00	100	100	[62, 57, 58, 56161]	8507061.57	2042.84	Maximum number of iterations	pseudorandom_5	normal
624	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	942.00	100	100	[931, 931, 931, 53683]	8501346.18	12.25	Maximum number of iterations	weighted_by_scenario_prob	normal
625	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	115.00	100	100	[72, 10583, 15669, 29357]	8453185.43	14.50	Maximum number of iterations	minimal_2_8467	normal
626	100_it_940_945_step	[4089, 5111, 8178, 13289]	7646794.56	941.00	100	100	[325, 406, 650, 54693]	8504479.72	11.92	Maximum number of iterations	minimal_3*3_4089	normal
627	100_it_steps_based_on_900	[4089, 5111, 8178, 13289]	7646794.56	960.00	100	100	[249, 311, 498, 55529]	8505083.12	51.88	Maximum number of iterations	minimal_3*3_4089	normal
628	100_it_steps_based_on_500	[8467, 8468, 8469, 8470]	7875668.58	575.00	100	100	[417, 6743, 419, 48145]	8492486.07	22.41	Maximum number of iterations	uniform	normal
629	100_it_steps_based_on_900	[1363, 1703, 2726, 4429]	3120307.78	945.00	100	100	[418, 758, 836, 54514]	8503127.14	19.71	Maximum number of iterations	minimal_3_1363	normal
630	100_it_940_945_step	[8475, 8458, 8470, 8472]	7875731.04	944.00	100	100	[923, 906, 918, 53784]	8501420.32	12.36	Maximum number of iterations	hybrid_demand_probabilistic	normal
631	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	30.00	100	100	[5467, 10583, 16934, 27517]	8426342.64	14.85	Maximum number of iterations	minimal_2_8467	normal
632	100_it_936_945_step	[9389, 8487, 7744, 8099]	7864039.05	936.00	100	100	[29, 63, 256, 55835]	8506721.57	12.59	Maximum number of iterations	cost_sensitive	normal
633	100_it_steps_lower_100	[8467, 10583, 16934, 27517]	8398967.62	60.00	100	100	[2467, 10583, 16934, 27517]	8444192.76	14.85	Maximum number of iterations	minimal_2_8467	normal
634	100_it_900_step	[8477, 8472, 8473, 8476]	7877227.30	930.00	100	100	[107, 102, 103, 55906]	8506781.48	971.80	Maximum number of iterations	pseudorandom_5	normal
635	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	924.00	100	100	[151, 151, 151, 55591]	8506462.37	27.64	Maximum number of iterations	weighted_by_scenario_prob	normal
636	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	75.00	100	100	[8475, 8458, 8470, 15972]	8238350.95	14.97	Maximum number of iterations	hybrid_demand_probabilistic	normal
637	100_it_steps_based_on_936	[8430, 10537, 16860, 27397]	8401544.14	939.00	100	100	[918, 208, 897, 54628]	8502734.24	17.72	Maximum number of iterations	minimal_1_8430	normal
638	100_it_steps_based_on_915	[2726, 3407, 5452, 8859]	6130430.30	918.00	100	100	[890, 653, 862, 53841]	8502164.00	28930.70	Maximum number of iterations	minimal_3*2_2726	normal
639	100_it_steps_based_on_915	[8430, 10537, 16860, 27397]	8401544.14	924.00	100	100	[114, 373, 228, 55117]	8505891.75	25.71	Maximum number of iterations	minimal_1_8430	normal
640	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	900.00	100	100	[367, 367, 367, 55267]	8505050.29	39.69	Maximum number of iterations	weighted_by_scenario_prob	normal
641	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	927.00	100	100	[124, 124, 124, 55744]	8506649.29	27.66	Maximum number of iterations	weighted_by_scenario_prob	normal
642	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	918.00	100	100	[205, 205, 205, 55285]	8506063.22	28.30	Maximum number of iterations	average_demand	normal
643	100_it_steps_based_on_500	[8430, 10537, 16860, 27397]	8401544.14	545.00	100	100	[255, 3997, 510, 50832]	8497837.62	87.69	Maximum number of iterations	minimal_1_8430	normal
644	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	45.00	100	100	[8430, 8430, 8430, 12930]	8115567.60	2622.80	Maximum number of iterations	most_probable_scenario	normal
645	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	30.00	100	100	[8467, 8467, 8467, 11467]	8050584.36	2987.36	Maximum number of iterations	weighted_by_scenario_prob	normal
646	100_it_steps_based_on_936	[8467, 8467, 8467, 8467]	7875273.42	939.00	100	100	[16, 16, 16, 56356]	8507326.77	20.27	Maximum number of iterations	weighted_by_scenario_prob	normal
647	100_it_steps_based_on_915	[8467, 8468, 8469, 8470]	7875668.58	927.00	100	100	[124, 125, 126, 55747]	8506643.55	27.54	Maximum number of iterations	uniform	normal
648	100_it_steps_based_on_500	[8430, 8430, 8430, 8430]	7865580.14	560.00	100	100	[30, 8430, 30, 47630]	8491274.87	22.35	Maximum number of iterations	most_probable_scenario	normal
649	100_it_steps_based_on_900	[4089, 5111, 8178, 13289]	7646794.56	900.00	100	100	[489, 611, 78, 54689]	8504839.32	55.46	Maximum number of iterations	minimal_3*3_4089	normal
650	100_it_steps_based_on_915	[8467, 10583, 16934, 27517]	8398967.62	921.00	100	100	[178, 452, 356, 55147]	8505395.67	25.80	Maximum number of iterations	minimal_2_8467	normal
651	100_it_steps_based_on_500	[1363, 1703, 2726, 4429]	3120307.78	560.00	100	100	[803, 1703, 2726, 49789]	8495337.83	23.01	Maximum number of iterations	minimal_3_1363	normal
652	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	100.00	100	100	[2726, 3407, 5452, 18859]	7640348.02	14.80	Maximum number of iterations	minimal_3*2_2726	normal
653	100_it_all_x	[8467, 8468, 8469, 8470]	7875668.58	12.00	100	100	[8467, 8468, 8469, 9670]	7951813.96	22.99	Maximum number of iterations	uniform	normal
654	multi_change	[8430, 8430, 8430, 8430]	7865580.14	936.00	100	100	[6, 6, 6, 56166]	8507422.61	120.53	Maximum number of iterations	most_probable_scenario	normal
655	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	60.00	100	100	[8467, 8467, 8467, 14467]	8184223.00	490.44	Maximum number of iterations	average_demand	normal
656	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	75.00	100	100	[8430, 8430, 8430, 15930]	8233434.96	15.55	Maximum number of iterations	most_probable_scenario	normal
657	100_it_940_945_step	[8475, 8458, 8470, 8472]	7875731.04	941.00	100	100	[6, 930, 1, 55522]	8505633.59	14.14	Maximum number of iterations	hybrid_demand_probabilistic	normal
658	100_it_steps_based_on_900	[2726, 3407, 5452, 8859]	6130430.30	900.00	100	100	[26, 707, 52, 55659]	8505902.46	58.42	Maximum number of iterations	minimal_3*2_2726	normal
659	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	944.00	100	100	[915, 915, 915, 53779]	8501432.33	12.26	Maximum number of iterations	weighted_by_scenario_prob	normal
660	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	18.00	100	100	[8467, 8467, 8467, 10267]	7986288.32	23.01	Maximum number of iterations	weighted_by_scenario_prob	normal
661	100_it_all_x	[8475, 8458, 8470, 8472]	7875731.04	12.00	100	100	[8475, 8458, 8470, 9672]	7951869.19	23.56	Maximum number of iterations	hybrid_demand_probabilistic	normal
662	100_it_steps_based_on_500	[8477, 8472, 8473, 8476]	7877227.30	500.00	100	100	[477, 8472, 2473, 44476]	8484739.00	22.62	Maximum number of iterations	pseudorandom_5	normal
663	100_it_940_945_step	[8467, 10583, 16934, 27517]	8398967.62	940.00	100	100	[7, 243, 14, 55717]	8506922.35	11.50	Maximum number of iterations	minimal_2_8467	normal
664	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	115.00	100	100	[4089, 5111, 8178, 24789]	8284525.92	15.69	Maximum number of iterations	minimal_3*3_4089	normal
665	100_it_steps_based_on_936	[8467, 8467, 8467, 8467]	7875273.42	937.00	100	100	[34, 34, 34, 56254]	8507222.39	20.17	Maximum number of iterations	average_demand	normal
666	100_it_steps_based_on_915	[2726, 3407, 5452, 8859]	6130430.30	936.00	100	100	[854, 599, 772, 53787]	8502516.73	25.90	Maximum number of iterations	minimal_3*2_2726	normal
667	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	100.00	100	100	[8475, 8458, 8470, 18472]	8310827.21	148.90	Maximum number of iterations	hybrid_demand_probabilistic	normal
668	1000_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	14.00	1000	1000	[2, 10537, 14522, 30631]	8455927.57	2104.49	Maximum number of iterations	minimal_1_8430	normal
669	100_it_all_x	[8430, 10537, 16860, 27397]	8401544.14	12.00	100	100	[7230, 10537, 16860, 27397]	8413204.22	34.51	Maximum number of iterations	minimal_1_8430	normal
670	100_it_steps_based_on_915	[9389, 8487, 7744, 8099]	7864039.05	939.00	100	100	[938, 36, 232, 55049]	8504566.23	27.58	Maximum number of iterations	cost_sensitive	normal
671	100_it_940_945_step	[8467, 8468, 8469, 8470]	7875668.58	944.00	100	100	[915, 916, 917, 53782]	8501423.71	12.36	Maximum number of iterations	uniform	normal
672	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	45.00	100	100	[8477, 8472, 8473, 12976]	8123189.21	14.94	Maximum number of iterations	pseudorandom_5	normal
673	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	943.00	100	100	[923, 923, 923, 53731]	8501389.75	12.36	Maximum number of iterations	weighted_by_scenario_prob	normal
674	100_it_steps_based_on_915	[8475, 8458, 8470, 8472]	7875731.04	933.00	100	100	[78, 61, 73, 56055]	8506992.31	27.83	Maximum number of iterations	hybrid_demand_probabilistic	normal
675	100_it_steps_based_on_936	[8467, 8467, 8467, 8467]	7875273.42	937.00	100	100	[34, 34, 34, 56254]	8507222.39	20.08	Maximum number of iterations	weighted_by_scenario_prob	normal
676	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	560.00	100	100	[67, 7907, 67, 47107]	8491188.12	22.00	Maximum number of iterations	weighted_by_scenario_prob	normal
677	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	100.00	100	100	[8430, 8430, 8430, 18430]	8307210.00	14.70	Maximum number of iterations	most_probable_scenario	normal
678	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	100.00	100	100	[2726, 3407, 5452, 18859]	7640348.02	15.60	Maximum number of iterations	minimal_3*2_2726	normal
679	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	100.00	100	100	[6863, 1703, 2726, 8929]	6081723.19	15.04	Maximum number of iterations	minimal_3_1363	normal
680	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	942.00	100	100	[931, 931, 931, 53683]	8501346.18	12.39	Maximum number of iterations	weighted_by_scenario_prob	normal
681	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	933.00	100	100	[70, 70, 70, 56050]	8507002.21	38.23	Maximum number of iterations	average_demand	normal
682	1000_it_steps_936_939	[8467, 8467, 8467, 8467]	7875273.42	936.00	1000	1000	[43, 43, 43, 56203]	8507168.39	319.45	Maximum number of iterations	average_demand	normal
683	100_it_steps_based_on_900	[8477, 8472, 8473, 8476]	7877227.30	945.00	100	100	[917, 912, 913, 53836]	8501414.10	19.95	Maximum number of iterations	pseudorandom_5	normal
684	100_it_900_step	[4089, 5111, 8178, 13289]	7646794.56	940.00	100	100	[329, 411, 658, 54649]	8504437.82	12.14	Maximum number of iterations	minimal_3*3_4089	normal
685	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	30.00	100	100	[2726, 3407, 5452, 11859]	6734029.53	920.24	Maximum number of iterations	minimal_3*2_2726	normal
686	100_it_steps_based_on_936	[8467, 8467, 8467, 8467]	7875273.42	936.00	100	100	[43, 43, 43, 56203]	8507168.39	20.08	Maximum number of iterations	average_demand	normal
687	100_it_936_945_step	[8467, 8467, 8467, 8467]	7875273.42	936.00	100	100	[43, 43, 43, 56203]	8507168.39	12.41	Maximum number of iterations	average_demand	normal
688	100_it_steps_based_on_915	[8477, 8472, 8473, 8476]	7877227.30	924.00	100	100	[161, 156, 157, 55600]	8506420.28	27.83	Maximum number of iterations	pseudorandom_5	normal
689	100_it_steps_based_on_900	[8430, 8430, 8430, 8430]	7865580.14	945.00	100	100	[870, 870, 870, 53790]	8501765.82	19.35	Maximum number of iterations	most_probable_scenario	normal
690	100_it_steps_based_on_915	[8477, 8472, 8473, 8476]	7877227.30	930.00	100	100	[107, 102, 103, 55906]	8506781.48	3023.17	Maximum number of iterations	pseudorandom_5	normal
691	100_it_steps_based_on_900	[8467, 8467, 8467, 8467]	7875273.42	915.00	100	100	[232, 232, 232, 55132]	8505855.51	21.29	Maximum number of iterations	weighted_by_scenario_prob	normal
692	100_it_900_step	[8475, 8458, 8470, 8472]	7875731.04	920.00	100	100	[195, 178, 190, 55392]	8506191.65	1320.01	Maximum number of iterations	hybrid_demand_probabilistic	normal
693	100_it_steps_based_on_936	[8477, 8472, 8473, 8476]	7877227.30	936.00	100	100	[53, 48, 49, 56212]	8507115.25	20.22	Maximum number of iterations	pseudorandom_5	normal
694	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	930.00	100	100	[97, 97, 97, 55897]	8506828.77	30.09	Maximum number of iterations	weighted_by_scenario_prob	normal
695	100_it_steps_based_on_915	[8467, 10583, 16934, 27517]	8398967.62	927.00	100	100	[124, 386, 248, 55327]	8505881.43	25.36	Maximum number of iterations	minimal_2_8467	normal
696	100_it_936_945_step	[4089, 5111, 8178, 13289]	7646794.56	936.00	100	100	[345, 431, 690, 54473]	8504257.61	11.81	Maximum number of iterations	minimal_3*3_4089	normal
697	100_it_steps_based_on_900	[8467, 8468, 8469, 8470]	7875668.58	930.00	100	100	[97, 98, 99, 55900]	8506822.61	20.66	Maximum number of iterations	uniform	normal
698	100_it_940_945_step	[8467, 8467, 8467, 8467]	7875273.42	943.00	100	100	[923, 923, 923, 53731]	8501389.75	12.38	Maximum number of iterations	average_demand	normal
699	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	14.00	100	100	[8467, 8467, 8467, 9867]	7963322.67	22.42	Maximum number of iterations	average_demand	normal
700	100_it_steps_based_on_500	[8467, 8468, 8469, 8470]	7875668.58	515.00	100	100	[227, 8468, 1774, 45035]	8486526.67	22.53	Maximum number of iterations	uniform	normal
701	100_it_steps_based_on_900	[8430, 10537, 16860, 27397]	8401544.14	960.00	100	100	[750, 937, 540, 54277]	8502609.36	18.93	Maximum number of iterations	minimal_1_8430	normal
702	1000_it_940_step	[8477, 8472, 8473, 8476]	7877227.30	940.00	1000	1000	[17, 12, 13, 56416]	8507320.52	97.39	Maximum number of iterations	pseudorandom_5	normal
703	100_it_steps_based_on_915	[8467, 10583, 16934, 27517]	8398967.62	933.00	100	100	[70, 320, 140, 55507]	8506364.31	25.24	Maximum number of iterations	minimal_2_8467	normal
704	100_it_steps_based_on_500	[8475, 8458, 8470, 8472]	7875731.04	545.00	100	100	[300, 8458, 295, 46622]	8489721.80	23.60	Maximum number of iterations	hybrid_demand_probabilistic	normal
705	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	30.00	100	100	[8467, 8467, 8467, 11467]	8050584.36	14.73	Maximum number of iterations	average_demand	normal
706	100_it_steps_based_on_500	[8430, 8430, 8430, 8430]	7865580.14	545.00	100	100	[255, 8430, 255, 46580]	8489813.22	22.12	Maximum number of iterations	most_probable_scenario	normal
707	100_it_940_945_step	[8477, 8472, 8473, 8476]	7877227.30	945.00	100	100	[917, 912, 913, 53836]	8501414.10	13.72	Maximum number of iterations	pseudorandom_5	normal
708	100_it_936_945_step	[8430, 8430, 8430, 8430]	7865580.14	939.00	100	100	[918, 918, 918, 53502]	8501470.79	12.46	Maximum number of iterations	most_probable_scenario	normal
709	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	100.00	100	100	[8467, 8467, 8467, 18467]	8310663.26	1083.48	Maximum number of iterations	average_demand	normal
710	100_it_steps_lower_100	[2726, 3407, 5452, 8859]	6130430.30	60.00	100	100	[2726, 3407, 5452, 14859]	7196729.58	15.48	Maximum number of iterations	minimal_3*2_2726	normal
711	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	75.00	100	100	[6838, 1703, 2726, 6454]	5454892.97	14.65	Maximum number of iterations	minimal_3_1363	normal
712	100_it_940_945_step	[8467, 8468, 8469, 8470]	7875668.58	945.00	100	100	[907, 908, 909, 53830]	8501465.96	12.41	Maximum number of iterations	uniform	normal
713	100_it_steps_based_on_915	[8475, 8458, 8470, 8472]	7875731.04	915.00	100	100	[240, 223, 235, 55137]	8505849.68	27.47	Maximum number of iterations	hybrid_demand_probabilistic	normal
714	100_it_all_x	[8467, 8467, 8467, 8467]	7875273.42	20.00	100	100	[8467, 8467, 8467, 10467]	7997464.10	22.86	Maximum number of iterations	weighted_by_scenario_prob	normal
715	100_it_all_x	[8477, 8472, 8473, 8476]	7877227.30	18.00	100	100	[8477, 8472, 8473, 10276]	7987921.92	23.68	Maximum number of iterations	pseudorandom_5	normal
716	5000_it_940_step	[8467, 8467, 8467, 8467]	7875273.42	940.00	5000	5000	[7, 7, 7, 56407]	8507377.71	2050.57	Maximum number of iterations	weighted_by_scenario_prob	normal
717	100_it_900_step	[8467, 8468, 8469, 8470]	7875668.58	925.00	100	100	[142, 143, 144, 55645]	8506520.16	2350.82	Maximum number of iterations	uniform	normal
718	100_it_steps_based_on_500	[8475, 8458, 8470, 8472]	7875731.04	500.00	100	100	[475, 8458, 2470, 44472]	8484763.40	22.86	Maximum number of iterations	hybrid_demand_probabilistic	normal
719	100_it_steps_lower_100	[4089, 5111, 8178, 13289]	7646794.56	30.00	100	100	[4089, 5111, 8178, 16289]	7882966.26	15.11	Maximum number of iterations	minimal_3*3_4089	normal
720	100_it_all_x	[9389, 8487, 7744, 8099]	7864039.05	18.00	100	100	[9389, 8487, 7744, 9899]	7976623.84	22.87	Maximum number of iterations	cost_sensitive	normal
721	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	545.00	100	100	[292, 8467, 292, 46617]	8489724.56	25.04	Maximum number of iterations	average_demand	normal
722	100_it_all_x	[4089, 5111, 8178, 13289]	7646794.56	14.00	100	100	[4089, 5111, 8178, 14689]	7765056.86	22.75	Maximum number of iterations	minimal_3*3_4089	normal
723	100_it_steps_based_on_915	[8467, 8467, 8467, 8467]	7875273.42	936.00	100	100	[43, 43, 43, 56203]	8507168.39	28.01	Maximum number of iterations	weighted_by_scenario_prob	normal
724	100_it_steps_lower_100	[8475, 8458, 8470, 8472]	7875731.04	60.00	100	100	[8475, 8458, 8470, 14472]	8184482.26	14.69	Maximum number of iterations	hybrid_demand_probabilistic	normal
725	100_it_steps_based_on_900	[8467, 10583, 16934, 27517]	8398967.62	960.00	100	100	[787, 23, 614, 54397]	8504045.12	18.16	Maximum number of iterations	minimal_2_8467	normal
726	100_it_steps_based_on_936	[8467, 10583, 16934, 27517]	8398967.62	936.00	100	100	[43, 287, 86, 55597]	8506604.08	18.52	Maximum number of iterations	minimal_2_8467	normal
727	100_it_900_step	[8430, 10537, 16860, 27397]	8401544.14	925.00	100	100	[105, 362, 210, 55147]	8505969.93	11.51	Maximum number of iterations	minimal_1_8430	normal
728	100_it_all_x	[2726, 3407, 5452, 8859]	6130430.30	16.00	100	100	[2726, 3407, 5452, 10459]	6471377.19	23.08	Maximum number of iterations	minimal_3*2_2726	normal
729	100_it_steps_lower_100	[8467, 8468, 8469, 8470]	7875668.58	60.00	100	100	[8467, 8468, 8469, 14470]	8184448.13	14.60	Maximum number of iterations	uniform	normal
730	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	115.00	100	100	[6883, 1703, 2726, 10409]	6407258.43	14.93	Maximum number of iterations	minimal_3_1363	normal
731	100_it_940_945_step	[8475, 8458, 8470, 8472]	7875731.04	943.00	100	100	[931, 914, 926, 53736]	8501377.85	12.48	Maximum number of iterations	hybrid_demand_probabilistic	normal
732	100_it_steps_based_on_500	[2726, 3407, 5452, 8859]	6130430.30	530.00	100	100	[76, 2347, 152, 52849]	8502039.09	22.64	Maximum number of iterations	minimal_3*2_2726	normal
733	100_it_steps_based_on_500	[2726, 3407, 5452, 8859]	6130430.30	560.00	100	100	[486, 47, 412, 54219]	8504528.32	403.04	Maximum number of iterations	minimal_3*2_2726	normal
734	100_it_steps_lower_100	[8467, 8467, 8467, 8467]	7875273.42	30.00	100	100	[8467, 8467, 8467, 11467]	8050584.36	14.72	Maximum number of iterations	weighted_by_scenario_prob	normal
735	100_it_steps_based_on_900	[9389, 8487, 7744, 8099]	7864039.05	915.00	100	100	[239, 252, 424, 55679]	8505373.48	70.15	Maximum number of iterations	cost_sensitive	normal
736	100_it_steps_based_on_500	[8467, 8467, 8467, 8467]	7875273.42	530.00	100	100	[517, 8467, 517, 45567]	8487869.58	23.23	Maximum number of iterations	average_demand	normal
737	100_it_steps_lower_100	[8430, 8430, 8430, 8430]	7865580.14	60.00	100	100	[8430, 8430, 8430, 14430]	8178739.21	14.70	Maximum number of iterations	most_probable_scenario	normal
738	100_it_steps_lower_100	[8477, 8472, 8473, 8476]	7877227.30	75.00	100	100	[8477, 8472, 8473, 15976]	8239072.04	14.72	Maximum number of iterations	pseudorandom_5	normal
739	100_it_940_945_step	[8477, 8472, 8473, 8476]	7877227.30	942.00	100	100	[941, 936, 937, 53692]	8501288.27	911.25	Maximum number of iterations	pseudorandom_5	normal
740	100_it_940_945_step	[8475, 8458, 8470, 8472]	7875731.04	945.00	100	100	[915, 898, 910, 53832]	8501462.56	12.33	Maximum number of iterations	hybrid_demand_probabilistic	normal
741	100_it_steps_based_on_500	[8467, 8468, 8469, 8470]	7875668.58	500.00	100	100	[467, 8468, 2469, 44470]	8484765.84	22.71	Maximum number of iterations	uniform	normal
742	100_it_steps_lower_100	[1363, 1703, 2726, 4429]	3120307.78	75.00	100	100	[6838, 1703, 2726, 6454]	5454892.97	15.05	Maximum number of iterations	minimal_3_1363	normal
743	100_it_940_945_step	[9389, 8487, 7744, 8099]	7864039.05	942.00	100	100	[911, 9, 208, 55199]	8504729.04	12.52	Maximum number of iterations	cost_sensitive	normal
744	100_it_steps_based_on_900	[2726, 3407, 5452, 8859]	6130430.30	975.00	100	100	[776, 482, 577, 54684]	8503321.83	18.29	Maximum number of iterations	minimal_3*2_2726	normal
745	100_it_all_x	[8467, 10583, 16934, 27517]	8398967.62	16.00	100	100	[6867, 10583, 16934, 27517]	8414640.64	23.77	Maximum number of iterations	minimal_2_8467	normal
746	100_it_940_945_step	[8430, 10537, 16860, 27397]	8401544.14	940.00	100	100	[910, 197, 880, 54657]	8502815.77	11.48	Maximum number of iterations	minimal_1_8430	normal
747	100_it_steps_based_on_915	[8475, 8458, 8470, 8472]	7875731.04	927.00	100	100	[132, 115, 127, 55749]	8506640.61	27.70	Maximum number of iterations	hybrid_demand_probabilistic	normal
748	100_it_all_x	[1363, 1703, 2726, 4429]	3120307.78	14.00	100	100	[2763, 1703, 2726, 4429]	3587581.48	23.53	Maximum number of iterations	minimal_3_1363	normal
\.

COPY public.experimento_random_restart (id, modelo, experimento, x_inicial, obj_inicial, step, cant_iteraciones, iteracion, cant_iteraciones_sin_mejora_max, cant_iteraciones_sin_mejora, cant_reinicios_max, cant_reinicios, x_optimo, obj, tiempo, motivo_parada, estrategia, distribucion) FROM stdin;
1	RandomRestart	20_loops_10_restarts	[671, 9445, 4651, 4682]	8503643.50	936.00	50	50	10	0	10	0	[671, 85, 907, 54290]	8503643.50	106.93	Maximum number of iterations	x_random	normal
3	RandomRestart	20_loops_10_restarts	[5184, 5914, 6217, 8923]	8504356.28	936.00	50	50	10	0	10	3	[504, 298, 601, 54787]	8504356.28	603.81	Maximum number of iterations	x_random	normal
6	RandomRestart	30_loops_10_restarts	[5152, 7614, 1340, 3693]	8505184.36	936.00	50	50	10	0	10	0	[472, 126, 404, 55173]	8505184.36	119.41	Maximum number of iterations	x_random	normal
7	RandomRestart	30_loops_10_restarts	[2918, 4949, 7142, 4528]	8505397.95	936.00	50	50	10	0	10	4	[110, 269, 590, 55072]	8505397.95	603.11	Maximum number of iterations	x_random	normal
8	RandomRestart	10_loops_10_restarts	[7932, 9520, 2261, 1501]	8505135.33	936.00	50	50	10	0	10	0	[444, 160, 389, 54853]	8505135.33	301.38	Maximum number of iterations	x_random	normal
9	RandomRestart	10_loops_10_restarts	[7697, 1355, 990, 9448]	8506001.77	936.00	50	50	10	0	10	3	[209, 419, 54, 55312]	8506001.77	846.69	Maximum number of iterations	x_random	normal
10	RandomRestart	10_loops_10_restarts	[9484, 4731, 2167, 2645]	8506375.29	936.00	50	50	10	0	10	11	[124, 51, 295, 55997]	8506375.29	2261.58	Maximum number of iterations	x_random	normal
11	RandomRestart	10_loops_10_restarts	[1678, 746, 131, 8187]	8503817.24	936.00	50	50	10	0	10	0	[742, 746, 131, 54987]	8503817.24	104.41	Maximum number of iterations	x_random	normal
12	RandomRestart	10_loops_10_restarts	[2082, 9540, 2569, 1747]	8505104.96	936.00	50	50	10	0	10	0	[210, 180, 697, 55099]	8505104.96	202.45	Maximum number of iterations	x_random	normal
13	RandomRestart	10_loops_10_restarts	[3856, 6898, 225, 1446]	8506012.28	936.00	50	50	10	0	10	9	[112, 346, 225, 55734]	8506012.28	4172.81	Maximum number of iterations	x_random	normal
14	RandomRestart	10_loops_10_restarts	[1883, 1425, 6691, 1617]	8506126.55	936.00	50	50	10	0	10	17	[11, 489, 139, 55905]	8506126.55	5353.97	Maximum number of iterations	x_random	normal
15	RandomRestart	10_loops_10_restarts	[8494, 6019, 4734, 2397]	8506402.67	936.00	50	50	10	0	10	18	[70, 403, 54, 55749]	8506402.67	5543.58	Maximum number of iterations	x_random	normal
17	RandomRestart	100k_random_10_loops_10_restarts	[28786, 63279, 29700, 62015]	8487141.58	936.00	50	50	10	0	10	0	[706, 8991, 684, 46103]	8487141.58	185.15	Maximum number of iterations	x_random	normal
18	RandomRestart	100k_random_10_loops_10_restarts	[238, 21968, 13775, 95121]	8504597.19	936.00	50	50	10	7	10	7	[238, 440, 671, 54873]	8504597.19	27757.65	Maximum number of iterations	x_random	normal
19	RandomRestart	100k_random_10_loops_10_restarts	[2202, 13655, 42163, 31175]	8505467.90	936.00	50	50	10	1	10	8	[330, 551, 43, 55511]	8505467.90	27941.10	Maximum number of iterations	x_random	normal
16	RandomRestart	100k_random_10_loops_10_restarts	[1393, 91204, 7937, 76673]	8275850.39	936.00	50	50	10	8	10	0	[457, 34108, 449, 39233]	8275850.39	91.14	Maximum number of iterations	x_random	normal
5	RandomRestart	20_loops_10_restarts	[3785, 3776, 6144, 3479]	8506106.00	936.00	50	50	10	5	10	3	[41, 32, 528, 55895]	8506106.00	802.62	Maximum number of iterations	x_random	normal
4	RandomRestart	20_loops_10_restarts	[5903, 6607, 9897, 9626]	8505476.00	936.00	50	50	10	3	10	3	[287, 55, 537, 55490]	8505476.00	703.07	Maximum number of iterations	x_random	normal
2	RandomRestart	20_loops_10_restarts	[1563, 2609, 1125, 5914]	8504096.10	936.00	50	50	10	2	10	2	[627, 737, 189, 54586]	8504096.10	404.00	Maximum number of iterations	x_random	normal
\.

SELECT pg_catalog.setval('public.experimento_hill_climbing_id_seq', 748, true);

SELECT pg_catalog.setval('public.experimento_random_restart_id_seq', 19, true);

ALTER TABLE ONLY public.experimento_hill_climbing
    ADD CONSTRAINT experimento_hill_climbing_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.experimento_random_restart
    ADD CONSTRAINT experimento_random_restart_pkey PRIMARY KEY (id);
