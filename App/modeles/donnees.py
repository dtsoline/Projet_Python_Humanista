from lxml import etree as ET
from ..app import db
from ..constantes import CORPUS
import re


# définition de la classe HummCorr,
# les attributs de la table correspondent aux caractéristiques des lettres.
class HumCorr(db.Model):
    __tablename__ = "lettres"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    ref = db.Column(db.Text)
    type = db.Column(db.Text)
    date = db.Column(db.Text)
    place = db.Column(db.Text)
    author_ref = db.Column(db.Text)
    author_name = db.Column(db.Text)
    dest_ref = db.Column(db.Text)
    dest_name = db.Column(db.Text)


# définition de la classe Personnes,
# les attributs de la table correspondent aux caractéristiques des personnes renseignés dans le teiHeader.
class Personnes(db.Model):
    __tablename__ = "personnes"
    id_person = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    xml_ref_person = db.Column(db.Text)
    author = db.Column(db.Integer)
    name_person = db.Column(db.Text)
    person_image = db.Column(db.Text)
    naissance = db.Column(db.Text)
    mort = db.Column(db.Text)
    wiki = db.Column(db.Text)
    id_wikidata = db.Column(db.Text)


# définition de la classe Lieux,
# les attributs de la table correspondent aux caractéristiques des lieux renseignés dans le teiHeader.
class Lieux(db.Model):
    __tablename__ = "lieux"
    id_lieu = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    xml_ref_lieu = db.Column(db.Text)
    name_lieu = db.Column(db.Text)
    longitude = db.Column(db.Integer)
    latitude = db.Column(db.Integer)
    pays = db.Column(db.Integer)



# la fonction db_init récupère les informations dans le dataset TEI pour remplir les classes.
#
def db_init(tei_corpus):
    """
        Cette fonction prend comme argument un fichier XML répondant au schéma TEI,
        préalablement parsé par LXML.
        Après avoir effacé le précédent contenu des classes, elle recherche les informations
        correspondantes pour chaque lettres, chaque personnes et chaque lieux.
        La fonction retourne les valeurs correspondantes pour chaque attribut
        des tables HumCorr, Personnes et Lieux, si celles-ci existent.
        Dans le cas contraire, elle retourne la valeur None.

        :param tei_corpus: variable dont la valeur correspond au chemin de fichier XML parsé par etree
        :tei_corpus type: str
        :return: informations au sein des classes HumCorr, Personnes et Lieux
        :return type: list
        """


    db.drop_all()
    db.create_all()


# On boucle sur chaque élément 'text' lui-même contenu dans un élément 'group' correspondant à une lettre.

    for lettre in tei_corpus.xpath("//group/text"):

        author_propre = lettre.xpath(".//persName[@role='author']/@ref")[0][1:] if lettre.xpath(
                ".//persName[@role='author']/@ref") else None
        destinataire_propre = lettre.xpath(".//persName[@role='dest']/@ref")[0][1:] if lettre.xpath(
                ".//persName[@role='dest']/@ref") else None
        aut_name = tei_corpus.xpath(f"//person[@xml:id='{str(author_propre)}']/persName/text()")
        dest_name = tei_corpus.xpath(f"//person[@xml:id='{str(destinataire_propre)}']/persName/text()")

        # la méthode .add permet d'jouter les valeurs des listes dans la table HumCorr.
        # Si cette valeur n'existe pas, c'est une valeur nulle 'None' qui est ajoutée.

        db.session.add(HumCorr(
            id = lettre.xpath("./@n")[0],
            ref = lettre.xpath("./@xml:id")[0],
            type = lettre.xpath("./@type")[0],
            date = lettre.xpath("./@date")[0] if lettre.xpath("./@date") else None,
            place =lettre.xpath("./@place")[0] if lettre.xpath("./@place") else None,
            author_ref = lettre.xpath(".//persName[@role='author']/@ref")[0] if lettre.xpath(
                ".//persName[@role='author']/@ref") else None,
            author_name = str(aut_name) if author_propre else None,
            dest_ref = lettre.xpath(".//persName[@role='dest']/@ref")[0] if lettre.xpath(
                ".//persName[@role='dest']/@ref") else None,
            dest_name = str(dest_name) if destinataire_propre else None
        ))

# On boucle sur chaque élément 'person' contenu dans un élément 'listPerson' correspondant à une personne.

    for name_pers in tei_corpus.xpath("//listPerson/person"):

        db.session.add(Personnes(
            xml_ref_person = name_pers.xpath("./@xml:id")[0] if name_pers.xpath("./@xml:id") else None,
            author='#'+name_pers.xpath("./@xml:id")[0] if name_pers.xpath("./@xml:id") else None,
            name_person = name_pers.xpath("./persName/text()")[0] if name_pers.xpath("./persName/text()") else None,
            person_image = name_pers.xpath("./graphic/@url")[0] if name_pers.xpath("./graphic/@url") else None,
            naissance = name_pers.xpath("./birth/@when")[0][0:4] if name_pers.xpath("./birth/@when") else None,
            mort = name_pers.xpath("./death/@when")[0][0:4] if name_pers.xpath("./death/@when") else None,
            wiki = name_pers.xpath("./ptr[@type='furtherInfo']/@target")[0] if name_pers.xpath("./ptr[@type='furtherInfo']/@target") else None,
            id_wikidata = name_pers.xpath("./ptr[@type='wikidata']/@target")[0] if name_pers.xpath("./ptr[@type='wikidata']/@target") else None
        ))

# On boucle sur chaque élément 'place' contenu dans un 'listPlace' correspondant à un lieu.

    for name_lieu in tei_corpus.xpath("//listPlace/place"):

        lieu_xmlref = name_lieu.xpath("./@xml:id")
        lieu_ref = '#' + lieu_xmlref[0]

        db.session.add(Lieux(
            xml_ref_lieu = name_lieu.xpath("./@xml:id")[0] if name_lieu.xpath("./@xml:id") else None,
            name_lieu = name_lieu.xpath("./placeName/text()")[0] if name_lieu.xpath("./@xml:id") else None,
            longitude = name_lieu.xpath(".//long/text()")[0] if name_lieu.xpath(".//long/text()") else None,
            latitude = name_lieu.xpath(".//lat/text()")[0] if name_lieu.xpath(".//lat/text()") else None,
            pays = name_lieu.xpath(".//country/text()")[0] if name_lieu.xpath(".//country/text()") else None
            ))

# La méthode .commit() permet les requêtes nécessaires pour faire les ajouts dans les tables.

    db.session.commit()