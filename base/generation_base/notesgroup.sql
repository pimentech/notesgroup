CREATE TABLE object (
	id SERIAL PRIMARY KEY,
	authcrea int4,
	authmodif int4,
	codecrea text,
	codemodif text,
	datecrea timestamp DEFAULT now(),
	datemodif timestamp DEFAULT now(),
	nom text,
	statut int4 DEFAULT 0
);
create unique index idx_object_id on object (id);
CREATE TABLE personne (
	adresse1 text,
	adresse2 text,
	commentaire text,
	cp text,
	email text,
	euid text,
	fax text,
	pays text,
	tel text,
	tel2 text,
	ville text,
	web text
) inherits (object);
create unique index idx_personne_id on personne (id);
alter table personne alter column datecrea set default now();
alter table personne alter column statut set default 0;
alter table personne alter column datemodif set default now();
CREATE TABLE personne_physique (
	administrateur int4 DEFAULT 0,
	civilite int4,
	key text,
	naissance date,
	prenom text
) inherits (personne);
create unique index idx_personne_physique_id on personne_physique (id);
alter table personne_physique alter column datecrea set default now();
alter table personne_physique alter column statut set default 0;
alter table personne_physique alter column datemodif set default now();
CREATE TABLE societe (
	logo text,
	raison text,
	siren text,
	siret text,
	ue_tva text
) inherits (personne);
create unique index idx_societe_id on societe (id);
alter table societe alter column datecrea set default now();
alter table societe alter column statut set default 0;
alter table societe alter column datemodif set default now();
CREATE TABLE auth_user (
	date_joined timestamp,
	email text,
	first_name text,
	id int4 DEFAULT 0,
	is_staff boolean,
	is_superuser boolean,
	last_login timestamp,
	last_name text,
	password text,
	username text unique
);
CREATE TABLE type_employe (

) inherits (object);
create unique index idx_type_employe_id on type_employe (id);
alter table type_employe alter column datecrea set default now();
alter table type_employe alter column statut set default 0;
alter table type_employe alter column datemodif set default now();
CREATE TABLE employe (
	auth_user_id int4 DEFAULT 0,
	societe_id int4 DEFAULT 0,
	type_employe_id int4 DEFAULT 0
) inherits (personne_physique);
create unique index idx_employe_id on employe (id);
create index idx_employe_auth_user_id on employe (auth_user_id);
create index idx_employe_societe_id on employe (societe_id);
create index idx_employe_type_employe_id on employe (type_employe_id);
alter table employe alter column administrateur set default 0;
alter table employe alter column datecrea set default now();
alter table employe alter column statut set default 0;
alter table employe alter column datemodif set default now();
CREATE TABLE type (

) inherits (object);
create unique index idx_type_id on type (id);
alter table type alter column datecrea set default now();
alter table type alter column statut set default 0;
alter table type alter column datemodif set default now();
CREATE TABLE type_note (

) inherits (type);
create unique index idx_type_note_id on type_note (id);
alter table type_note alter column datecrea set default now();
alter table type_note alter column statut set default 0;
alter table type_note alter column datemodif set default now();
CREATE TABLE userid (
	employe_id int4 DEFAULT 0,
	login text,
	pwd text
) inherits (object);
create unique index idx_userid_id on userid (id);
create index idx_userid_employe_id on userid (employe_id);
alter table userid alter column datecrea set default now();
alter table userid alter column statut set default 0;
alter table userid alter column datemodif set default now();
CREATE TABLE etat_note (

) inherits (type);
create unique index idx_etat_note_id on etat_note (id);
alter table etat_note alter column datecrea set default now();
alter table etat_note alter column statut set default 0;
alter table etat_note alter column datemodif set default now();
CREATE TABLE note (
	auteur_employe_id int4 DEFAULT 0,
	date_debut timestamp,
	date_fin timestamp,
	demandeur_employe_id int4 DEFAULT 0,
	description text,
	etat_note_id int4 DEFAULT 0,
	montant float8,
	object_id int4 DEFAULT 0,
	path array,
	post_alarme timestamp,
	pre_alarme timestamp,
	priorite int4,
	responsable_employe_id int4 DEFAULT 0,
	resume text,
	reussite int4,
	send_post_alarme boolean DEFAULT false,
	send_pre_alarme boolean DEFAULT false,
	type_note_id int4 DEFAULT 0
) inherits (object);
create unique index idx_note_id on note (id);
create index idx_note_type_note_id on note (type_note_id);
create index idx_note_datemodif on note (datemodif);
create index idx_note_object_id on note (object_id);
create index idx_note_auteur_employe_id on note (auteur_employe_id);
create index idx_note_responsable_employe_id on note (responsable_employe_id);
create index idx_note_etat_note_id on note (etat_note_id);
create index idx_note_demandeur_employe_id on note (demandeur_employe_id);
alter table note alter column datecrea set default now();
alter table note alter column statut set default 0;
alter table note alter column datemodif set default now();
CREATE TABLE timer (
	duration float8 DEFAULT 0,
	effective_date date DEFAULT now(),
	employe_id int4 DEFAULT 0,
	note_id int4 DEFAULT 0
) inherits (object);
create unique index idx_timer_id on timer (id);
create index idx_timer_note_id on timer (note_id);
create index idx_timer_employe_id on timer (employe_id);
create unique index timer_effective_date_ref_employe_ref_note_key on timer (effective_date, ref_employe, ref_note);
create unique index timer_note_id_employe_id_key on timer (note_id,employe_id);
alter table timer alter column datecrea set default now();
alter table timer alter column statut set default 0;
alter table timer alter column datemodif set default now();
CREATE TABLE type_role (

) inherits (type);
create unique index idx_type_role_id on type_role (id);
alter table type_role alter column datecrea set default now();
alter table type_role alter column statut set default 0;
alter table type_role alter column datemodif set default now();
CREATE TABLE droits (
	id SERIAL PRIMARY KEY,
	employe_id int4 DEFAULT 0,
	note_id int4 DEFAULT 0,
	type_role_id int4 DEFAULT 0
);
create unique index idx_droits_id on droits (id);
create index idx_droits_note_id on droits (note_id);
create index idx_droits_employe_id on droits (employe_id);
create index idx_droits_type_role_id on droits (type_role_id);
create unique index droits_note_id_employe_id_type_role_id_key on droits (note_id,employe_id,type_role_id);
CREATE TABLE action (

) inherits (note);
create unique index idx_action_id on action (id);
create index idx_action_type_note_id on action (type_note_id);
alter table action alter column type_note_id set default 0;
create index idx_action_datemodif on action (datemodif);
create index idx_action_object_id on action (object_id);
alter table action alter column object_id set default 0;
create index idx_action_auteur_employe_id on action (auteur_employe_id);
alter table action alter column auteur_employe_id set default 0;
alter table action alter column send_post_alarme set default false;
create index idx_action_responsable_employe_id on action (responsable_employe_id);
alter table action alter column responsable_employe_id set default 0;
alter table action alter column send_pre_alarme set default false;
create index idx_action_etat_note_id on action (etat_note_id);
alter table action alter column etat_note_id set default 0;
create index idx_action_demandeur_employe_id on action (demandeur_employe_id);
alter table action alter column demandeur_employe_id set default 0;
alter table action alter column datecrea set default now();
alter table action alter column statut set default 0;
alter table action alter column datemodif set default now();
