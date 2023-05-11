--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

-- Started on 2023-05-11 23:12:09

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

--
-- TOC entry 220 (class 1255 OID 16455)
-- Name: oklad_func(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.oklad_func()
    LANGUAGE plpgsql
    AS $$
declare
	  rezult double precision;
begin
	select roads.distance * payment_work.salary  from roads 
	inner join payment_work on roads.kod_m = payment_work.kod_m into rezult;
	raise notice '%', rezult;
end ;
$$;


ALTER PROCEDURE public.oklad_func() OWNER TO postgres;

--
-- TOC entry 221 (class 1255 OID 16457)
-- Name: oklad_func(integer); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.oklad_func(IN kod integer)
    LANGUAGE plpgsql
    AS $$
declare
	  rezult double precision;
begin
	select roads.distance * payment_work.salary into rezult from roads 
	inner join payment_work on roads.kod_m = payment_work.kod_m where roads.kod_m = kod;
	raise notice '%', rezult;
end ;
$$;


ALTER PROCEDURE public.oklad_func(IN kod integer) OWNER TO postgres;

--
-- TOC entry 222 (class 1255 OID 16458)
-- Name: update_procent_prize(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_procent_prize() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
	update prize set procent_prize = procent_prize + 0.10;
	return new;
end;
$$;


ALTER FUNCTION public.update_procent_prize() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16417)
-- Name: cargo_transp; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cargo_transp (
    kod_m integer NOT NULL,
    kod_dr integer NOT NULL,
    date_otgr date,
    date_prib date,
    time_add double precision DEFAULT '0'::double precision NOT NULL
);


ALTER TABLE public.cargo_transp OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16402)
-- Name: drivers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.drivers (
    kod_dr integer NOT NULL,
    fio character(100) NOT NULL,
    adress character(100),
    tel character(20),
    work_exp integer
);


ALTER TABLE public.drivers OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16445)
-- Name: date_work_drivers; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.date_work_drivers AS
 SELECT drivers.kod_dr,
    drivers.fio,
    cargo_transp.date_otgr,
    cargo_transp.date_prib
   FROM (public.drivers
     JOIN public.cargo_transp ON ((drivers.kod_dr = cargo_transp.kod_dr)));


ALTER TABLE public.date_work_drivers OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16431)
-- Name: payment_work; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_work (
    kod_pw integer NOT NULL,
    kod_m integer NOT NULL,
    salary integer NOT NULL,
    salary_time_add integer NOT NULL
);


ALTER TABLE public.payment_work OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16407)
-- Name: prize; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prize (
    kod_prize integer NOT NULL,
    kod_dr integer NOT NULL,
    procent_prize double precision
);


ALTER TABLE public.prize OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16397)
-- Name: roads; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roads (
    kod_m integer NOT NULL,
    name_m character(100) NOT NULL,
    distance double precision NOT NULL
);


ALTER TABLE public.roads OWNER TO postgres;

--
-- TOC entry 3355 (class 0 OID 16417)
-- Dependencies: 217
-- Data for Name: cargo_transp; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cargo_transp (kod_m, kod_dr, date_otgr, date_prib, time_add) VALUES (1, 3, '2023-01-12', '2023-01-15', 0);
INSERT INTO public.cargo_transp (kod_m, kod_dr, date_otgr, date_prib, time_add) VALUES (2, 2, '2023-01-12', '2023-01-13', 1.15);
INSERT INTO public.cargo_transp (kod_m, kod_dr, date_otgr, date_prib, time_add) VALUES (3, 1, '2023-02-22', '2023-02-23', 0.16);


--
-- TOC entry 3353 (class 0 OID 16402)
-- Dependencies: 215
-- Data for Name: drivers; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.drivers (kod_dr, fio, adress, tel, work_exp) VALUES (1, 'Андреев Андрей Андреевич                                                                            ', 'ул. Пушкина, д.12, кв.2                                                                             ', '+79053336161        ', 1);
INSERT INTO public.drivers (kod_dr, fio, adress, tel, work_exp) VALUES (3, 'Васильев Василий Васильевич                                                                         ', 'ул. Б. Санкт-Петербугская, д.2, к.3, кв.199                                                         ', '89552348171         ', 2);
INSERT INTO public.drivers (kod_dr, fio, adress, tel, work_exp) VALUES (2, 'Петров Петр Петрович                                                                                ', 'ул. Грибоедова, д.133, кв.422                                                                       ', '+79099936162        ', 1);


