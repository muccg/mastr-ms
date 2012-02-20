--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: repository_samplelog; Type: TABLE; Schema: public; Owner: madasapp; Tablespace: 
--

CREATE TABLE repository_samplelog (
    id integer NOT NULL,
    "type" integer NOT NULL,
    changetimestamp timestamp with time zone NOT NULL,
    description character varying(255) NOT NULL,
    user_id integer,
    sample_id integer NOT NULL,
    CONSTRAINT repository_samplelog_type_check CHECK ((type >= 0))
);


ALTER TABLE public.repository_samplelog OWNER TO madasapp;

-- Name: repository_samplelog_id_seq; Type: SEQUENCE; Schema: public; Owner: madasapp
--

CREATE SEQUENCE repository_samplelog_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.repository_samplelog_id_seq OWNER TO madasapp;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: madasapp
--

ALTER TABLE repository_samplelog ALTER COLUMN id SET DEFAULT nextval('repository_samplelog_id_seq'::regclass);


--
-- Data for Name: repository_samplelog; Type: TABLE DATA; Schema: public; Owner: madasapp
--

COPY repository_samplelog (id, "type", changetimestamp, description, user_id, sample_id) FROM stdin;
\.


--
-- Name: repository_samplelog_pkey; Type: CONSTRAINT; Schema: public; Owner: madasapp; Tablespace: 
--

ALTER TABLE ONLY repository_samplelog
    ADD CONSTRAINT repository_samplelog_pkey PRIMARY KEY (id);


--
-- Name: repository_samplelog_sample_id; Type: INDEX; Schema: public; Owner: madasapp; Tablespace: 
--

CREATE INDEX repository_samplelog_sample_id ON repository_samplelog USING btree (sample_id);


--
-- Name: repository_samplelog_user_id; Type: INDEX; Schema: public; Owner: madasapp; Tablespace: 
--

CREATE INDEX repository_samplelog_user_id ON repository_samplelog USING btree (user_id);


--
-- Name: repository_samplelog_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: madasapp
--

ALTER TABLE ONLY repository_samplelog
    ADD CONSTRAINT repository_samplelog_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES repository_sample(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: repository_samplelog_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: madasapp
--

ALTER TABLE ONLY repository_samplelog
    ADD CONSTRAINT repository_samplelog_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--
