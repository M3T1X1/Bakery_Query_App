--
-- PostgreSQL database dump
--

\restrict PTL5hVFYAuT6udZk1KgMbAtAYuNBfSxxbJRzZg0SXcCZUHo4yvTaPflASJNeCcp

-- Dumped from database version 17.6 (Debian 17.6-0+deb13u1)
-- Dumped by pg_dump version 17.6 (Debian 17.6-0+deb13u1)

-- Started on 2026-02-02 23:09:09 CET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 218 (class 1259 OID 16491)
-- Name: adresy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.adresy (
    id_adresu integer NOT NULL,
    wojewodztwo character varying(50),
    miasto character varying(100),
    ulica character varying(100),
    numer_domu_lub_mieszkania character varying(20)
);


ALTER TABLE public.adresy OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16490)
-- Name: adresy_id_adresu_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.adresy_id_adresu_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.adresy_id_adresu_seq OWNER TO postgres;

--
-- TOC entry 3496 (class 0 OID 0)
-- Dependencies: 217
-- Name: adresy_id_adresu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.adresy_id_adresu_seq OWNED BY public.adresy.id_adresu;


--
-- TOC entry 224 (class 1259 OID 16522)
-- Name: dostawcy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dostawcy (
    id_dostawcy integer NOT NULL,
    nazwa character varying(100),
    id_adresu integer
);


ALTER TABLE public.dostawcy OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16521)
-- Name: dostawcy_id_dostawcy_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dostawcy_id_dostawcy_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dostawcy_id_dostawcy_seq OWNER TO postgres;

--
-- TOC entry 3497 (class 0 OID 0)
-- Dependencies: 223
-- Name: dostawcy_id_dostawcy_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dostawcy_id_dostawcy_seq OWNED BY public.dostawcy.id_dostawcy;


--
-- TOC entry 222 (class 1259 OID 16510)
-- Name: pracownicy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pracownicy (
    id_pracownika integer NOT NULL,
    imie character varying(50),
    nazwisko character varying(50),
    id_adresu integer,
    stanowisko character varying(50),
    zarobki numeric(10,2)
);


ALTER TABLE public.pracownicy OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16509)
-- Name: pracownicy_id_pracownika_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pracownicy_id_pracownika_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pracownicy_id_pracownika_seq OWNER TO postgres;

--
-- TOC entry 3498 (class 0 OID 0)
-- Dependencies: 221
-- Name: pracownicy_id_pracownika_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pracownicy_id_pracownika_seq OWNED BY public.pracownicy.id_pracownika;


--
-- TOC entry 226 (class 1259 OID 16534)
-- Name: produkty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produkty (
    id_produktu integer NOT NULL,
    nazwa character varying(100),
    id_dostawcy integer
);


ALTER TABLE public.produkty OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16533)
-- Name: produkty_id_produktu_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produkty_id_produktu_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.produkty_id_produktu_seq OWNER TO postgres;

--
-- TOC entry 3499 (class 0 OID 0)
-- Dependencies: 225
-- Name: produkty_id_produktu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produkty_id_produktu_seq OWNED BY public.produkty.id_produktu;


--
-- TOC entry 220 (class 1259 OID 16498)
-- Name: sklepy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sklepy (
    id_sklepu integer NOT NULL,
    id_adresu integer,
    nazwa character varying(100),
    sklep_wlasnosciowy boolean
);


ALTER TABLE public.sklepy OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16497)
-- Name: sklepy_id_sklepu_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sklepy_id_sklepu_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sklepy_id_sklepu_seq OWNER TO postgres;

--
-- TOC entry 3500 (class 0 OID 0)
-- Dependencies: 219
-- Name: sklepy_id_sklepu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sklepy_id_sklepu_seq OWNED BY public.sklepy.id_sklepu;


--
-- TOC entry 230 (class 1259 OID 16558)
-- Name: transakcje; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transakcje (
    id_transakcji integer NOT NULL,
    id_wypieku integer,
    id_sklepu integer,
    ilosc integer,
    cena numeric(10,2)
);


