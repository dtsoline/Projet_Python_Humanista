from warnings import warn
from lxml import etree as ET

SECRET_KEY = "JE SUIS UN SECRET !"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Il serait plus sage de changer la clé secrète !", Warning)

# le fichier XML contenant les informations nécessaires à l'application
# est parsé par lxml en utilisant la méthode .parse() de etree.
CORPUS = ET.parse("App/static/xml/corpus_humanistes.xml")


# les feuilles de transformation XSL sont parsées
ITEM = ET.parse("App/static/xsl/affichage_lettre.xsl")
PERS = ET.parse("App/static/xsl/item_pers.xsl")
XSLT_PLACE = ET.parse("App/static/xsl/index_lieux.xsl")
XSLT_NAME = ET.parse("App/static/xsl/index_personnes.xsl")



