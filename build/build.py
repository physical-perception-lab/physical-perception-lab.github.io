#!/usr/bin/env python3
"""Build script for Physical Perception Lab website.

Reads publication .txt files + people.json + HTML templates and generates
index.html, projects.html, and people.html.

Usage: python build/build.py  (from the ppl/ directory)
"""

import os
import json
import html as html_module

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, 'data')
PUB_DIR = os.path.join(DATA_DIR, 'publications')
TEMPLATE_DIR = os.path.join(ROOT, 'build', 'templates')

TOPIC_LABELS = {
    '3d-reconstruction': '3D Reconstruction',
    'neural-rendering': 'Neural Rendering',
    'robot-learning': 'Robot Learning',
    'physics-dynamics': 'Physics & Dynamics',
    'object-understanding': 'Object Understanding',
    'generative-models': 'Generative Models',
}

# Publication ordering — list of tuples: ('year', year_label, False) or (paper_id, is_new, is_selected)
PUBLICATIONS = [
    ('year', '2026', False),
    ('icra26demodiffusion', True, True),
    ('iclr26crisp', True, False),
    ('3dv26haptic', True, False),
    ('year', '2025', False),
    ('iccv25lightswitch', True, True),
    ('corl25gen2act', True, False),
    ('cvpr25diffusionsfm', True, True),
    ('cvpr25uniphy', True, False),
    ('cvpr25aerialmegadepth', True, False),
    ('cvpr25turbo3d', True, True),
    ('cvpr25scenefactor', True, False),
    ('3dv25materialfusion', False, False),
    ('3dv25dressrecon', False, False),
    ('year', '2024', False),
    ('neurips24ags', False, True),
    ('eccv24track2act', False, True),
    ('eccv24upfusion', False, False),
    ('cvpr24ghop', False, True),
    ('cvpr24mvdfusion', False, False),
    ('iclr24rays', False, True),
    ('icra24hopman', False, True),
    ('icra24roboagent', False, False),
    ('3dv24relposepp', False, False),
    ('year', '2023', False),
    ('iccv23diffhoi', False, False),
    ('iccv23control', False, False),
    ('iccv23texture', False, False),
    ('icra23affordance', False, False),
    ('iclr23analogical', False, False),
    ('cvpr23sparsefusion', False, True),
    ('cvpr23affordance', False, False),
    ('year', '2022', False),
    ('neurips22dycheck', False, False),
    ('eccv22relpose', False, False),
    ('cvpr22ss3d', False, False),
    ('cvpr22ihoi', False, True),
    ('cvpr22autosdf', False, True),
    ('year', '2021', False),
    ('neurips21ners', False, True),
    ('neurips21nrns', False, False),
    ('corl21planar', False, False),
    ('iccv21act', False, True),
    ('icml21pixel', False, False),
    ('cvpr21mesh', False, False),
    ('year', '2020', False),
    ('neurips20audio', False, False),
    ('corl20vime', False, False),
    ('cvpr20acsm', False, False),
    ('cvpr20force', False, True),
    ('iclr20synergy', False, False),
    ('iclr20motor', False, False),
    ('icra20schema', False, False),
    ('year', '2019', False),
    ('corl19ocm', False, False),
    ('iccv19csm', False, True),
    ('iccv19cvp', False, False),
    ('iccv19relnet', False, False),
    ('iccv19craft', False, False),
    ('arxiv19mvs', False, False),
    ('year', '2018', False),
    ('eccv18lsi', False, False),
    ('eccv18cmr', False, True),
    ('cvpr18mvc', False, False),
    ('cvpr18f3d', False, False),
    ('year', '2017', False),
    ('cvpr17drc', False, True),
    ('cvpr17abstraction', False, True),
    ('3dv17hsp', False, False),
    ('year', '2016', False),
    ('pami16reconstruction', False, False),
    ('eccv16flow', False, False),
    ('year', '2015', False),
    ('iccv15pose', False, False),
    ('iccv15amodal', False, False),
    ('cvpr15vps', False, False),
    ('cvpr15csdm', False, True),
    ('cvpr15vvn', False, False),
    ('year', '2013', False),
    ('uist13colors', False, False),
]

# Keys that are not rendered as links
SKIP_LINK_KEYS = {'title', 'author', 'venue', 'img', 'imgbase', 'abstract', 'note', 'topics'}


def read_file(fpath):
    with open(fpath, 'r') as f:
        return f.read()