ALTER TABLE public.transakcje OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16557)
-- Name: transakcje_id_transakcji_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transakcje_id_transakcji_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transakcje_id_transakcji_seq OWNER TO postgres;

--
-- TOC entry 3501 (class 0 OID 0)
-- Dependencies: 229
-- Name: transakcje_id_transakcji_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transakcje_id_transakcji_seq OWNED BY public.transakcje.id_transakcji;


--
-- TOC entry 228 (class 1259 OID 16546)
-- Name: wypieki; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wypieki (
    id_wypieku integer NOT NULL,
    nazwa character varying(100),
    cena_produkcji numeric(10,2),
    czas_wypiekania interval,
    id_produktu integer,
    gramatura integer
);


ALTER TABLE public.wypieki OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16545)
-- Name: wypieki_id_wypieku_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.wypieki_id_wypieku_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.wypieki_id_wypieku_seq OWNER TO postgres;

--
-- TOC entry 3502 (class 0 OID 0)
-- Dependencies: 227
-- Name: wypieki_id_wypieku_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.wypieki_id_wypieku_seq OWNED BY public.wypieki.id_wypieku;


--
-- TOC entry 3304 (class 2604 OID 16494)
-- Name: adresy id_adresu; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adresy ALTER COLUMN id_adresu SET DEFAULT nextval('public.adresy_id_adresu_seq'::regclass);


--
-- TOC entry 3307 (class 2604 OID 16525)
-- Name: dostawcy id_dostawcy; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dostawcy ALTER COLUMN id_dostawcy SET DEFAULT nextval('public.dostawcy_id_dostawcy_seq'::regclass);


--
-- TOC entry 3306 (class 2604 OID 16513)
-- Name: pracownicy id_pracownika; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pracownicy ALTER COLUMN id_pracownika SET DEFAULT nextval('public.pracownicy_id_pracownika_seq'::regclass);


--
-- TOC entry 3308 (class 2604 OID 16537)
-- Name: produkty id_produktu; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produkty ALTER COLUMN id_produktu SET DEFAULT nextval('public.produkty_id_produktu_seq'::regclass);


--
-- TOC entry 3305 (class 2604 OID 16501)
-- Name: sklepy id_sklepu; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sklepy ALTER COLUMN id_sklepu SET DEFAULT nextval('public.sklepy_id_sklepu_seq'::regclass);


--
-- TOC entry 3310 (class 2604 OID 16561)
-- Name: transakcje id_transakcji; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transakcje ALTER COLUMN id_transakcji SET DEFAULT nextval('public.transakcje_id_transakcji_seq'::regclass);


--
-- TOC entry 3309 (class 2604 OID 16549)
-- Name: wypieki id_wypieku; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wypieki ALTER COLUMN id_wypieku SET DEFAULT nextval('public.wypieki_id_wypieku_seq'::regclass);


--
-- TOC entry 3478 (class 0 OID 16491)
-- Dependencies: 218
-- Data for Name: adresy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.adresy (id_adresu, wojewodztwo, miasto, ulica, numer_domu_lub_mieszkania) FROM stdin;
1	Warmińsko - mazurskie	Bielsko-Biała	Floriana	686
2	Lubelskie	Sopot	Zakątek	65
3	Pomorskie	Sieradz	Morelowa	514
4	Świętokrzyskie	Jelenia Góra	Sowia	55/78
5	Zachodniopomorskie	Biała Podlaska	Tęczowa	85/87
\.


--
-- TOC entry 3484 (class 0 OID 16522)
-- Dependencies: 224
-- Data for Name: dostawcy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dostawcy (id_dostawcy, nazwa, id_adresu) FROM stdin;
1	PPUH Dąbrówka	2
2	Fundacja Chojak	1
3	Kusyk Sp.k.	3
4	Grupa Serwa-Sudnik Sp.j.	1
\.


