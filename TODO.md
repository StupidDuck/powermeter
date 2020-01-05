Procfile:
before : logout all users
  => backup the actual DB !
after : migrate db script (erase / recreate DB + import data)

Pas de reload apres la suppression d'un mr

STAGING BRANCH ON GITHUB
MASTER = heroku stable