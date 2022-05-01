# import des libraries
from flask import render_template, Flask, request, url_for, flash, redirect, send_file
from flask_login import login_user, current_user, logout_user, login_required
from lxml import etree as ET
from flask_sqlalchemy import SQLAlchemy
from warnings import warn
import random
from SPARQLWrapper import SPARQLWrapper, JSON


# import de l'application depuis app
from ..app import app, login
# import des variables CORPUS, XSLT_PLACE, XSLT_NAME, ITEM, PERS depuis le fichier constantes
from ..constantes import CORPUS, XSLT_PLACE, XSLT_NAME, PERS, ITEM
# import de la fonction db_init depuis le fichier donnees
from ..modeles.donnees import db_init

# import de la classe HumCorr depuis le fichier donnees
from ..modeles.donnees import HumCorr, Personnes, Lieux
from ..modeles.utilisateurs import User



# activation de la fonction db_init lançant la base de données
db_init(CORPUS)


docs = HumCorr.query.all()
lettre = []


# Route vers la page d'accueil
@app.route("/")
def accueil():
    return render_template("pages/accueil.html", nom="Accueil", docs=docs)


# Route vers l'index de lieux
@app.route("/index_lieux")
def index_lieu():
    transform_place = ET.XSLT(XSLT_PLACE)
    index_Place = transform_place(CORPUS)
    return render_template("pages/indexPlace.html", nom="Index de lieux", index_Place=index_Place)


# Route vers l'index de personnes
@app.route("/index_personnes")
def index_noms():
    transform_nameIndex = ET.XSLT(XSLT_NAME)
    index_Name = transform_nameIndex(CORPUS)
    return render_template("pages/indexPersonne.html", nom="Index des personnes", index_Name=index_Name)


# Route vers le sommaire de toutes les lettres présentes dans la base
@app.route("/sommaire")
def corpus_entier():
    list_mois = {'01':'Janvier',
                 '02':'Février',
                 '03':'Mars',
                 '04':'Avril',
                 '05':'Mai',
                 '06':'Juin',
                 '07':'Juillet',
                 '08':'Août',
                 '09':'Septembre',
                 '10':'Octobre',
                 '11':'Novembre',
                 '12':'Décembre' }
    month = []
    return render_template("pages/indexgeneral.html", nom="Sommaire", docs=docs, mois=list_mois, month=month)


# Route vers l'affichage des lettres en fonction de leur identifiant
@app.route("/item/<int:lettre_ID>")
@login_required
def pub(lettre_ID):
    if (0 < lettre_ID <= len(docs)):
        t_pot = len(docs) + -1
        doc_xsl = ET.XSLT(ITEM)
        sortie = doc_xsl(CORPUS, numero=str(lettre_ID))
        nbrelettre = len(docs)
        return render_template("pages/lettre.html",
                               lettre_txt = sortie,
                               lettre_ID = lettre_ID,
                               docs = docs,
                               nbrelettre = nbrelettre,
                               t_pot = t_pot)
    else:
        return page_not_found(404)


# Route vers les pages de présentation de chaque personne présente dans la base
@app.route("/pers/<string:idperson>")
@login_required
def person(idperson):
    doc_xsl = ET.XSLT(PERS)
    sortie = doc_xsl(CORPUS, idpers=str(idperson))
    data = Personnes.query.filter(Personnes.xml_ref_person == idperson).all()
    if data:
        pers_info = []
        for personne in data:
            pers_info.append(personne.name_person)
            pers_info.append(personne.person_image)
            pers_info.append(personne.naissance)
            pers_info.append(personne.mort)
            pers_info.append(personne.wiki)
            pers_info.append(personne.id_wikidata)
            nomImage = pers_info[1]
            print(pers_info[3])
            wikidataId=pers_info[5]
            if wikidataId != None :
                # requete SPARQL pour récupérer une description des personnes
                wikidataId = 'wd:'+wikidataId
                endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
                sparql = SPARQLWrapper(endpoint)
                sparql.setQuery(
                    """
                PREFIX bd: <http://www.bigdata.com/rdf#> 
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                PREFIX schema: <http://schema.org/> 
                PREFIX wd: <http://www.wikidata.org/entity/> 
                PREFIX wikibase: <http://wikiba.se/ontology#> """
                    +
                    """
                    SELECT ?personLabel ?personDesc
                    WHERE {
                      SERVICE wikibase:label {
                        bd:serviceParam wikibase:language "fr" .
                        """ + wikidataId +
                    """ rdfs:label ?personLabel .
    
                    """ + wikidataId + """ schema:description ?personDesc .
                  }
                }
                """)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                print(results)
                desc = results['results']['bindings'][0]['personDesc']['value']

            else :
                desc = 'None'


        return render_template("pages/item_person.html",
                               personxsl = sortie,
                               idperson = idperson,
                               pers_info = pers_info,
                               nomImage = nomImage,
                               desc = desc)
    else:
        return render_template('pages/404.html', nom = "404 - Page non trouvée"), 404