--
-- TOC entry 3482 (class 0 OID 16510)
-- Dependencies: 222
-- Data for Name: pracownicy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pracownicy (id_pracownika, imie, nazwisko, id_adresu, stanowisko, zarobki) FROM stdin;
1	Szymon	Smolka	2	Sprzedawca	7137.04
2	Tymoteusz	Pal	5	Piekarz	7733.11
3	Nikodem	Osica	5	Kierownik	3590.49
4	Olgierd	Działo	5	Sprzedawca	5700.32
5	Dominik	Kościołek	3	Sprzedawca	4826.74
6	Rozalia	Jachimczak	4	Sprzedawca	4720.02
7	Nikodem	Kurzydło	4	Sprzedawca	7797.12
8	Róża	Budych	5	Kierownik	5887.50
9	Maksymilian	Siudek	2	Piekarz	4518.26
10	Aniela	Sowała	3	Piekarz	3621.62
11	Maks	Wojtaszak	3	Kierownik	5639.83
12	Artur	Dziduch	1	Piekarz	7416.63
13	Dariusz	Pakos	3	Piekarz	3910.32
14	Grzegorz	Rykała	4	Kierownik	5863.79
\.


--
-- TOC entry 3486 (class 0 OID 16534)
-- Dependencies: 226
-- Data for Name: produkty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produkty (id_produktu, nazwa, id_dostawcy) FROM stdin;
1	Mąka pszenna	1
2	Drożdże	1
3	Sól	2
4	Cukier	2
5	Ziarna słonecznika	4
6	Jaja	1
7	Mleko	2
8	Ziarna słonecznika	4
9	Ziarna słonecznika	3
10	Cukier	3
11	Jaja	3
12	Ziarna słonecznika	4
13	Mąka pszenna	2
14	Cukier	1
15	Drożdże	1
16	Mleko	4
17	Sól	2
18	Mąka pszenna	4
19	Drożdże	1
20	Mąka pszenna	3
21	Cukier	3
22	Drożdże	3
23	Mleko	4
24	Cukier	3
25	Mąka pszenna	3
26	Jaja	2
27	Ziarna słonecznika	4
28	Cukier	1
29	Jaja	1
30	Mąka pszenna	3
\.


--
-- TOC entry 3480 (class 0 OID 16498)
-- Dependencies: 220
-- Data for Name: sklepy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sklepy (id_sklepu, id_adresu, nazwa, sklep_wlasnosciowy) FROM stdin;
1	3	Piekarnia Walenciak S.A.	f
2	1	Piekarnia Gabinety Balcewicz-Sadownik Sp.k.	f
3	2	Piekarnia Strządała Sp.k.	t
4	1	Piekarnia Gabinety Reiter Sp.j.	f
5	5	Piekarnia Gabinety Wojczuk	t
\.