def parse_paper(paper_id):
    """Parse a publication .txt file and return a dict of fields."""
    fpath = os.path.join(PUB_DIR, paper_id + '.txt')
    elems = {}
    ordered_keys = []
    with open(fpath, 'r') as f:
        for ln in f:
            parts = ln.split('::', 1)
            if len(parts) != 2:
                continue
            key = parts[0].strip()
            val = parts[1].strip()
            elems[key] = val
            if key not in ('title', 'author', 'venue', 'img', 'imgbase'):
                ordered_keys.append(key)
    elems['_ordered_keys'] = ordered_keys
    return elems


def rewrite_img_path(img_path):
    """Rewrite figures/ paths to assets/figures/."""
    if img_path.startswith('figures/'):
        return 'assets/' + img_path
    if img_path.startswith('./figures/'):
        return 'assets/' + img_path[2:]
    return img_path


def make_media_tag(img_path, css_class, title=''):
    """Create an img or video tag based on file extension."""
    img_path = rewrite_img_path(img_path)
    alt = html_module.escape(title, quote=True)
    if img_path.endswith('.mp4') or img_path.endswith('.m4v'):
        return f'<video class="{css_class}" muted autoplay loop playsinline><source src="{img_path}" type="video/mp4"></video>'
    else:
        return f'<img class="{css_class}" src="{img_path}" alt="{alt}" loading="lazy">'


def bold_pi(author_str):
    """Bold the PI name in author string."""
    return author_str.replace('Shubham Tulsiani', '<strong>Shubham Tulsiani</strong>')


def build_project_card(paper_id, elems, is_new, current_year):
    """Build HTML for a project card on the projects page."""
    topics_str = elems.get('topics', '')
    topics_list = [t.strip() for t in topics_str.split(',') if t.strip()]

    s = f'<div class="card--project" id="{paper_id}" data-year="{current_year}" data-topics="{",".join(topics_list)}">\n'

    # Media
    if 'img' in elems:
        s += f'  <div class="card--project__media-wrap">\n'
        s += f'    {make_media_tag(elems["img"], "card--project__media", elems.get("title", ""))}\n'
        s += f'  </div>\n'

    # Body
    s += f'  <div class="card--project__body">\n'

    # Title
    s += f'    <div class="card--project__title">{elems.get("title", "")}</div>\n'

    # Authors
    s += f'    <div class="card--project__authors">{bold_pi(elems.get("author", ""))}</div>\n'

    # Venue + note
    venue = elems.get('venue', '')
    note = elems.get('note', '')
    if note:
        s += f'    <div class="card--project__venue">{venue} <span class="card--project__note">({note})</span></div>\n'
    else:
        s += f'    <div class="card--project__venue">{venue}</div>\n'

    # Links
    s += f'    <div class="card--project__links">\n'
    for key in elems['_ordered_keys']:
        if key in SKIP_LINK_KEYS:
            continue
        link = elems[key]
        if key == 'bibtex':
            bib_id = paper_id + 'Bib'
            s += f'      <a class="card--project__link" href="javascript:toggleblock(\'{bib_id}\')">{key}</a>\n'
        else:
            s += f'      <a class="card--project__link" href="{link}" target="_blank" rel="noopener">{key}</a>\n'
    s += f'    </div>\n'

    # BibTeX content
    if 'bibtex' in elems:
        bib_id = paper_id + 'Bib'
        bib_path = os.path.join(PUB_DIR, elems['bibtex'])
        try:
            bib_content = html_module.escape(read_file(bib_path).strip())
        except FileNotFoundError:
            bib_content = '(bibtex file not found)'
        s += f'    <pre class="bibtex-content" id="{bib_id}">{bib_content}</pre>\n'

    # Topic tags
    if topics_list:
        s += f'    <div class="card--project__topics">\n'
        for t in topics_list:
            label = TOPIC_LABELS.get(t, t)
            s += f'      <span class="card--project__topic">{label}</span>\n'
        s += f'    </div>\n'

    s += f'  </div>\n'
    s += f'</div>\n'
    return s


def build_projects_html():
    """Build the full projects list HTML with year dividers."""
    html = ''
    current_year = ''
    for entry in PUBLICATIONS:
        if entry[0] == 'year':
            current_year = str(entry[1])
            html += f'<div class="year-divider" data-year="{current_year}">\n'
            html += f'  <span class="year-divider__label">{current_year}</span>\n'
            html += f'</div>\n'
        else:
            paper_id, is_new, is_selected = entry
            elems = parse_paper(paper_id)
            html += build_project_card(paper_id, elems, is_new, current_year)
    return html


