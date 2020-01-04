Procfile:
before : logout all users
  => backup the actual DB !
after : migrate db script (erase / recreate DB + import data)

link in menu to change graph or list, only change #list or #graph