--
-- TOC entry 3490 (class 0 OID 16558)
-- Dependencies: 230
-- Data for Name: transakcje; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transakcje (id_transakcji, id_wypieku, id_sklepu, ilosc, cena) FROM stdin;
1	15	5	5	6.19
2	18	1	6	14.70
3	6	4	8	13.87
4	14	4	7	12.69
5	14	5	3	13.45
6	20	1	8	12.57
7	6	5	6	10.46
8	6	5	7	10.08
9	5	1	10	14.99
10	9	4	6	6.81
11	18	2	9	5.58
12	19	4	7	10.21
13	15	2	9	13.18
14	1	3	2	2.69
15	20	5	7	7.96
16	17	1	6	3.48
17	6	1	5	11.80
18	11	5	5	10.62
19	11	4	7	8.03
20	18	4	7	3.01
21	12	4	6	12.16
22	13	2	2	14.27
23	12	1	4	4.84
24	6	1	7	10.00
25	10	2	10	7.46
26	4	1	8	8.74
27	12	4	3	3.31
28	9	2	2	6.07
29	17	2	5	6.00
30	9	3	6	10.03
31	10	1	8	9.92
32	7	1	2	14.46
33	4	4	9	3.82
34	17	4	1	14.59
35	3	5	2	5.04
36	11	2	9	11.21
37	11	5	7	10.67
38	18	2	4	13.95
39	15	4	10	11.62
40	13	2	7	12.31
41	1	5	9	12.30
42	11	4	6	5.04
43	1	3	3	6.25
44	11	5	3	12.24
45	17	2	6	12.16
46	6	2	6	2.72
47	12	5	4	7.32
48	13	2	8	2.66
49	17	2	10	12.72
50	14	2	4	7.01
51	3	1	9	3.13
52	13	3	9	12.02
53	1	2	10	5.02
54	17	1	3	4.12
55	8	3	4	13.05
56	18	1	5	3.55
57	14	4	10	10.35
58	13	5	7	12.08
59	7	4	3	4.01
60	3	1	6	9.17
61	20	2	4	12.44
62	3	4	7	14.76
63	9	5	10	8.48
64	16	3	6	9.99
65	9	4	10	11.80
66	17	2	10	9.32
67	14	1	2	8.46
68	9	4	7	12.57
69	11	3	5	9.72
70	17	3	10	8.59
71	2	1	7	3.58
72	18	2	10	7.80
73	14	5	7	13.67
74	14	5	3	5.55
75	2	1	9	2.63
76	13	3	10	13.01
77	9	5	1	7.01
78	9	2	7	11.34
79	8	4	1	9.74
80	13	2	5	14.67
81	5	2	2	3.78
82	2	3	3	11.27
83	17	3	9	12.48
84	15	3	3	3.30
85	12	3	2	7.29
86	11	5	4	7.43
87	7	3	9	10.15
88	4	1	1	9.18
89	10	4	7	12.89
90	16	1	5	12.33
91	1	5	9	6.75
92	17	1	1	8.14
93	20	5	2	7.65
94	1	2	3	12.73
95	16	3	10	5.50
96	6	1	7	4.37
97	18	3	4	11.66
98	11	2	4	10.48
99	12	2	7	13.08
100	12	4	9	12.53
\.


--
-- TOC entry 3488 (class 0 OID 16546)
-- Dependencies: 228
-- Data for Name: wypieki; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wypieki (id_wypieku, nazwa, cena_produkcji, czas_wypiekania, id_produktu, gramatura) FROM stdin;
1	Pączek	1.25	00:51:00	17	500
2	Chleb żytni	3.45	00:52:00	2	50
3	Rogal maślany	2.55	01:00:00	16	50
4	Rogal maślany	3.41	00:33:00	2	500
5	Chleb żytni	1.63	00:37:00	1	500
6	Bagietka	2.95	00:48:00	5	50
7	Bułka kajzerka	4.75	00:28:00	14	100
8	Bagietka	4.05	00:44:00	23	50
9	Bułka kajzerka	1.60	00:42:00	3	50
10	Pączek	2.80	00:37:00	6	50
11	Chleb razowy	3.47	00:27:00	11	100
12	Pączek	4.05	00:49:00	13	100
13	Bułka kajzerka	2.26	00:27:00	12	50
14	Rogal maślany	3.78	00:53:00	3	500
15	Chleb żytni	1.92	00:41:00	11	50
16	Chleb żytni	3.77	00:50:00	16	100
17	Pączek	2.20	00:57:00	12	500
18	Bułka kajzerka	4.40	00:32:00	2	50
19	Chleb razowy	2.71	00:41:00	24	100
20	Chleb żytni	4.93	00:53:00	10	100
\.


--
-- TOC entry 3503 (class 0 OID 0)
-- Dependencies: 217
-- Name: adresy_id_adresu_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.adresy_id_adresu_seq', 5, true);


--
-- TOC entry 3504 (class 0 OID 0)
-- Dependencies: 223
-- Name: dostawcy_id_dostawcy_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dostawcy_id_dostawcy_seq', 4, true);


--
-- TOC entry 3505 (class 0 OID 0)
-- Dependencies: 221
-- Name: pracownicy_id_pracownika_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pracownicy_id_pracownika_seq', 16, true);


--
-- TOC entry 3506 (class 0 OID 0)
-- Dependencies: 225
-- Name: produkty_id_produktu_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produkty_id_produktu_seq', 30, true);


--
-- TOC entry 3507 (class 0 OID 0)
-- Dependencies: 219
-- Name: sklepy_id_sklepu_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sklepy_id_sklepu_seq', 5, true);


