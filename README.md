# appseven.fr — site vitrine

Site statique (Jekyll) d'AppSeven, publié sur GitHub Pages — domaine
`www.appseven.fr` (voir `CNAME`).

## Structure

- `index.md` — accueil vitrine (iDictée)
- `iDictee.md` — page iDictée (`/idictee/`)
- `contact.html` — formulaire (Formspree)
- `en/`, `pt/` — sections anglaise (iDictation) et portugaise (iDitado) :
  accueil, descriptif (`/en/description/`, `/pt/descricao/`), contact et
  remerciement dédiés
- `privacyPolicy-*.md` — pages de confidentialité, une par app et par
  plateforme — en **français**, sauf `privacyPolicy-iDiktat.md` (allemand,
  pour la fiche iDiktat), `privacyPolicy-iDictation.md` (anglais) et
  `privacyPolicy-iDitado.md` (portugais)
- `404.md`, `thanks.md`
- `css/site.css` — feuille de style unique
- `_layouts/`, `_includes/` — gabarits Jekyll
- `images/` — logos et captures d'app (`images/shots/` : captures générées
  depuis le dépôt de l'app, `script/render_store_screenshots.py` côté app)

## Textes de la vitrine — alignés sur les fiches stores

Les textes de `index.md` proviennent **verbatim** des descriptions de fiches
(dépôt app : `script/assets/ios/lite/store/metadata/<lang>/description.txt`,
locale `fr-FR`). Une seule rédaction par langue sert ainsi au store **et** au
site. Pour ajouter une langue : reprendre les mêmes sections dans la
description de cette langue et créer la variante de page (ex. `/de/`).
Toute modification d'une description store se répercute ici — mêmes phrases,
au caractère près. Les libellés propres au site (« L'app en images »,
« Pourquoi iDictée ? », navigation) sont les seules chaînes à traduire à part.

## ⚠️ URL à ne jamais casser

Les fiches App Store / Google Play pointent vers
`/privacyPolicy-iDicteeFree/` (et variantes) : les `permalink:` des pages de
confidentialité **ne doivent pas changer** (exigence App Review). Toute
évolution d'une page légale se fait sur place.

## Prévisualiser en local

```sh
bundle install
bundle exec jekyll serve     # http://localhost:4000
```

## Publier

```sh
git push                     # GitHub Pages reconstruit automatiquement
```

Uniquement des plugins de la liste blanche GitHub Pages (ici : sitemap).
Langues du site : français (racine), de, es, it, pl, en, pt.
