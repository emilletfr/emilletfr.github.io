#!/usr/bin/env python3
"""Aligne les textes du site appseven.fr sur les descriptions de fiches stores.

Source unique de vérité : le dépôt APP —
`script/assets/ios/lite/store/metadata/<locale>/description.txt` —
une seule rédaction par langue sert au store ET au site (doctrine du README).

Usage :
    python3 script/align_texts_from_store.py --check            # montre les diffs
    python3 script/align_texts_from_store.py --write [lang ...] # réécrit

Ce qui est régénéré (au caractère près, avec asserts sur la structure) :
- pages descriptifs : lede + sections + liste « pour commencer » + citation
  (l'en-tête de page et le bloc légal du .txt sont conservés/ignorés) ;
- pages vitrines : h1 + lede du héros, les trois cartes « Pourquoi ? »
  (sept langues, erreurs, progression), « POUR QUI ? » et la citation.
Le reste des vitrines (kicker, badges, captures, libellés propres au site)
n'est jamais touché.
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
BASE = Path.home() / 'Desktop' / 'temp'
STORE = BASE / 'code_flutter_idictee' / 'script' / 'assets' / 'ios' / 'lite' / 'store' / 'metadata'

# lang, locale du dépôt app, page descriptif, page vitrine (chemins site)
LANGS = [
    ('fr', 'fr-FR', 'iDictee.md', 'index.md'),
    ('de', 'de-DE', 'de/beschreibung/index.md', 'de/index.md'),
    ('es', 'es-ES', 'es/descripcion/index.md', 'es/index.md'),
    ('it', 'it', 'it/descrizione/index.md', 'it/index.md'),
    ('pl', 'pl', 'pl/opis/index.md', 'pl/index.md'),
    ('en', 'en-US', 'en/description.md', 'en/index.md'),
    ('pt', 'pt-BR', 'pt/descricao.md', 'pt/index.md'),
]

# Indices des sections (0 = « sept langues ») utilisées par les vitrines.
CARDS = [0, 5, 7]     # sept langues, erreurs, progression
AUDIENCE = 9          # « POUR QUI ? »
SECTIONS_ATTENDUES = 10


def parse_description(path):
    """Décompose un description.txt en (p1, sections, en-tête puces, puces, citation)."""
    blocks = re.split(r'\n\s*\n', path.read_text(encoding='utf-8').strip())
    legal = [b for b in blocks if b.startswith('EULA')]
    assert len(legal) == 1, f'{path} : bloc légal introuvable ou multiple'
    blocks = blocks[:blocks.index(legal[0])]

    p1 = blocks[0].strip()
    sections, bullets, quote = [], [], None
    bullets_header = None
    for block in blocks[1:]:
        lines = [l.rstrip() for l in block.split('\n') if l.strip()]
        assert lines, f'{path} : bloc vide inattendu'
        if len(lines) >= 2 and lines[1].startswith('• '):
            assert all(l.startswith('• ') for l in lines[1:]), f'{path} : liste hétérogène'
            bullets_header = lines[0]
            bullets = [l[2:].strip() for l in lines[1:]]
        elif len(lines) == 1:
            assert quote is None, f'{path} : plusieurs citations ?'
            quote = lines[0]
        else:
            sections.append((lines[0], ' '.join(lines[1:]).strip()))

    assert len(sections) == SECTIONS_ATTENDUES, f'{path} : {len(sections)} sections (attendu {SECTIONS_ATTENDUES})'
    assert bullets and len(bullets) >= 8, f'{path} : {(len(bullets) if bullets else 0)} puces'
    assert quote, f'{path} : citation manquante'
    return p1, sections, bullets_header, bullets, quote


def first_sentence(text):
    m = re.match(r'^(.*?\.)\s+(.*)$', text, re.S)
    assert m, f'séparation h1/lede impossible : {text[:60]!r}'
    return m.group(1), m.group(2)


def drop_last_sentence(text):
    parts = re.split(r'(?<=\.)\s+', text)
    return ' '.join(parts[:-1]) if len(parts) > 1 else text


def sub_once(pattern, repl, text, what):
    new, n = re.subn(pattern, repl, text)
    assert n == 1, f'{what} : {n} occurrence(s)'
    return new


def rebuild_descriptif(path, p1, sections, bullets_header, bullets, quote):
    """Ne touche que le corps après le <h1> (en-tête YAML et h1 conservés)."""
    text = path.read_text(encoding='utf-8')
    cut = text.index('<p class="lede">')
    body = [f'<p class="lede">{p1}</p>', '']
    for header, paragraph in sections:
        body += [f'<h3>{header}</h3>', f'<p>{paragraph}</p>', '']
    body += [f'<h3>{bullets_header}</h3>', '<ul>']
    body += [f'<li>{b}</li>' for b in bullets]
    body += ['</ul>', '', f'<blockquote class="quote"><p>{quote}</p></blockquote>', '']
    text = text[:cut] + '\n'.join(body)
    return sub_once(r'(meta_description:\s*")(.*?)(")',
                    lambda m: m.group(1) + drop_last_sentence(p1) + m.group(3),
                    text, 'meta_description (descriptif)')


def rebuild_vitrine(path, p1, sections, bullets_header, bullets, quote):
    text = path.read_text(encoding='utf-8')
    h1, lede = first_sentence(p1)
    assert '"' not in lede, 'lede avec guillemet droit : casserait le YAML'

    text = sub_once(r'(<h1>)(.*?)(</h1>)', lambda m: m.group(1) + h1 + m.group(3), text, 'h1 vitrine')
    text = sub_once(r'(<p class="lede">)(.*?)(</p>)', lambda m: m.group(1) + lede + m.group(3), text, 'lede vitrine')

    cards = list(re.finditer(r'(<div class="card">\s*<h3>)(.*?)(</h3>\s*<p>)(.*?)(</p>\s*</div>)', text, re.S))
    assert len(cards) == 3, f'{path} : {len(cards)} carte(s)'
    for m, idx in zip(reversed(cards), reversed(CARDS)):
        header, paragraph = sections[idx]
        text = text[:m.start()] + m.group(1) + header + m.group(3) + paragraph + m.group(5) + text[m.end():]

    header, paragraph = sections[AUDIENCE]
    text = sub_once(
        r'(<p class="audience"><strong>)(.*?)(</strong>)(.*?)(</p>)',
        lambda m: m.group(1) + header + m.group(3) + paragraph + m.group(5),
        text, 'audience vitrine')
    text = sub_once(r'(<blockquote class="quote">\s*<p>)(.*?)(</p>)',
                    lambda m: m.group(1) + quote + m.group(3), text, 'citation vitrine')
    text = sub_once(r'(meta_description:\s*")(.*?)(")',
                    lambda m: m.group(1) + lede + m.group(3), text, 'meta_description (vitrine)')
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('langs', nargs='*', help='restreindre à certaines langues')
    args = ap.parse_args()

    print(f'── {"ÉCRITURE" if args.write else "VÉRIFICATION"} ──')
    changed = 0
    for lang, locale, descriptif_rel, vitrine_rel in LANGS:
        if args.langs and lang not in args.langs:
            continue
        p1, sections, bullets_header, bullets, quote = parse_description(
            STORE / locale / 'description.txt')
        jobs = [
            (descriptif_rel, lambda p, _rel=descriptif_rel: rebuild_descriptif(
                p, p1, sections, bullets_header, bullets, quote)),
            (vitrine_rel, lambda p, _rel=vitrine_rel: rebuild_vitrine(
                p, p1, sections, bullets_header, bullets, quote)),
        ]
        for rel, rebuild in jobs:
            path = SITE / rel
            before = path.read_text(encoding='utf-8')
            after = rebuild(path)
            if before == after:
                print(f'{lang:3} {rel:32} à jour')
                continue
            changed += 1
            diff = list(difflib.unified_diff(before.splitlines(), after.splitlines(), lineterm='', n=0))
            added = len([d for d in diff if d.startswith('+') and not d.startswith('+++')])
            print(f'{lang:3} {rel:32} {added} ligne(s) à mettre à jour')
            for line in diff[2:8]:
                print('      ' + line[:150])
            if args.write:
                path.write_text(after, encoding='utf-8')
    if args.write:
        print(f'terminé : {changed} fichier(s) réécrit(s)')
    else:
        print(f'{changed} fichier(s) à réécrire (relancer avec --write)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