--
-- TOC entry 3508 (class 0 OID 0)
-- Dependencies: 229
-- Name: transakcje_id_transakcji_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transakcje_id_transakcji_seq', 100, true);


--
-- TOC entry 3509 (class 0 OID 0)
-- Dependencies: 227
-- Name: wypieki_id_wypieku_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.wypieki_id_wypieku_seq', 20, true);


--
-- TOC entry 3312 (class 2606 OID 16496)
-- Name: adresy adresy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adresy
    ADD CONSTRAINT adresy_pkey PRIMARY KEY (id_adresu);


--
-- TOC entry 3318 (class 2606 OID 16527)
-- Name: dostawcy dostawcy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dostawcy
    ADD CONSTRAINT dostawcy_pkey PRIMARY KEY (id_dostawcy);


--
-- TOC entry 3316 (class 2606 OID 16515)
-- Name: pracownicy pracownicy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pracownicy
    ADD CONSTRAINT pracownicy_pkey PRIMARY KEY (id_pracownika);


--
-- TOC entry 3320 (class 2606 OID 16539)
-- Name: produkty produkty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produkty
    ADD CONSTRAINT produkty_pkey PRIMARY KEY (id_produktu);


--
-- TOC entry 3314 (class 2606 OID 16503)
-- Name: sklepy sklepy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sklepy
    ADD CONSTRAINT sklepy_pkey PRIMARY KEY (id_sklepu);


--
-- TOC entry 3324 (class 2606 OID 16563)
-- Name: transakcje transakcje_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transakcje
    ADD CONSTRAINT transakcje_pkey PRIMARY KEY (id_transakcji);


--
-- TOC entry 3322 (class 2606 OID 16551)
-- Name: wypieki wypieki_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wypieki
    ADD CONSTRAINT wypieki_pkey PRIMARY KEY (id_wypieku);


--
-- TOC entry 3327 (class 2606 OID 16528)
-- Name: dostawcy dostawcy_id_adresu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dostawcy
    ADD CONSTRAINT dostawcy_id_adresu_fkey FOREIGN KEY (id_adresu) REFERENCES public.adresy(id_adresu);


--
-- TOC entry 3326 (class 2606 OID 16516)
-- Name: pracownicy pracownicy_id_adresu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pracownicy
    ADD CONSTRAINT pracownicy_id_adresu_fkey FOREIGN KEY (id_adresu) REFERENCES public.adresy(id_adresu);


--
-- TOC entry 3328 (class 2606 OID 16540)
-- Name: produkty produkty_id_dostawcy_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produkty
    ADD CONSTRAINT produkty_id_dostawcy_fkey FOREIGN KEY (id_dostawcy) REFERENCES public.dostawcy(id_dostawcy);


--
-- TOC entry 3325 (class 2606 OID 16504)
-- Name: sklepy sklepy_id_adresu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sklepy
    ADD CONSTRAINT sklepy_id_adresu_fkey FOREIGN KEY (id_adresu) REFERENCES public.adresy(id_adresu);


--
-- TOC entry 3330 (class 2606 OID 16569)
-- Name: transakcje transakcje_id_sklepu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transakcje
    ADD CONSTRAINT transakcje_id_sklepu_fkey FOREIGN KEY (id_sklepu) REFERENCES public.sklepy(id_sklepu);


--
-- TOC entry 3331 (class 2606 OID 16564)
-- Name: transakcje transakcje_id_wypieku_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transakcje
    ADD CONSTRAINT transakcje_id_wypieku_fkey FOREIGN KEY (id_wypieku) REFERENCES public.wypieki(id_wypieku);


--
-- TOC entry 3329 (class 2606 OID 16552)
-- Name: wypieki wypieki_id_produktu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wypieki
    ADD CONSTRAINT wypieki_id_produktu_fkey FOREIGN KEY (id_produktu) REFERENCES public.produkty(id_produktu);


-- Completed on 2026-02-02 23:09:09 CET

--
-- PostgreSQL database dump complete
--

\unrestrict PTL5hVFYAuT6udZk1KgMbAtAYuNBfSxxbJRzZg0SXcCZUHo4yvTaPflASJNeCcp

