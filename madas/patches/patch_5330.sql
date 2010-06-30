ALTER TABLE seq_id_formalquote RENAME TO formalquote_id_seq;
ALTER TABLE seq_id_emailmap RENAME TO emailmap_id_seq;
ALTER TABLE seq_id_quotehistory RENAME TO quotehistory_id_seq;
ALTER TABLE seq_id_quoterequest RENAME TO quoterequest_id_seq;

ALTER TABLE emailmap ALTER COLUMN id SET DEFAULT nextval('emailmap_id_seq'::regclass);
ALTER TABLE formalquote ALTER COLUMN id SET DEFAULT nextval('formalquote_id_seq'::regclass);
ALTER TABLE quotehistory ALTER COLUMN id SET DEFAULT nextval('quotehistory_id_seq'::regclass);
ALTER TABLE quoterequest ALTER COLUMN id SET DEFAULT nextval('quoterequest_id_seq'::regclass);


