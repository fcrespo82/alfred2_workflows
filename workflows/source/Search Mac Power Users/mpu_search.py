#!/usr/bin/python
# -*- coding: utf-8 -*-

# require bs4, requests, lxml, re, shelve

from bs4 import BeautifulSoup
import requests
import re
import shelve
from pprint import pprint # just for development

query = "{query}"

item_template='  <item arg="{0}" valid="{3}" autocomplete="{0}"><title><![CDATA[{1}]]></title><subtitle><![CDATA[{2}]]></subtitle><icon>icon.png</icon></item>'

def getEpisodesInPage(page):
    episodes = []
    mpu = 'http://5by5.tv/mpu/page/{0}'
    response = requests.get(mpu.format(page))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        for div in soup.findAll('div'):
            if div.get('class') and div.get('class')[0] == 'episode':
                title = div.h3.a.text.encode('ascii', 'ignore').strip()
                episode_number = re.search('.*#([0-9]{,3}).*', title).group(1)
                subtitle = div.p.text.encode('ascii', 'ignore').strip()
                episodes.append([episode_number, title, subtitle])
    return episodes

def addEpisodeToCache(cache, episode):
    episode_number = episode[0].zfill(4)
    if not cache.has_key(episode_number):
        cache[episode_number] = episode
        return True
    return False

def cacheAll(cache):
    for i in range(1, 20): # Pick last 20 pages to cache all episodes
        episodesInPageI = getEpisodesInPage(i)
        for episode in episodesInPageI:
            #print "Caching episode {0}".format(episode[0])
            print item_template.format(episode[0], episode[1], episode[2], 'yes')
            addEpisodeToCache(cache, episode)

def listAll():
    for i in range(1, 20): # Pick last 20 pages to cache all episodes
        episodesInPageI = getEpisodesInPage(i)
        for episode in episodesInPageI:
            print item_template.format(episode[0], episode[1], episode[2], 'yes')

def main():
    # Fazer cache de tudo e depois sempre verificar a primeira página para adicionar itens atuais no cache

    cached_items = shelve.open('episodes_cache')

    if not cached_items:
        cacheAll(cached_items)
        cached_items.close()
        cached_items = shelve.open('episodes_cache')

    sorted_cached_items = sorted(cached_items, reverse=True)

    print('<?xml version="1.0" encoding="UTF-8"?>\n<items>')

    if cached_items:
        # Force get lastest 10 episodes to keep up to date
        episodesInPage0 = getEpisodesInPage(0)
        for episode in episodesInPage0:
            addEpisodeToCache(cached_items, episode)

        for item in sorted_cached_items:
            searchIn = str(cached_items[item][0]).lower() + " " + \
            str(cached_items[item][1]).lower() + " " + \
            str(cached_items[item][2]).lower()
            if query.lower() in searchIn:
                print item_template.format(cached_items[item][0], cached_items[item][1], cached_items[item][2], 'yes')
    else:
        #for item in getEpisodesInPage(9):
        #    print item_template.format(item[0], item[1], item[2], 'yes')
        #for item in getEpisodesInPage(11):
        #    print item_template.format(item[0], item[1], item[2], 'yes')
        print item_template.format(0, "Error", "Could not read cache file", 'no')

    print('</items>')

    cached_items.close()

main()