def build_featured_json():
    """Build JSON array of selected publications for the featured section."""
    selected = []
    for entry in PUBLICATIONS:
        if entry[0] == 'year':
            continue
        paper_id, is_new, is_selected = entry
        if not is_selected:
            continue
        elems = parse_paper(paper_id)
        img = rewrite_img_path(elems.get('img', ''))
        selected.append({
            'id': paper_id,
            'title': elems.get('title', ''),
            'img': img,
            'venue': elems.get('venue', ''),
            'project_page': elems.get('project page', ''),
            'pdf': elems.get('pdf', ''),
        })
    return json.dumps(selected, indent=2)


def build_person_card(person):
    """Build HTML for a person card."""
    s = '<div class="card--person">\n'
    photo = person.get('photo', 'assets/people/placeholder.jpg')
    url = person.get('url', '#')
    name = person.get('name', '')
    s += f'  <a href="{url}" target="_blank" rel="noopener">'
    s += f'<img class="card--person__photo" src="{photo}" alt="{html_module.escape(name, quote=True)}" loading="lazy"></a>\n'
    s += f'  <div class="card--person__name"><a href="{url}" target="_blank" rel="noopener">{name}</a></div>\n'
    meta_parts = []
    if 'program' in person:
        meta_parts.append(person['program'])
    if 'note' in person:
        meta_parts.append(person['note'])
    if meta_parts:
        s += f'  <div class="card--person__meta">{" · ".join(meta_parts)}</div>\n'
    s += '</div>\n'
    return s


def build_pi_html(pi):
    """Build the PI section HTML."""
    s = '<div class="pi-section">\n'
    s += f'  <img class="pi-section__photo" src="{pi["photo"]}" alt="{html_module.escape(pi["name"], quote=True)}">\n'
    s += '  <div class="pi-section__info">\n'
    s += f'    <h1 class="pi-section__name">{pi["name"]}</h1>\n'
    s += f'    <p class="pi-section__bio">{pi["bio"]}</p>\n'
    s += f'    <p class="pi-section__bio">{pi["bio_extra"]}</p>\n'
    s += f'    <p class="pi-section__bio">Email: {pi["email"]} · Office: {pi["office"]}</p>\n'
    s += '    <div class="pi-section__links">\n'
    for label, url in pi.get('links', {}).items():
        s += f'      <a class="pi-section__link" href="{url}" target="_blank" rel="noopener">{label}</a>\n'
    s += '    </div>\n'
    s += '  </div>\n'
    s += '</div>\n'
    return s


def build_alumni_html(alumni):
    """Build alumni sections."""
    s = ''

    # PhD alumni
    if alumni.get('phd'):
        s += '<div class="alumni-section">\n'
        s += '  <h3 class="alumni-section__title">PhD Alumni</h3>\n'
        s += '  <ul class="alumni-list">\n'
        for a in alumni['phd']:
            note = f' ({a["note"]})' if a.get('note') else ''
            s += f'    <li class="alumni-list__item">'
            s += f'<a href="{a["url"]}" target="_blank" rel="noopener">{a["name"]}</a>{note}, '
            s += f'<span class="alumni-list__thesis">{a.get("thesis", "")}</span>, '
            s += f'{a.get("year", "")}. {a.get("destination", "")}'
            s += '</li>\n'
        s += '  </ul>\n'
        s += '</div>\n'

    # MSR alumni
    if alumni.get('msr'):
        s += '<div class="alumni-section">\n'
        s += '  <h3 class="alumni-section__title">MSR Alumni</h3>\n'
        s += '  <ul class="alumni-list">\n'
        for a in alumni['msr']:
            dest = f'. {a["destination"]}' if a.get('destination') else ''
            s += f'    <li class="alumni-list__item">'
            s += f'<a href="{a["url"]}" target="_blank" rel="noopener">{a["name"]}</a>{dest}'
            s += '</li>\n'
        s += '  </ul>\n'
        s += '</div>\n'

    # MSCV alumni
    if alumni.get('mscv'):
        s += '<div class="alumni-section">\n'
        s += '  <h3 class="alumni-section__title">MSCV Alumni</h3>\n'
        s += '  <ul class="alumni-list alumni-list--compact">\n'
        for a in alumni['mscv']:
            s += f'    <li class="alumni-list__item">'
            s += f'<a href="{a["url"]}" target="_blank" rel="noopener">{a["name"]}</a>'
            s += '</li>\n'
        s += '  </ul>\n'
        s += '</div>\n'

    # Undergrad alumni
    if alumni.get('undergrad'):
        s += '<div class="alumni-section">\n'
        s += '  <h3 class="alumni-section__title">Undergraduate Alumni</h3>\n'
        s += '  <ul class="alumni-list alumni-list--compact">\n'
        for a in alumni['undergrad']:
            s += f'    <li class="alumni-list__item">'
            s += f'<a href="{a["url"]}" target="_blank" rel="noopener">{a["name"]}</a>'
            s += '</li>\n'
        s += '  </ul>\n'
        s += '</div>\n'

    return s


