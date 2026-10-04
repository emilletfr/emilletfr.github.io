# appseven.fr — site vitrine

Site statique (Jekyll) d'AppSeven, publié sur GitHub Pages — domaine
`www.appseven.fr` (voir `CNAME`).

## Structure

- `index.md` — accueil vitrine (iDictée)
- `iDictee.md` — page iDictée (`/idictee/`)
- `contact.html` — formulaire (Formspree)
- `privacyPolicy-*.md` — pages de confidentialité, une par app et par
  plateforme — en **français**, sauf `privacyPolicy-iDiktat.md` (allemand,
  pour la fiche iDiktat)
- `404.md`, `thanks.md`
- `css/site.css` — feuille de style unique
- `_layouts/`, `_includes/` — gabarits Jekyll
- `images/` — logos et captures d'app (`images/shots/` : captures générées
  depuis le dépôt de l'app, `script/render_store_screenshots.py` côté app)

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
Langue du site : français.
