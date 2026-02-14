#!/usr/bin/env python3
"""One-time script to download member photos from their personal websites.

Usage: python build/scrape_photos.py  (from the ppl/ directory)

This script attempts to find and download profile photos from each member's
personal website. Photos are saved to assets/people/.
"""

import json
import os
import re
import urllib.request
import urllib.error
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEOPLE_JSON = os.path.join(ROOT, 'data', 'people.json')
PHOTO_DIR = os.path.join(ROOT, 'assets', 'people')


class OGImageParser(HTMLParser):
    """Parse og:image and other image meta tags from HTML."""
    def __init__(self):
        super().__init__()
        self.og_image = None
        self.profile_images = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        # Check for og:image
        if tag == 'meta':
            prop = attrs_dict.get('property', '')
            if prop == 'og:image' and 'content' in attrs_dict:
                self.og_image = attrs_dict['content']
        # Check for profile-like images
        if tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '').lower()
            cls = attrs_dict.get('class', '').lower()
            if any(kw in src.lower() for kw in ['profile', 'avatar', 'photo', 'headshot', 'portrait']):
                self.profile_images.append(src)
            elif any(kw in alt for kw in ['profile', 'photo', 'headshot', 'portrait']):
                self.profile_images.append(src)
            elif any(kw in cls for kw in ['profile', 'avatar', 'photo', 'headshot', 'portrait']):
                self.profile_images.append(src)


def download_image(url, save_path):
    """Download an image from url to save_path."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            with open(save_path, 'wb') as f:
                f.write(data)
            print(f'  Downloaded: {url} -> {save_path}')
            return True
    except Exception as e:
        print(f'  Failed to download {url}: {e}')
        return False


def find_and_download_photo(name, url, photo_filename):
    """Try to find and download a profile photo from a personal website."""
    save_path = os.path.join(PHOTO_DIR, photo_filename)
    if os.path.exists(save_path):
        print(f'  Skipping {name} - photo already exists')
        return True

    if not url or url == '#':
        print(f'  Skipping {name} - no URL')
        return False

    print(f'Processing {name}: {url}')

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f'  Failed to fetch {url}: {e}')
        return False

    parser = OGImageParser()
    try:
        parser.feed(html)
    except Exception:
        pass

    # Try og:image first
    if parser.og_image:
        img_url = parser.og_image
        if not img_url.startswith('http'):
            img_url = urllib.request.urljoin(url, img_url)
        if download_image(img_url, save_path):
            return True

    # Try profile-like images
    for src in parser.profile_images:
        if not src.startswith('http'):
            src = urllib.request.urljoin(url, src)
        if download_image(src, save_path):
            return True

    # Fallback: look for common image patterns in the HTML
    img_patterns = re.findall(r'(?:src|href)=["\']([^"\']*?(?:profile|avatar|photo|headshot|portrait|pic)[^"\']*?\.(?:jpg|jpeg|png|webp))["\']', html, re.IGNORECASE)
    for src in img_patterns[:3]:
        if not src.startswith('http'):
            src = urllib.request.urljoin(url, src)
        if download_image(src, save_path):
            return True

    print(f'  Could not find photo for {name}')
    return False


def main():
    os.makedirs(PHOTO_DIR, exist_ok=True)

    with open(PEOPLE_JSON) as f:
        people = json.load(f)

    members = []
    for p in people.get('phd_students', []):
        filename = os.path.basename(p.get('photo', ''))
        if filename:
            members.append((p['name'], p.get('url', ''), filename))
    for p in people.get('ms_students', []):
        filename = os.path.basename(p.get('photo', ''))
        if filename:
            members.append((p['name'], p.get('url', ''), filename))

    print(f'Attempting to download photos for {len(members)} members...\n')
    success = 0
    for name, url, filename in members:
        if find_and_download_photo(name, url, filename):
            success += 1
        print()

    print(f'\nDone: {success}/{len(members)} photos downloaded.')
    missing = [m[0] for m in members if not os.path.exists(os.path.join(PHOTO_DIR, m[2]))]
    if missing:
        print(f'Missing photos for: {", ".join(missing)}')
        print('You may need to manually download these photos.')


if __name__ == '__main__':
    main()
