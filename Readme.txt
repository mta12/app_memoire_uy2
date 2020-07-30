APP WEB

https://getbootstrap.com/docs/4.0/components/

- on veut lister les travaux dans l'UY2 
- memoires -- Master et these, en cours et soutenus, 
- memoires en cours: 
    
    - theme, 
    - etudiant (matricule, nom complet, date de naissance, 
    region d'origine)
    - Encadreurs ou superviseurs: liste d'Enseignant (titre, nomcomplet)
    - Date de sélection
    - type: Master 2 academique ou professionnel, ou these de Doctorat 
- memoires soutenus 
    - memoire en cours 
    - Date de soutenance
    - Lieu de soutenance  
    - membres du jury: liste d'Enseignant (titre, nomcomplet)
    - Note de soutenance 
    - Résume du memoire 
    - Lien d'acces au memoire 

****************************************************************

LES FONCTIONNALITES (Utiliser un theme simple)
- créer les différents modèles (Document, Enseignant, Etudiant, Personne)----------- OK
- Afficher la liste des documents initiale -- OK
    - Les tests 
        TEST DES VUES 
            tester l'affichage des documents récents -- OK
            TestDocumentIndexView -- OK
            TestDocumentDetailsView -- OK 
            TestDocumentResultView -- 
                - pas de resultats 
                - tous les docs vieux 
                - pas de docs du future 
        TEST DES MODELES 
            Les futures publications ne doivent pas être considérées comme récentes -- OK
            Les publication de plus d'un jour aussi -- OK
            Les publications de 1 jour au plus sont récentes -- OK
- charger les modeles via csv avec l'admin et la console
    - via la console -- 
        err: TypeError: Field 'id' expected a number but got <Personne: Mekou nama>.
        ./manage.py test main.tests.test_models.TestImportDoc

    - via l'admin -- 

- Introduire la pagination à 10 éléments dans les vues et interfaces 
    
- Introduire la fonctionnalité de recherche avec fonction avancée: par etab, 
par type de document, (On pourra mettre cela dans des menus )
    - Recupérer la requête 
    - Traiter la requet
    - Retourner le résultat  
    - la recherche doit être récursive selon les infos transmits par le user 
- gérer les users et droits d'accès coté admin 
- utiliser un template simple et du bootstrap pour les boutons. 
- Deployer le système 

****************************************************************

- gérer la recherche + tests 
- gerer les sessions: quand on clique sur un détails on peut revenir là ou on était + test 
- les tests des vues 
- le look and feel (home, recherche, details, Apropos)
- corriger la pagination 
- déployer 

********************* IMPORTATION -- OK
importation des documents: 
- testons la lecture du fichier 
- testons la recupération du contenu (affichage à l'écran)
- testons la création 

********************* LA PAGINATION -- OK
- pagination dans les resultats (bon)
    Il fallait ajouter la query dans l'url de la pagination 
    pui définir un get_context dans la vue 
- test de pagination 

********************* LA RECHERCHE 
recherche de documents 
- recherche par mot clés - test
    - gérer la recherche avec accent -- ok
- introduire la recherche avancée  et testons (plus tard)

******************* FINIR LES INTERFACES ET DEPLOYER (déployer et présenter avant de revenir)
- Le look est bon pour un prototype 

*** IL faut déployer maintenant (AVANT DE CONTINUER)
Heroku
    - git config --global user.name "mta12"
    - git config --global user.email "tobiemanga@gmail.com"
    - git init Mytest
    - cd 
    - git add -A 
    - git commit -m "some_message"
    - create a repo 
    - git remote add origin https://github.com/mta12/app_memoire_uy2.git
    - git push origin master
(Préparer le code en local avant de le déployer utiliser django for begi et practical djanA)