def render_page(page_title, content, nav_active, extra_scripts=''):
    """Render a page by filling in the base template."""
    base = read_file(os.path.join(TEMPLATE_DIR, 'base.html'))
    nav_map = {
        'overview': ('nav__link--active', '', ''),
        'projects': ('', 'nav__link--active', ''),
        'people': ('', '', 'nav__link--active'),
    }
    active = nav_map.get(nav_active, ('', '', ''))
    result = base.replace('{{PAGE_TITLE}}', page_title)
    result = result.replace('{{NAV_OVERVIEW_ACTIVE}}', active[0])
    result = result.replace('{{NAV_PROJECTS_ACTIVE}}', active[1])
    result = result.replace('{{NAV_PEOPLE_ACTIVE}}', active[2])
    result = result.replace('{{CONTENT}}', content)
    result = result.replace('{{EXTRA_SCRIPTS}}', extra_scripts)
    return result


def build_index():
    """Build the index.html page."""
    template = read_file(os.path.join(TEMPLATE_DIR, 'index_template.html'))
    featured_json = build_featured_json()
    content = template.replace('{{FEATURED_JSON}}', featured_json)
    scripts = '<script src="js/featured.js"></script>'
    page = render_page('Overview', content, 'overview', scripts)
    out_path = os.path.join(ROOT, 'index.html')
    with open(out_path, 'w') as f:
        f.write(page)
    print(f'  Generated {out_path}')


def build_projects():
    """Build the projects.html page."""
    template = read_file(os.path.join(TEMPLATE_DIR, 'projects_template.html'))
    projects_html = build_projects_html()
    content = template.replace('{{PROJECTS_HTML}}', projects_html)
    scripts = '<script src="js/projects.js"></script>'
    page = render_page('Projects', content, 'projects', scripts)
    out_path = os.path.join(ROOT, 'projects.html')
    with open(out_path, 'w') as f:
        f.write(page)
    print(f'  Generated {out_path}')


def build_people():
    """Build the people.html page."""
    people_path = os.path.join(DATA_DIR, 'people.json')
    with open(people_path, 'r') as f:
        people = json.load(f)

    template = read_file(os.path.join(TEMPLATE_DIR, 'people_template.html'))

    faculty_card = build_person_card({
        'name': people['pi']['name'],
        'url': 'https://shubhtuls.github.io',
        'photo': people['pi']['photo'],
    })
    phd_html = ''.join(build_person_card(p) for p in people['phd_students'])
    ms_html = ''.join(build_person_card(p) for p in people['ms_students'])
    prospective_html = people.get('prospective_text', '')
    alumni_html = build_alumni_html(people.get('alumni', {}))

    content = template
    content = content.replace('{{FACULTY_HTML}}', faculty_card)
    content = content.replace('{{PHD_STUDENTS_HTML}}', phd_html)
    content = content.replace('{{MS_STUDENTS_HTML}}', ms_html)
    content = content.replace('{{PROSPECTIVE_HTML}}', prospective_html)
    content = content.replace('{{ALUMNI_HTML}}', alumni_html)

    scripts = '<script src="js/projects.js"></script>'
    page = render_page('Members', content, 'people', scripts)
    out_path = os.path.join(ROOT, 'people.html')
    with open(out_path, 'w') as f:
        f.write(page)
    print(f'  Generated {out_path}')


def main():
    print('Building Physical Perception Lab website...')
    build_index()
    build_projects()
    build_people()
    print('Done!')


if __name__ == '__main__':
    main()
