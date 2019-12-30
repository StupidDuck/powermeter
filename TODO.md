Procfile:
before : logout all users
  => backup the actual DB !
after : migrate db script (erase / recreate DB + import data)

make this a thin layer on top of postgresql, business logic moves to JS (PWA)
remplacer flash et render_template par du JS / JSON ?
supprimer le endpoint : /meter/<int:meter_id>/json => faire tout en JS via @app.route('/meter/<int:meter_id>/journal')
passer tout les link rel .js => import webpack

BUT => faire une SPA pour la partie graph / list (pas de chargement de page entre les deux vues...)
ATTENTION : essayer de rester le plus proche du web standard : le plus static possible, pas de SPA...