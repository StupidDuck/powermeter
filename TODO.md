Procfile:
before : logout all users
  => backup the actual DB !
after : migrate db script (erase / recreate DB + import data)

STAGING BRANCH ON GITHUB
MASTER = heroku stable

todo : unifier la facon dont le controlleur exporte ces variables : meter_id ou data.meter_id, journal, etc...
unifier les espaces / tab : 2 / 4 ...

range des dates a afficher sur le graph (filtre ?)
traitement de l'affichage des données (mise en forme des dates, ...) de la vue liste

CSS => responsive design !

dans main.py, tous les if / else => try /except ?

Show loading asset when importing / deleting / etc...