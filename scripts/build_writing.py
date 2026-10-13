#!/usr/bin/env python3
"""Build the portfolio and Markdown writing archive into a publish-only directory."""
import argparse
import datetime as dt
import html
import re
import shutil
from pathlib import Path
from xml.etree import ElementTree as ET

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://doczbs.github.io'

def esc(value):
    return html.escape(str(value), quote=True)

def shell(title, description, body, route):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Boshi Zhang</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{URL}{route}"><link rel="icon" href="/assets/compass.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="Boshi Zhang · Writing" href="/writing/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
<script>try{{var t=localStorage.getItem('voyage-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="/writing/theme.css"><link rel="stylesheet" href="/writing/writing.css"><script src="/writing/writing.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="mast"><a class="name" href="/">Boshi Zhang<span>THE RESEARCH VOYAGE</span></a><nav aria-label="Main navigation"><a href="/">Home</a><a href="/writing/" aria-current="{'page' if route == '/writing/' else 'false'}">Writing</a><button type="button" data-theme-toggle aria-label="Switch colour theme">Night</button></nav></header>
<main id="main">{body}</main>
<footer><span>Boshi Zhang · Notes along the way</span><div><a href="/writing/feed.xml">RSS ↗</a><a href="/">Back to home ↗</a></div></footer></body></html>'''

def build(out):
    out.mkdir(parents=True, exist_ok=True)
    for name in ['index.html', 'style.css', 'motion.js', '.nojekyll']:
        if (ROOT/name).exists(): shutil.copy2(ROOT/name, out/name)
    shutil.copytree(ROOT/'assets', out/'assets', dirs_exist_ok=True)
    dest=out/'writing'
    # Only the generated Writing directory is replaced; published source never contains drafts.
    if dest.exists(): shutil.rmtree(dest)
    dest.mkdir()
    for name in ['writing.css','writing.js']:
        shutil.copy2(ROOT/'writing'/name,dest/name)
    homepage=(ROOT/'index.html').read_text()
    (dest/'theme.css').write_text(homepage[homepage.index(':root {'):homepage.index('/* ===== Base ===== */')])
    posts=[]
    for path in (ROOT/'content/posts').glob('*.md'):
        text=path.read_text()
        parts=text.split('---',2)
        if len(parts)!=3 or parts[0].strip(): raise ValueError(f'{path.name}: YAML frontmatter required')
        meta=yaml.safe_load(parts[1]) or {}
        if meta.get('draft',True) is not False: continue
        slug=path.stem
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug): raise ValueError(f'Invalid slug: {slug}')
        title=meta.get('title','').strip()
        if not title: raise ValueError(f'{slug}: title required')
        date=dt.date.fromisoformat(str(meta['date']))
        kind=str(meta.get('kind','Essay'))
        if kind not in ['Essay','Research note','Field note']: raise ValueError(f'{slug}: unknown kind')
        md=markdown.Markdown(extensions=['extra','toc','sane_lists'],extension_configs={'toc':{'permalink':False}})
        content=md.convert(parts[2])
        words=len(re.findall(r'\w+|[\u4e00-\u9fff]',parts[2]))
        minutes=max(1,round(words/220))
        posts.append(dict(slug=slug,title=title,date=date,kind=kind,description=str(meta.get('summary','')),content=content,toc=md.toc if md.toc_tokens else '',minutes=minutes))
    posts.sort(key=lambda p:(p['date'],p['slug']), reverse=True)
    rows=''
    year=None
    for p in posts:
        if p['date'].year!=year:
            if year is not None: rows+='</div>'
            year=p['date'].year
            rows+=f'<div class="year-group"><h3 class="year">{year}</h3>'
        rows+=f'''<article class="entry"><div class="entry-meta"><time datetime="{p['date']}">{p['date']:%b %d}</time><span>{esc(p['kind'])}</span></div><div><h3><a href="/writing/{p['slug']}/">{esc(p['title'])}</a></h3><p>{esc(p['description'])}</p></div><a class="entry-arrow" href="/writing/{p['slug']}/" aria-label="Read {esc(p['title'])}">↗</a></article>'''
    if year is not None: rows+='</div>'
    if not rows: rows='''<div class="empty"><span class="empty-mark" aria-hidden="true">✧</span><div><h3>The notebook is open.</h3><p>No published entries yet. Essays, research notes, and observations will appear here.</p></div></div>'''
    body=f'''<section class="writing-hero"><div><p class="eyebrow">WRITING · BOSHI ZHANG</p><h1>Notes from<br>the <em>voyage.</em></h1><p class="intro">Ideas in progress. Research in perspective.<br>A place to think beyond the paper.</p></div><div class="seal" aria-hidden="true"><img src="/assets/compass.svg" width="164" height="164" alt=""><span>OBSERVE · QUESTION · WRITE</span></div></section>
<section class="archive" aria-labelledby="archive-title"><div class="archive-head"><h2 id="archive-title">The notebook</h2><span>{len(posts):02d} {'entry' if len(posts)==1 else 'entries'}</span></div>{rows}</section>'''
    (dest/'index.html').write_text(shell('Writing','Essays, research notes and observations by Boshi Zhang.',body,'/writing/'))
    for i,p in enumerate(posts):
        route=f"/writing/{p['slug']}/"
        nextpost=posts[i+1] if i+1<len(posts) else None
        nextlink=f'<a href="/writing/{nextpost["slug"]}/">Next entry: {esc(nextpost["title"])} →</a>' if nextpost else '<a href="/writing/">All writing →</a>'
        toc=f'<aside class="contents"><p>ON THIS PAGE</p>{p["toc"]}</aside>' if p['toc'] else ''
        body=f'''<header class="post-head"><a class="back" href="/writing/">← The notebook</a><p class="eyebrow">{esc(p['kind'])} · <time datetime="{p['date']}">{p['date']:%B %d, %Y}</time> · {p['minutes']} MIN READ</p><h1>{esc(p['title'])}</h1><p class="dek">{esc(p['description'])}</p><p class="byline">Boshi Zhang</p></header><div class="reading-grid"><article class="prose">{p['content']}<nav class="post-end" aria-label="More writing">{nextlink}</nav></article>{toc}</div>'''
        target=dest/p['slug'];target.mkdir();(target/'index.html').write_text(shell(p['title'],p['description'],body,route))
    rss=ET.Element('rss',version='2.0');channel=ET.SubElement(rss,'channel')
    for key,value in [('title','Boshi Zhang · Writing'),('link',URL+'/writing/'),('description','Essays, research notes and observations.')]:ET.SubElement(channel,key).text=value
    for p in posts:
        item=ET.SubElement(channel,'item')
        for key,value in [('title',p['title']),('link',URL+'/writing/'+p['slug']+'/'),('guid',URL+'/writing/'+p['slug']+'/'),('description',p['description']),('pubDate',p['date'].strftime('%a, %d %b %Y 00:00:00 +0800'))]:ET.SubElement(item,key).text=value
    ET.ElementTree(rss).write(dest/'feed.xml',encoding='utf-8',xml_declaration=True)
    print(f'Built {len(posts)} published entries into {out}')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=ROOT/'_site');parser.add_argument('--new',help='Create a Markdown draft with this URL slug');args=parser.parse_args()
    if args.new:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',args.new):parser.error('Use a lowercase hyphenated slug')
        p=ROOT/'content/posts'/f'{args.new}.md'
        with p.open('x') as f:f.write(f'---\ntitle: "Untitled"\ndate: {dt.date.today()}\nkind: Essay\nsummary: ""\ndraft: true\n---\n\nWrite here.\n')
        print(f'Draft created: {p}')
    else: build(args.out.resolve())
