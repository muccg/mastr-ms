BEGIN;

ALTER SEQUENCE emailmap_id_seq OWNED BY emailmap.id;
ALTER SEQUENCE formalquote_id_seq OWNED BY formalquote.id;
ALTER SEQUENCE quotehistory_id_seq OWNED BY quotehistory.id;
ALTER SEQUENCE quoterequest_id_seq OWNED BY quoterequest.id;

COMMIT;
