
CREATE TABLE utilisateur (
	id INTEGER,
	password VARCHAR(50),
	nom VARCHAR(50),
	prenom VARCHAR(50),
	dateNaissance VARCHAR(50),
	role VARCHAR(20), /* admin,citoyen ou visiteur */
	profession VARCHAR(40),
	nbAnneesPostBac INTEGER,
	sexe VARCHAR(1),
	CONSTRAINT user_PK PRIMARY KEY(id)
    );

CREATE TABLE conference(
	id INTEGER,
	titre VARCHAR(20),
	theme VARCHAR(20),
	dateCreation VARCHAR(50) DEFAULT (datetime(current_timestamp)),
	etatActuel VARCHAR(10),
	description VARCHAR(500),
	CONSTRAINT conference_PK PRIMARY KEY(id)
	);

CREATE TABLE questionnaire(
	id INTEGER,
	titre VARCHAR(200),
	idCreateur INTEGER, /* ref à ID_USER */
	dateFermeture VARCHAR(50) DEFAULT (DATETIME('now', '+2 days')),
	idConference INTEGER,
	CONSTRAINT questionnaire_PK PRIMARY KEY(id),
	CONSTRAINT questionnaire_user_fk FOREIGN KEY (idCreateur) REFERENCES utilisateur(id),
	CONSTRAINT questionnaire_conf_fk FOREIGN KEY (idConference) REFERENCES conference(id)
);

CREATE TABLE question(
	id INTEGER,
	numero INTEGER,
	typeQuestion VARCHAR(6), /* QCM OU TEXTE */
	contenu VARCHAR(500),
	idQuestionnaire INTEGER,
	CONSTRAINT question_PK PRIMARY KEY(id),
	CONSTRAINT question_questionnaire_fk FOREIGN KEY (idQuestionnaire) REFERENCES questionnaire(id)
);

CREATE TABLE reponseTexte(
	id INTEGER,
	contenu VARCHAR(1000),
	idQuestion INTEGER,
	idUtilisateur INTEGER,
	CONSTRAINT reponsetexte_PK PRIMARY KEY(id),
	CONSTRAINT reponsetxt_question_fk FOREIGN KEY (idQuestion) REFERENCES question(id),
	CONSTRAINT reponsetxt_user_fk FOREIGN KEY (idUtilisateur) REFERENCES utilisateur(id)
);

CREATE TABLE reponseQcm(
	idChoix INTEGER,
	idQuestion INTEGER,
	idUtilisateur INTEGER,
	CONSTRAINT reponseqcm_PK PRIMARY KEY(idChoix, idQuestion, idUtilisateur),
	CONSTRAINT reponseqcm_question_fk FOREIGN KEY (idQuestion) REFERENCES question(id),
	CONSTRAINT reponseqcm_choix_fk FOREIGN KEY (idChoix) REFERENCES choixQcm(id),
	CONSTRAINT reponseqcm_user_fk FOREIGN KEY (idUtilisateur) REFERENCES utilisateur(id)
);

CREATE TABLE choixQcm(
	id INTEGER,
	numero INTEGER,
	contenu VARCHAR(100),
	idQuestion INTEGER,
	CONSTRAINT choixqcm_PK PRIMARY KEY(id),
	CONSTRAINT choixqcm_question_fk FOREIGN KEY (idQuestion) REFERENCES question(id)
);

CREATE TABLE participe(
	idUtilisateur INTEGER,
	idConference INTEGER,
	CONSTRAINT participe_PK PRIMARY KEY(idUtilisateur,idConference),
	CONSTRAINT participe_user_fk FOREIGN KEY (idUtilisateur) REFERENCES utilisateur(id),
	CONSTRAINT participe_conf_fk FOREIGN KEY (idConference) REFERENCES conference(id)
)