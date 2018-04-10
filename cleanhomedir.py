#! python

# Script permettant de nettoyer un repertoire utilisateur en fonction d'une
# et du matin 8h.
# Ce fonctionnement permet a priori de supprimer tout ce qui a ete cree
# dans la journee sur un poste de travail.
# Ce script etant destine a des postes de pret, les sessions sont normalement
# fermees chaque soir.
# Il est destine a etre place de le repertoire d'execution de "logout" de 
# maniere a nettoyer systematiquement les sessions utilisateurs du poste
# de pret.
# Il peut aussi etre execute manuellement par un administrateur du systeme.

import shutil
import sys
import os
from datetime import datetime
from zipfile import ZipFile
#import cgitb
#cgitb.enable(format='text')

USER = 'moi'

def syntax():
    pass

def cmd_line(args):
    pass

def renvoieDate(tstamp):
    """Renvoyer un objet datetime depuis un timestamp"""
    return datetime.fromtimestamp(tstamp)

if __name__ == '__main__':

    # retourner un objet date correspondant a la duree (s) 
    # depuis aujourd'hui 8:00 (matin)
    m = datetime.now()
    
    # Recuperer la duree en secondes depuis une date donnee
    # duree = ((m - datetime(m.year, m.month, m.day, 8, 0, 0)).        
    #  total_seconds()
    # )
	  	
    # Instancier un objet date d'aujourd'hui 8h a partir de la variable 'm'
    #   m = datetime.now()
    cematin8h = datetime(m.year, m.month, m.day, 8, 0, 0)
    #	
    # st_ctime, st_mtime... renvoient des timestamps
    # convertir un timestamp en date : 
    #   createdate = datetime.fromtimestamp(object.st_[a,c,m]time))
    # Faire un timedelta avec date calculee plus haut :
    #   diff = createdate - cematin8h
    # On peut aussi comparer les 2 dates et obtenir un booleen :
    #   cematin8h < createdate

    # with open('c:\\Users\\moi\\Documents\\sortie.txt', 'a') as fic:
    #	fic.write('Salut\n')
    rep_exp = os.path.join('c:', os.sep, 'Users', USER, 'Documents')
	
    # tableau qui contient les noms de dossier deja identifies comme
    # modifies et archives qui permet d'eviter le traitement 
    # de l'un de leurs sous-repertoires et d'avoir la liste pour
    # pour post-traitements (archivage, suppression)
    dossiers_deja_identif = []
    # Idem pour les fichiers
    fichiers_deja_identif = []

    for dossier, sousdossiers, fichiers in os.walk(rep_exp, topdown=True):
        #print("{}\n, {}\n, {}".format(dossier, sousdossiers, fichiers,))
        bool_dossier = False
        t_sousdossiers = []
        t_fichiers = []
        # On commence par verifier si le dossier parent n'a pas deja
        # ete traite
        test = False
        for d in dossiers_deja_identif:
            if d in dossier:
                test = True
        if test:
            continue
        dossierstat = os.stat(dossier)
        createdossier = renvoieDate(dossierstat.st_ctime)
        modifdossier = renvoieDate(dossierstat.st_mtime)
        accessdossier = renvoieDate(dossierstat.st_atime)
        if (createdossier or modifdossier or accessdossier) > cematin8h:
            bool_dossier = True
            dossiers_deja_identif.append(dossier)
        for s in sousdossiers:
            sabs = os.path.join(dossier, s)
            s_stat = os.stat(sabs)
            s_create = renvoieDate(s_stat.st_ctime)
            s_modif = renvoieDate(s_stat.st_mtime)
            s_access = renvoieDate(s_stat.st_atime)
            if (s_create or s_modif or s_access) > cematin8h:
                t_sousdossiers.append(sabs)
        for f in fichiers:
            fabs = os.path.join(dossier, f)
            fstat = os.stat(fabs)
            f_create = renvoieDate(fstat.st_ctime)
            f_modif = renvoieDate(fstat.st_mtime)
            f_access = renvoieDate(fstat.st_atime)
            if (f_create or f_modif or f_access) > cematin8h:
                t_fichiers.append(fabs)
        if bool_dossier:
            print('\nDossier ajoute/modifie/accede : "{}"'.
                    format(dossier))
            continue
        else :
            print('\nPas de modification sur "{}"'.format(dossier,))
        if len(t_sousdossiers) > 0:
            print("Sous-dossiers de {} ajoutes/modifies/supprimes :\n{}".
                    format(dossier, t_sousdossiers,))
        else:
            print('Pas de sous-dossiers ajoutes/modifies/supprimes dans "{}"'.
                    format(dossier,))
        if len(t_fichiers) > 0:
            print("Fichiers de {} ajoutes/supprimes/modifies :\n{}\n".
                    format(dossier, t_fichiers,))
            for t in t_fichiers:
                fichiers_deja_identif.append(t)
        else:
            print('Pas de fichiers ajoutes/modifies/supprimes dans "{}\n"'.
                    format(dossier,))

        del bool_dossier, t_sousdossiers, t_fichiers

    # Y a-t-il qque chose a archiver ?
    flag_dossier = False
    flag_fichier = False

    if len(dossiers_deja_identif) > 0:
        print('Dossiers a archiver :\n{}'.format(dossiers_deja_identif,))
        flag_dossier = True

    if len(fichiers_deja_identif) > 0:
        print('Fichiers a archiver :\n{}'.format(fichiers_deja_identif,))
        flag_fichier = True

    if flag_dossier or flag_fichier:
        # S'il faut archiver, on cree un fichier archive 
        # (nomprofil_date.zip)
        # le nom...
        f_archive = os.path.join("c:", os.sep, "temp", USER + 
                str(m.year) + str(m.month) + str(m.day) + str(m.hour) + 
                str(m.minute) + str(m.second) + ".zip")
    
        # ... le fichier lui-meme.
        try:
            f = open(f_archive, 'w') 
        except:
            pass
        else:
            f.close()
    
    if flag_fichier:
        # On archive les fichiers
        for f in fichiers_deja_identif:
            with ZipFile(f_archive, 'a') as myzip:
                myzip.write(f)

