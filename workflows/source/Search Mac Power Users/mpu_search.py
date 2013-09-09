#!/usr/bin/python
# -*- coding: utf-8 -*-

# requires: beautifulsoup4, requests, lxml, re, shelve, sys

## CONFIG
DAYS_OF_CACHE = 5
## END CONFIG

__title__ = "Search Mac Power Users show notes"
__author__ = "Fernando Xavier de Freitas Crespo"
__author_email__ = "fernando@crespo.in"
__version__ = "1.3"

from bs4 import BeautifulSoup
import sys
import requests
import re
import shelve
import os
import datetime

def must_update_cache():
    return datetime.datetime.fromtimestamp(os.path.getmtime('episodes_cache.db')) < datetime.datetime.now() - datetime.timedelta(days=DAYS_OF_CACHE)

query = "{query}"
item_template='  <item arg="{0}" valid="{3}" autocomplete="{0}"><title><![CDATA[{1}]]></title><subtitle><![CDATA[{2}]]></subtitle><icon>icon.png</icon></item>'

def get_episodes_in_page(page):
    episodes = []
    url = 'http://5by5.tv/mpu/page/{0}'
    response = requests.get(url.format(page))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        for div in soup.findAll('div'):
            if div.get('class') and div.get('class')[0] == 'episode':
                title = div.h3.a.text.encode('ascii', 'ignore').strip()
                episode_number = re.search(r'.*#([0-9]{,3}).*', title).group(1)
                subtitle = div.p.text.encode('ascii', 'ignore').strip()
                episodes.append([episode_number, title, subtitle])
    return episodes

def add_episode_to_cache(cache, episode):
    episode_number = episode[0].zfill(4)
    if episode_number not in cache:
        cache[episode_number] = episode
        return True
    return False

def cache_all(cache):
    for i in range(1, 20): # Pick last 20 pages to cache all episodes
        episodes_in_page_i = get_episodes_in_page(i)
        for episode in episodes_in_page_i:
            #print "Caching episode {0}".format(episode[0])
            print(item_template.format(episode[0], episode[1], episode[2], 'yes'))
            add_episode_to_cache(cache, episode)

def list_all():
    for i in range(1, 20): # Pick last 20 pages to cache all episodes
        episodes_in_page_i = get_episodes_in_page(i)
        for episode in episodes_in_page_i:
            print(item_template.format(episode[0], episode[1], episode[2], 'yes'))

def main(argv):
    global query

    if len(argv) >= 1:
        query = argv[0]

    cached_items = shelve.open('episodes_cache')

    if not cached_items:
        cache_all(cached_items)
        cached_items.close()
        cached_items = shelve.open('episodes_cache')

    sorted_cached_items = sorted(cached_items, reverse=True)

    print('<?xml version="1.0" encoding="UTF-8"?>\n<items>')

    if cached_items:
        # Force get lastest 10 episodes (firs page) to keep up to date
        #print('Getting latest 10 episodes')
        if must_update_cache():
            episodes_in_page_1 = get_episodes_in_page(1)
            for episode in episodes_in_page_1:
                #print('Found episode {0}, caching it'.format(episode))
                add_episode_to_cache(cached_items, episode)

        for item in sorted_cached_items:
            search_in = str(cached_items[item][0]).lower() + " " + \
            str(cached_items[item][1]).lower() + " " + \
            str(cached_items[item][2]).lower()
            if query.lower() in search_in:
                print(item_template.format(cached_items[item][0], cached_items[item][1], cached_items[item][2], 'yes'))
    else:
        print(item_template.format(0, "Error", "Could not read cache file", 'no'))

    print('</items>')

    cached_items.close()

if __name__ == '__main__':
    main(sys.argv[1:])