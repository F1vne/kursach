--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

-- Started on 2023-09-18 16:51:24

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
-- TOC entry 216 (class 1259 OID 24596)
-- Name: correspondence; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.correspondence (
    id_korresp integer NOT NULL,
    document_type character varying(255),
    execution_date date,
    receipt_date date,
    id_sotrudnik integer,
    id_org integer NOT NULL
);


ALTER TABLE public.correspondence OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 24577)
-- Name: organization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization (
    name character varying(255) NOT NULL,
    ownership character varying(255),
    id_org integer NOT NULL
);


ALTER TABLE public.organization OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 24584)
-- Name: sotrudniki; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sotrudniki (
    id_sotrudnik integer NOT NULL,
    name character varying(255)
);


ALTER TABLE public.sotrudniki OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24616)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    login text,
    passwd text,
    id_sotrudnik integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 3337 (class 0 OID 24596)
-- Dependencies: 216
-- Data for Name: correspondence; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.correspondence (id_korresp, document_type, execution_date, receipt_date, id_sotrudnik, id_org) FROM stdin;
1	Договор	2022-01-15	2022-01-25	3	1
3	Договор	2023-03-15	2023-03-20	2	2
4	Уведомление	2023-03-19	2023-03-25	1	1
5	Акт	2023-12-19	2023-12-25	3	3
2	Письмо	2022-01-17	2022-01-20	1	4
\.


--
-- TOC entry 3335 (class 0 OID 24577)
-- Dependencies: 214
-- Data for Name: organization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization (name, ownership, id_org) FROM stdin;
ОАО Газпром	Государственная	1
ПАО ЛУКОЙЛ	Публичная	2
ПАО Северсталь	Публичная	3
Рога и копыта	Частная	4
\.


--
-- TOC entry 3336 (class 0 OID 24584)
-- Dependencies: 215
-- Data for Name: sotrudniki; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sotrudniki (id_sotrudnik, name) FROM stdin;
1	Иванов Иван Иванович
2	Петров Петр Петрович
3	Сидоров Сидор Сидорович
\.


--
-- TOC entry 3338 (class 0 OID 24616)
-- Dependencies: 217
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (login, passwd, id_sotrudnik) FROM stdin;
admin	1234	1
senior_manager	1234	2
product_manager	1234	3
\.


--
-- TOC entry 3189 (class 2606 OID 24600)
-- Name: correspondence correspondence_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.correspondence
    ADD CONSTRAINT correspondence_pkey PRIMARY KEY (id_korresp);


--
-- TOC entry 3185 (class 2606 OID 24629)
-- Name: organization organization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (id_org);


--
-- TOC entry 3187 (class 2606 OID 24590)
-- Name: sotrudniki sotrudniki_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sotrudniki
    ADD CONSTRAINT sotrudniki_pkey PRIMARY KEY (id_sotrudnik);


--
-- TOC entry 3190 (class 2606 OID 24630)
-- Name: correspondence id_org; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.correspondence
    ADD CONSTRAINT id_org FOREIGN KEY (id_org) REFERENCES public.organization(id_org) NOT VALID;


--
-- TOC entry 3191 (class 2606 OID 24606)
-- Name: correspondence id_sotrudnik; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.correspondence
    ADD CONSTRAINT id_sotrudnik FOREIGN KEY (id_sotrudnik) REFERENCES public.sotrudniki(id_sotrudnik) NOT VALID;


--
-- TOC entry 3192 (class 2606 OID 24621)
-- Name: users id_sotrudnik; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT id_sotrudnik FOREIGN KEY (id_sotrudnik) REFERENCES public.sotrudniki(id_sotrudnik);


--
-- TOC entry 3344 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE correspondence; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.correspondence TO admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.correspondence TO manager;
GRANT SELECT ON TABLE public.correspondence TO sotrudnik;


--
-- TOC entry 3345 (class 0 OID 0)
-- Dependencies: 214
-- Name: TABLE organization; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.organization TO admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.organization TO manager;


--
-- TOC entry 3346 (class 0 OID 0)
-- Dependencies: 215
-- Name: TABLE sotrudniki; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.sotrudniki TO admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.sotrudniki TO manager;
GRANT SELECT ON TABLE public.sotrudniki TO sotrudnik;


-- Completed on 2023-09-18 16:51:25

--
-- PostgreSQL database dump complete
--

