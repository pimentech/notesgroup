alter table employe add column user_id integer NOT NULL REFERENCES "auth_user" ("id"); 
alter table note add column path text; 
alter table action add column path text; 
insert into auth_user (id,username, first_name, last_name, email, password, is_staff,is_active,is_superuser,last_login,date_joined) select ref_employe,login,employe.prenom,employe.nom,employe.email,pwd,'t','t','f',employe.datecrea,employe.datemodif from userid,employe where login is not null and userid.ref_employe=employe.uid and employe.statut=0;
update employe set user_id=uid where statut=0;

-- + mig authcrea/modif -> user
