# Base (très largement modifiée) générée avec la librairie : flask-sqlacodegen et la commande :
# flask-sqlacodegen.exe sqlite:///database\database.db --flask --notables

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50))
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    dateNaissance = db.Column(db.String(50))
    role = db.Column(db.String(20))
    profession = db.Column(db.String(40))
    nbAnneesPostBac = db.Column(db.Integer)
    sexe = db.Column(db.String(1))

    participations = db.relationship('Participe',
                                     primaryjoin='Participe.idUtilisateur == Utilisateur.id',
                                     backref='participant')
    questionnaires = db.relationship('Questionnaire',
                                     primaryjoin='Questionnaire.idCreateur == Utilisateur.id',
                                     backref='createur')
    reponses_texte = db.relationship('ReponseTexte',
                                     primaryjoin='ReponseTexte.idUtilisateur == Utilisateur.id',
                                     backref='utilisateur')
    reponses_qcm = db.relationship('ReponseQcm',
                                   primaryjoin='ReponseQcm.idUtilisateur == Utilisateur.id',
                                   backref='utilisateur')


class Conference(db.Model):
    __tablename__ = 'conference'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(20))
    theme = db.Column(db.String(20))
    dateCreation = db.Column(db.String(50), server_default=db.FetchedValue())
    etatActuel = db.Column(db.String(10), default="En cours")
    description = db.Column(db.String(500))

    participations = db.relationship('Participe',
                                     primaryjoin='Participe.idConference == Conference.id',
                                     backref='conference')
    questionnaires = db.relationship('Questionnaire',
                                     primaryjoin='Questionnaire.idConference == Conference.id',
                                     backref='conference')


class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200))
    dateFermeture = db.Column(db.String(50), server_default=db.FetchedValue())
    idCreateur = db.Column(db.ForeignKey(Utilisateur.id))
    idConference = db.Column(db.ForeignKey(Conference.id))

    questions = db.relationship('Question',
                                primaryjoin='Question.idQuestionnaire == Questionnaire.id',
                                backref='questionnaire')


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer)
    typeQuestion = db.Column(db.String(6))
    contenu = db.Column(db.String(500))
    idQuestionnaire = db.Column(db.ForeignKey(Questionnaire.id))

    liste_choix_qcm = db.relationship('ChoixQcm',
                                      primaryjoin='ChoixQcm.idQuestion == Question.id',
                                      backref='question')
    reponses_texte = db.relationship('ReponseTexte',
                                     primaryjoin='ReponseTexte.idQuestion == Question.id',
                                     backref='question')


class ChoixQcm(db.Model):
    __tablename__ = 'choixQcm'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Integer)
    contenu = db.Column(db.String(100))
    idQuestion = db.Column(db.ForeignKey(Question.id))

    reponses_qcm = db.relationship('ReponseQcm',
                                   primaryjoin='ReponseQcm.idChoix == ChoixQcm.id',
                                   backref='choixQcm')


class ReponseQcm(db.Model):
    __tablename__ = 'reponseQcm'

    idChoix = db.Column(db.ForeignKey(ChoixQcm.id), primary_key=True)
    idQuestion = db.Column(db.ForeignKey(Question.id), primary_key=True)
    idUtilisateur = db.Column(db.ForeignKey(Utilisateur.id), primary_key=True)


class ReponseTexte(db.Model):
    __tablename__ = 'reponseTexte'

    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.String(1000))
    idQuestion = db.Column(db.ForeignKey(Question.id), nullable=False)
    idUtilisateur = db.Column(db.ForeignKey(Utilisateur.id), nullable=False)


class Participe(db.Model):
    __tablename__ = 'participe'

    idUtilisateur = db.Column(db.ForeignKey(Utilisateur.id), primary_key=True, nullable=False)
    idConference = db.Column(db.ForeignKey(Conference.id), primary_key=True, nullable=False)