# Route vers les pages de présentation de chaque lieu présent dans la base
@app.route("/place/<string:idlieu>")
@login_required
def place(idlieu):
    data = Lieux.query.filter(Lieux.xml_ref_lieu == idlieu).all()
    if data :
        lieu_info = []
        for lieu in data :
            lieu_info.append(lieu.name_lieu)
            lieu_info.append(lieu.longitude)
            lieu_info.append(lieu.latitude)
            lieu_info.append(lieu.pays)

            lon = lieu_info[1]
            lon = str(lon)
            lat = lieu_info[2]
            lat = str(lat)

        return render_template('pages/item_place.html',
                               lieu_info = lieu_info,
                               idlieu = idlieu,
                               lon = lon,
                               lat = lat)
    else:
        return render_template('pages/404.html', nom="404 - Page non trouvée"), 404



# Route vers la galerie présentant chaque personne présente dans la base
@app.route("/galerie")
def galerie():
    profils = Personnes.query.order_by(Personnes.person_image.desc()).all()
    return render_template("pages/galerie.html",
                           personnes = profils)



# Route pour la carte représentant tout les lieux présents dans la base
@app.route("/map")
def map():
    localisations = Lieux.query.all()
    return render_template("pages/map.html",
                           nom = "Carte",
                           lieux = localisations)


# Route pour le formulaire d'inscription
# Le succès ou les erreurs sont gérés avec flash
@app.route("/inscription", methods = ["GET", "POST"])
def inscription():
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


# Route pour permettre la connexion de l'utilisateur
# On vérifie d'abord que l'utilisateur n'est pas déjà connecté, il en est informé avec flash
# Quand le formulaire est envoyé, flash informe du succès ou des erreurs survenues
# Si la connexion est effectuée, l'utilisateur est renvoyé vers la page d'accueil
@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login = request.form.get("login", None),
            motdepasse = request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")

login.login_view = 'connexion'


# Route pour permettre la déconnexion
@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")


# Route pour le téléchargement du fichier XML-TEI
@app.route('/download/TEI')
def TEI_download():
    TEI = 'App/static/xml/corpus_humanistes.xml'
    return send_file(TEI,
                     attachment_filename = 'corpus_humanistes.xml',
                     as_attachment = True)


# Route pour le téléchargement du fichier sqlite généré à partir du fichier XML
@app.route('/download/bdd')
def bdd_download():
    bdd = 'db_hum.sqlite'
    return send_file(bdd,
                     attachment_filename = 'bdd_humanista',
                     as_attachment = True)


# Route de l'erreur 404.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html', nom = "404 - Page non trouvée"), 404


# Route de la simulation d'erreur 404.
@app.route('/error/HyperTextCoffeePotControlProtocol/supercalifragilisticexpialidocious/418')
def teapot():
    tpot_pict = random.randint(1, 15)
    return render_template('pages/418.html',
                           nom = 'Erreur 418',
                           tpot_pict = tpot_pict)

# Ce if permet de vérifier que ce fichier est celui qui est courrament exécuté. Cela permet par exemple d'éviter
# de lancer une fonction quand on importe ce fichier depuis un autre fichier.
# En python, lorsque l'on exécute un script avec la commande `python script.py`
# Le fichier `script.py` a en __name__ la valeur __main__.
if __name__ == "__main__":
    app.run()