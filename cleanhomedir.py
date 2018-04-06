#! python3

import shutil
import sys
import os
from datetime import datetime

USER = 'Invité'

def renvoieDate(tstamp):
    """Renvoyer un objet datetime depuis un timestamp"""
    return datetime.fromtimestamp(tstamp)

if __name__ == '__main__':

	# retourner un objet date correspondant à la duree (s) depuis 
	# aujourd'hui 8:00 (matin)
    m = datetime.now()
	
	# Recuperer la duree en secondes depuis une date donnee
    duree = ((m - datetime(m.year, m.month, m.day, 8, 0, 0)).
      total_seconds()
    )
	  
	# Instancier un objet date d'aujourd'hui 8h à partir de la variable 'm'
	#   m = datetime.now()
    cematin8h = datetime(m.year, m.month, m.day, 8, 0, 0)
    #	
	# st_ctime, st_mtime... renvoient des timestamps
	# convertir un timestamp en date : 
	#   createdate = datetime.fromtimestamp(object.st_[a,c,m]time))
	# Faire un timedelta avec date calculée plus haut :
    #   diff = createdate - cematin8h
	# On peut aussi comparer les 2 dates et obtenir un booléen :
	#   cematin8h < createdate

    #with open('c:\\Users\\moi\\Documents\\sortie.txt', 'a') as fic:
	#	fic.write('Salut\n')
    rep_exp = 'c:\\Users\\moi\\Documents'
	
    for dossier, sousdossiers, fichiers in os.walk(rep_exp, topdown=True):
        dossierstat = os.stat(dossier)
        createdossier = renvoieDate(dossierstat.st_ctime)
        modifdossier = renvoieDate(dossierstat.st_mtime)
        accessdossier = renvoieDate(dossierstat.st_atime)
        if createdossier > cematin8h:
            print ('dossier parcouru : {}'.format(dossier,))
            print('dernier acces : {} derniere modif : {}\n date creation : {}'.
              format(createdossier, modifdossier, accessdossier,))
            print('sous-dossiers : {}\nfichiers : {}'.
              format(dossier, sousdossiers, fichiers))