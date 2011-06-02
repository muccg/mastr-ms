
-- Creates Django users for all Madas LDAP users that aren't already in Django.
-- This is to be run on the LIVE DB

BEGIN;

INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'ntakayama@ccg.murdoch.edu.au', '', '', 'ntakayama@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'ntakayama@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'ntt@ii.net', '', '', 'ntt@ii.net', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'ntt@ii.net');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'ntakayama@murdoch.edu.au', '', '', 'ntakayama@murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'ntakayama@murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'aahunter@gmail.com', '', '', 'aahunter@gmail.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'aahunter@gmail.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'techs@cbbc.murdoch.edu.au', '', '', 'techs@cbbc.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'techs@cbbc.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'noreply@ccg.murdoch.edu.au', '', '', 'noreply@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'noreply@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'cletto13@gmail.com', '', '', 'cletto13@gmail.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'cletto13@gmail.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'sdayalan@unimelb.edu.au', '', '', 'sdayalan@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'sdayalan@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'blah@blah.com', '', '', 'blah@blah.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'blah@blah.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'selenium-noreply@ccg.murdoch.edu.au', '', '', 'selenium-noreply@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'selenium-noreply@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'u.roessner@unimelb.edu.au', '', '', 'u.roessner@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'u.roessner@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'vlikic@unimelb.edu.au', '', '', 'vlikic@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'vlikic@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'jeremy.hack@awri.com.au', '', '', 'jeremy.hack@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'jeremy.hack@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'o.frick@uq.edu.au', '', '', 'o.frick@uq.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'o.frick@uq.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'test@test.test.com', '', '', 'test@test.test.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'test@test.test.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'sdayalan@cs.rmit.edu.au', '', '', 'sdayalan@cs.rmit.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'sdayalan@cs.rmit.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'saravanan.dayalan@rmit.edu.au', '', '', 'saravanan.dayalan@rmit.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'saravanan.dayalan@rmit.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'g.cloud@zxz.com.au', '', '', 'g.cloud@zxz.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'g.cloud@zxz.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'ntt@iinet.net.au', '', '', 'ntt@iinet.net.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'ntt@iinet.net.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'test@test.com', '', '', 'test@test.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'test@test.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'sdayalan@goanna.cs.rmit.edu.au', '', '', 'sdayalan@goanna.cs.rmit.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'sdayalan@goanna.cs.rmit.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'test@user.com', '', '', 'test@user.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'test@user.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'ntakayama.nttblog@blogger.com', '', '', 'ntakayama.nttblog@blogger.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'ntakayama.nttblog@blogger.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'r.trengove@murdoch.edu.au', '', '', 'r.trengove@murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'r.trengove@murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'ricarda.fenske@uwa.edu.au', '', '', 'ricarda.fenske@uwa.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'ricarda.fenske@uwa.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'meagan.mercurio@awri.com.au', '', '', 'meagan.mercurio@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'meagan.mercurio@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'jsheedy@unimelb.edu.au', '', '', 'jsheedy@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'jsheedy@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'zfelton@unimelb.edu.au', '', '', 'zfelton@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'zfelton@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'desouzad@unimelb.edu.au', '', '', 'desouzad@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'desouzad@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'pereiran@unimelb.edu.au', '', '', 'pereiran@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'pereiran@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'markus.herderich@awri.com.au', '', '', 'markus.herderich@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'markus.herderich@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'alingham@unimelb.edu.au', '', '', 'alingham@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'alingham@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 's.natera@unimelb.edu.au', '', '', 's.natera@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 's.natera@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'saravanan.dayalan@gmail.com', '', '', 'saravanan.dayalan@gmail.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'saravanan.dayalan@gmail.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'davihac@rediffmail.com', '', '', 'davihac@rediffmail.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'davihac@rediffmail.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'e46949@rmit.edu.au', '', '', 'e46949@rmit.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'e46949@rmit.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'john@a.com', '', '', 'john@a.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'john@a.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'abcde1@unimelb.edu.au', '', '', 'abcde1@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'abcde1@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'e46949@ems.rmit.edu.au', '', '', 'e46949@ems.rmit.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'e46949@ems.rmit.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'abcde2@unimelb1.edu.au', '', '', 'abcde2@unimelb1.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'abcde2@unimelb1.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'abcde3@unimelb1.edu.au', '', '', 'abcde3@unimelb1.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'abcde3@unimelb1.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'amini@unimelb.edu.au', '', '', 'amini@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'amini@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'abcde5@unimelb1.edu.au', '', '', 'abcde5@unimelb1.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'abcde5@unimelb1.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'abcd@unimelb123.edu.au', '', '', 'abcd@unimelb123.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'abcd@unimelb123.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'drolli.frick@gmail.com', '', '', 'drolli.frick@gmail.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'drolli.frick@gmail.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'moshea@ccg.murdoch.edu.au', '', '', 'moshea@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'moshea@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'bpower@ccg.murdoch.edu.au', '', '', 'bpower@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'bpower@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'noderep@ccg.murdoch.edu.au', '', '', 'noderep@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'noderep@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'testuser@ccg.murdoch.edu.au', '', '', 'testuser@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'testuser@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 's.jacob@uq.edu.au', '', '', 's.jacob@uq.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 's.jacob@uq.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'a@a.com', '', '', 'a@a.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'a@a.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'kioumars@cyllene.uwa.edu.au', '', '', 'kioumars@cyllene.uwa.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'kioumars@cyllene.uwa.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'michelle.benison@orphan.com.au', '', '', 'michelle.benison@orphan.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'michelle.benison@orphan.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'chris.curtin@awri.com.au', '', '', 'chris.curtin@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'chris.curtin@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'robert.asenstorfer@adelaide.edu.au', '', '', 'robert.asenstorfer@adelaide.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'robert.asenstorfer@adelaide.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'w.lee@murdoch.edu.au', '', '', 'w.lee@murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'w.lee@murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'phil.giffard@menzies.edu.au', '', '', 'phil.giffard@menzies.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'phil.giffard@menzies.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'josquint@unimelb.edu.au', '', '', 'josquint@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'josquint@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'eunyoungchoi_2000@yahoo.com.au', '', '', 'eunyoungchoi_2000@yahoo.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'eunyoungchoi_2000@yahoo.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'pwale@pgrad.unimelb.edu.au', '', '', 'pwale@pgrad.unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'pwale@pgrad.unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'eveline.bartowsky@awri.com.au', '', '', 'eveline.bartowsky@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'eveline.bartowsky@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'r.bruzzese@latrobe.edu.au', '', '', 'r.bruzzese@latrobe.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'r.bruzzese@latrobe.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'melanie.mcdowall@adelaide.edu.au', '', '', 'melanie.mcdowall@adelaide.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'melanie.mcdowall@adelaide.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'andrew@ccg.murdoch.edu.au', '', '', 'andrew@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'andrew@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'wlia7758@uni.sydney.edu.au', '', '', 'wlia7758@uni.sydney.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'wlia7758@uni.sydney.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'peter.valente@adelaide.edu.au', '', '', 'peter.valente@adelaide.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'peter.valente@adelaide.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'Creina.Stockley@awri.com.au', '', '', 'Creina.Stockley@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'Creina.Stockley@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'pmir6490@uni.sydney.edu.au', '', '', 'pmir6490@uni.sydney.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'pmir6490@uni.sydney.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'erminawati.wuryatmo@adelaide.edu.au', '', '', 'erminawati.wuryatmo@adelaide.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'erminawati.wuryatmo@adelaide.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'christopher.ford@adelaide.edu.au', '', '', 'christopher.ford@adelaide.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'christopher.ford@adelaide.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'simon.schmidt@awri.com.au', '', '', 'simon.schmidt@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'simon.schmidt@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'warren.roget@awri.com.au', '', '', 'warren.roget@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'warren.roget@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'helen.holt@awri.com.au', '', '', 'helen.holt@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'helen.holt@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'Mango.Parker@awri.com.au', '', '', 'Mango.Parker@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'Mango.Parker@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'tszabo@ccg.murdoch.edu.au', '', '', 'tszabo@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'tszabo@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'resendis@ccg.unam.mx', '', '', 'resendis@ccg.unam.mx', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'resendis@ccg.unam.mx');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'jennie.gardner@adelaide.edu.au', '', '', 'jennie.gardner@adelaide.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'jennie.gardner@adelaide.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'w.ditcham@murdoch.edu.au', '', '', 'w.ditcham@murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'w.ditcham@murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'ondrej.zvarec@gmail.com', '', '', 'ondrej.zvarec@gmail.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'ondrej.zvarec@gmail.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'mosheo@unimelb.edu.au', '', '', 'mosheo@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'mosheo@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'dschibeci@ccg.murdoch.edu.au', '', '', 'dschibeci@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'dschibeci@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'simon.odell@awri.com.au', '', '', 'simon.odell@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'simon.odell@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'c.rawlinson@murdoch.edu.au', '', '', 'c.rawlinson@murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'c.rawlinson@murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'damienlc@unimelb.edu.au', '', '', 'damienlc@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'damienlc@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'dedreia@unimelb.edu.au', '', '', 'dedreia@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'dedreia@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'ignore@ccg.murdoch.edu.au', '', '', 'ignore@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'ignore@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'brgordon17@gmail.com', '', '', 'brgordon17@gmail.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'brgordon17@gmail.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'nicholas.hatzirodos@adelaide.edu.au', '', '', 'nicholas.hatzirodos@adelaide.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'nicholas.hatzirodos@adelaide.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'jaime.low.yokesum@simedarby.com', '', '', 'jaime.low.yokesum@simedarby.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'jaime.low.yokesum@simedarby.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'rakshitpanwar@yahoo.com', '', '', 'rakshitpanwar@yahoo.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'rakshitpanwar@yahoo.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'bolandm@unimelb.edu.au', '', '', 'bolandm@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'bolandm@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'adam.carroll@anu.edu.au', '', '', 'adam.carroll@anu.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'adam.carroll@anu.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'raisa_bano@yahoo.com', '', '', 'raisa_bano@yahoo.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'raisa_bano@yahoo.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'nsj@unimelb.edu.au', '', '', 'nsj@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'nsj@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'ros.gleadow@sci.monash.edu.au', '', '', 'ros.gleadow@sci.monash.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'ros.gleadow@sci.monash.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'jpyke@unimelb.edu.au', '', '', 'jpyke@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'jpyke@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'malaua@unimelb.edu.au', '', '', 'malaua@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'malaua@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'csilva@unimelb.edu.au', '', '', 'csilva@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'csilva@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'jairus.bowne@gmail.com', '', '', 'jairus.bowne@gmail.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'jairus.bowne@gmail.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'baboug@unimelb.edu.au', '', '', 'baboug@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'baboug@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'tru@unimelb.edu', '', '', 'tru@unimelb.edu', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'tru@unimelb.edu');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'spearse@graduate.uwa.edu.au', '', '', 'spearse@graduate.uwa.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'spearse@graduate.uwa.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'mbenghezal@ondek.com', '', '', 'mbenghezal@ondek.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'mbenghezal@ondek.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'arjmand1@yahoo.com', '', '', 'arjmand1@yahoo.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'arjmand1@yahoo.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'clemot01@student.uwa.edu.au', '', '', 'clemot01@student.uwa.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'clemot01@student.uwa.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'aharvey@ccg.murdoch.edu.au', '', '', 'aharvey@ccg.murdoch.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'aharvey@ccg.murdoch.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'phil.mercurio@awri.com.au', '', '', 'phil.mercurio@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'phil.mercurio@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'mariola.kwiatkowski@awri.com.au', '', '', 'mariola.kwiatkowski@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'mariola.kwiatkowski@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'brianjmeade@gmail.com', '', '', 'brianjmeade@gmail.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'brianjmeade@gmail.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'david.jeffery@awri.com.au', '', '', 'david.jeffery@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'david.jeffery@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'neil.scrimgeour@awri.com.au', '', '', 'neil.scrimgeour@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'neil.scrimgeour@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'mark.solomon@awri.com.au', '', '', 'mark.solomon@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'mark.solomon@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'kritaya.kongsuwan@csiro.au', '', '', 'kritaya.kongsuwan@csiro.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'kritaya.kongsuwan@csiro.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'paul.grbin@adelaide.edu.au', '', '', 'paul.grbin@adelaide.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'paul.grbin@adelaide.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'michael.oliver@uandinatural.com', '', '', 'michael.oliver@uandinatural.com', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'michael.oliver@uandinatural.com');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'yoji.hayasaka@awri.com.au', '', '', 'yoji.hayasaka@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'yoji.hayasaka@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'tyoung@aut.ac.nz', '', '', 'tyoung@aut.ac.nz', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'tyoung@aut.ac.nz');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'Randell.Taylor@awri.com.au', '', '', 'Randell.Taylor@awri.com.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'Randell.Taylor@awri.com.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'adam.potter@adelaide.edu.au', '', '', 'adam.potter@adelaide.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'adam.potter@adelaide.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'tru@unimelb.edu.au', '', '', 'tru@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'tru@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'c.schmitz-peiffer@garvan.org.au', '', '', 'c.schmitz-peiffer@garvan.org.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'c.schmitz-peiffer@garvan.org.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'jennihetz@yahoo.es', '', '', 'jennihetz@yahoo.es', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'jennihetz@yahoo.es');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 's.li@latrobe.edu.au', '', '', 's.li@latrobe.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 's.li@latrobe.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'alexander.wilding@monash.edu', '', '', 'alexander.wilding@monash.edu', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'alexander.wilding@monash.edu');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'rohan.lowe@unimelb.edu.au', '', '', 'rohan.lowe@unimelb.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'rohan.lowe@unimelb.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'mfakiola@ichr.uwa.edu.au', '', '', 'mfakiola@ichr.uwa.edu.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'mfakiola@ichr.uwa.edu.au');


INSERT INTO auth_user(username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
SELECT 'Mick.Alderton@dsto.defence.gov.au', '', '', 'Mick.Alderton@dsto.defence.gov.au', '!', false, true, false, now(), now()
  WHERE NOT EXISTS (
        SELECT 1 FROM auth_user WHERE username = 'Mick.Alderton@dsto.defence.gov.au');


COMMIT;