--
-- TOC entry 3356 (class 0 OID 16431)
-- Dependencies: 218
-- Data for Name: payment_work; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.payment_work (kod_pw, kod_m, salary, salary_time_add) VALUES (2, 1, 300, 350);
INSERT INTO public.payment_work (kod_pw, kod_m, salary, salary_time_add) VALUES (1, 2, 200, 250);
INSERT INTO public.payment_work (kod_pw, kod_m, salary, salary_time_add) VALUES (3, 3, 250, 150);


--
-- TOC entry 3354 (class 0 OID 16407)
-- Dependencies: 216
-- Data for Name: prize; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.prize (kod_prize, kod_dr, procent_prize) VALUES (1, 1, 0.25);
INSERT INTO public.prize (kod_prize, kod_dr, procent_prize) VALUES (2, 2, 0.1);
INSERT INTO public.prize (kod_prize, kod_dr, procent_prize) VALUES (3, 3, 0.35);


--
-- TOC entry 3352 (class 0 OID 16397)
-- Dependencies: 214
-- Data for Name: roads; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.roads (kod_m, name_m, distance) VALUES (1, 'Санкт-Петербург - Белгород                                                                          ', 100.332);
INSERT INTO public.roads (kod_m, name_m, distance) VALUES (2, 'Санкт-Петербург - Москва                                                                            ', 50.3);
INSERT INTO public.roads (kod_m, name_m, distance) VALUES (3, 'Великий Новгород - Москва                                                                           ', 150.23);


--
-- TOC entry 3199 (class 2606 OID 16406)
-- Name: drivers drivers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT drivers_pkey PRIMARY KEY (kod_dr);


--
-- TOC entry 3203 (class 2606 OID 16435)
-- Name: payment_work payment_work_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_work
    ADD CONSTRAINT payment_work_pkey PRIMARY KEY (kod_pw);


--
-- TOC entry 3201 (class 2606 OID 16411)
-- Name: prize prize_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prize
    ADD CONSTRAINT prize_pkey PRIMARY KEY (kod_prize);


--
-- TOC entry 3197 (class 2606 OID 16401)
-- Name: roads roads_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roads
    ADD CONSTRAINT roads_pkey PRIMARY KEY (kod_m);


--
-- TOC entry 3208 (class 2620 OID 16461)
-- Name: drivers add_procent_prize; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER add_procent_prize AFTER UPDATE OF work_exp ON public.drivers FOR EACH ROW WHEN ((new.work_exp > old.work_exp)) EXECUTE FUNCTION public.update_procent_prize();


--
-- TOC entry 3204 (class 2606 OID 16412)
-- Name: prize kod_dr; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prize
    ADD CONSTRAINT kod_dr FOREIGN KEY (kod_dr) REFERENCES public.drivers(kod_dr);


--
-- TOC entry 3205 (class 2606 OID 16426)
-- Name: cargo_transp kod_dr; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cargo_transp
    ADD CONSTRAINT kod_dr FOREIGN KEY (kod_dr) REFERENCES public.drivers(kod_dr) NOT VALID;


--
-- TOC entry 3206 (class 2606 OID 16421)
-- Name: cargo_transp kod_m; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cargo_transp
    ADD CONSTRAINT kod_m FOREIGN KEY (kod_m) REFERENCES public.roads(kod_m) NOT VALID;


--
-- TOC entry 3207 (class 2606 OID 16436)
-- Name: payment_work kod_m; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_work
    ADD CONSTRAINT kod_m FOREIGN KEY (kod_m) REFERENCES public.roads(kod_m);


-- Completed on 2023-05-11 23:12:10

--
-- PostgreSQL database dump complete
--

