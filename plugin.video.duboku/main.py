# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html


import re
from xbmcswift2 import Plugin
import requests
from bs4 import BeautifulSoup
import xbmcgui
import base64
import json
import urllib2
import sys
import HTMLParser
import re


def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    # 转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()


headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4'}
websiteurl = 'https://www.duboku.tv'


def get_categories():
    return [{'name': '电影', 'link': 'https://www.duboku.tv/vodtype/1'},
            {'name': '电视剧', 'link': 'https://www.duboku.tv/vodtype/2'},
            {'name': '综艺', 'link': 'https://www.duboku.tv/vodtype/3'},
            {'name': '动漫', 'link': 'https://www.duboku.tv/vodtype/4'}]


def get_videos(category, page):
    # if int(page) == 1:
    #     pageurl = category
    # else:
    #     pageurl = category + 'index_'+page+'.html'
    pageurl = category + '-' + page + '.html'
    r = requests.get(pageurl, headers=headers)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text, "html5lib")
    videos = []
    #videoelements = soup.find('ul', id='list1').find_all('li')
    #videoelements = contenter.find_all("a", attrs={"data-original": True})
    videoelements = soup.find('ul', class_='myui-vodlist').find_all('a', class_='myui-vodlist__thumb')

    if videoelements is None:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '没有播放源')
    else:
        for videoelement in videoelements:
            #movieitem = videoelement.find('a', class_='ui-pic')
            thumbsrc = videoelement['data-original']
            if thumbsrc[0:4] != 'http':
                thumbsrc = websiteurl + thumbsrc
            videoitem = {}
            videoitem['name'] = videoelement['title']
            videoitem['href'] = websiteurl + videoelement['href']
            videoitem['thumb'] = thumbsrc
            videoitem['genre'] = '喜剧片'
            videos.append(videoitem)
        return videos


def get_search(keyword, page):
    # if int(page) == 1:
    #     pageurl = category
    # else:
    #     pageurl = category + 'index_'+page+'.html'
    serachUrl = websiteurl + '/vodsearch/' + keyword + '----------' + str(page) + '---.html'

    r = requests.get(serachUrl, headers=headers)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text, "html5lib")
    videos = []
    videoelements = soup.find_all('a', class_='myui-vodlist__thumb')
    #videoelements = contenter.find_all("a", attrs={"data-original": True})
    #videoelements = soup.find('ul', id='list1').find_all('a', {'data-origin', True})
    #videoelements = soup.find_all('a', class_='myui-vodlist__thumb')

    if videoelements is None:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '没有播放源')
    else:
        for videoelement in videoelements:
            #movieitem = videoelement
            #videoinfo = movieitem.find('h3').find('a')
            #pattern = re.compile("\(([^\)]*)\)")
            #thumbsrc = str(pattern.findall(movieitem.find('a', class_='videopic')['style'])[0])
            #imglink = videoelement.find('img')
            #movieitem = videoelement.find('a')
            thumbsrc = videoelement['data-original']
            if thumbsrc[0:4] != 'http':
                thumbsrc = websiteurl + thumbsrc
            videoitem = {}
            videoitem['name'] = videoelement['title']
            videoitem['href'] = websiteurl + videoelement['href']
            videoitem['thumb'] = thumbsrc
            videoitem['genre'] = '喜剧片'
            videos.append(videoitem)
        return videos


def get_sources(videolink):
    r = requests.get(videolink, headers=headers)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text)
    sources = []
    #categoryname = soup.find('ul', class_='menulist').find('li', class_='active').find('a').get_text()

    alllink = soup.find('ul', class_='myui-content__list').find_all('a')
    thumba = soup.find('img', class_='lazyload')['data-original']
    # stylestr = thumba['style']
    # thumburl = stylestr.split("(", 1)[1].split(")")[0]
    # thumbsrc = thumburl
    thumbsrc = thumba
    if thumbsrc[0:4] != 'http':
        thumbsrc = websiteurl + thumbsrc

    if alllink is not None:
        for sourceitem in alllink:
            videosource = {}
            videosource['name'] = sourceitem.get_text()
            videosource['thumb'] = thumbsrc
            videosource['category'] = '电影'
            videosource['href'] = websiteurl + sourceitem['href']
            sources.append(videosource)
        return sources
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '没有播放源')


@plugin.route('/play/<url>/')
def play(url):
    s = requests.session()
    r = s.get(url, headers=headers)
    r.encoding = 'UTF-8'
    #soup = BeautifulSoup(r.text)
    #iframesrc = soup.find('iframe')['src']

    pattern = re.compile(",\"url\":\"([^\"]*)\"")
    
    #xbmc.log('Test pattern = %s'%pattern, level=xbmc.LOGDEBUG)
    #playurl = unescape(str(pattern.findall(r.text)[0]))
    #playurl = str(pattern.findall(r.text)).replace('\\', '')
    playurl = str(pattern.findall(r.text)[1]).replace('\\', '')
    #playurl = str(pattern.match("(m3u8)$",r.text)).replace('\\', '')
    #xbmc.log('Test playurl = %s'%playurl, level=xbmc.LOGDEBUG)


    # ishttp = unescape(playurl)
    # videourl = ''

    # if ishttp[0:7] == 'http://' or ishttp[0:8] == 'https://':
    #     videourl = ishttp
    # else:
    #     mheaders = {}
    #     mheaders['referer'] = websiteurl+'js/player/mp4.html?2020221'
    #     mheaders['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    #     ucookies = {}
    #     ucookies['__cfduid'] = s.cookies.get_dict()['__cfduid']
    #     videourl = 'https://www.nfmovies.com/api/vproxy.php?url=' + playurl + '&type=json'
    #     # print(s.cookies.get_dict())  # 先打印一下，此时一般应该是空的。
    #     rv = s.get(videourl, verify=False, headers=mheaders, cookies=ucookies)
    #     result = json.loads(rv.text)
    #     videourl = result['data']

    item = {'label': '播放', 'path': playurl, 'is_playable': True}
    items = []
    items.append(item)
    return items

    # if playurl is not None:
    #     plugin.set_resolved_url(item)
    # else:
    #     dialog = xbmcgui.Dialog()
    #     ok = dialog.ok('错误提示', '没有播放源')


@plugin.route('/sources/<url>/')
def sources(url):
    sources = get_sources(url)
    items = [{
        'label': source['name'],
        'path': plugin.url_for('play', url=source['href']),
        'thumbnail': source['thumb'],
        'icon': source['thumb'],
    } for source in sources]
    sorted_items = sorted(items, key=lambda item: item['label'])
    return sorted_items


@plugin.route('/category/<url>/<page>/')
def category(url, page):
    videos = get_videos(url, page)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('sources', url=video['href']),
        'thumbnail': video['thumb'],
        'icon': video['thumb']
    } for video in videos]

    sorted_items = items
    #sorted_items = sorted(items, key=lambda item: item['label'])
    pageno = int(page) + 1
    nextpage = {'label': ' 下一页', 'path': plugin.url_for('category', url=url, page=pageno)}
    sorted_items.append(nextpage)
    return sorted_items

# get search result by input keyword


@plugin.route('/search')
def search():
    keyboard = xbmc.Keyboard('', '请输入搜索内容')
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        #url = HOST_URL + '/index.php?m=vod-search&wd=' + keyword
        # https://www.nfmovies.com/search.php?page=1&searchword='+keyword+'&searchtype=

        videos = get_search(keyword, 1)
        items = [{
            'label': video['name'],
            'path': plugin.url_for('sources', url=video['href']),
            'thumbnail': video['thumb'],
            'icon': video['thumb']
        } for video in videos]

        sorted_items = items
        # sorted_items = sorted(items, key=lambda item: item['label'])
        nextpage = {'label': ' 下一页', 'path': plugin.url_for('searchMore', keyword=keyword, page=2)}
        sorted_items.append(nextpage)
        return sorted_items


@plugin.route('/searchMore/<keyword>/<page>/')
def searchMore(keyword, page):
    videos = get_search(keyword, page)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('sources', url=video['href']),
        'thumbnail': video['thumb'],
        'icon': video['thumb']
    } for video in videos]

    sorted_items = items
    # sorted_items = sorted(items, key=lambda item: item['label'])
    pageno = int(page) + 1
    nextpage = {'label': ' 下一页', 'path': plugin.url_for('searchMore', keyword=keyword, page=pageno)}
    sorted_items.append(nextpage)
    return sorted_items


@plugin.route('/')
def index():
    categories = get_categories()
    items = [{
        'label': category['name'],
        'path': plugin.url_for('category', url=category['link'], page=1),
    } for category in categories]

    items.append({
        'label': u'[COLOR yellow]搜索[/COLOR]',
        'path': plugin.url_for('search'),
    })
    #sorted_items = sorted(items, key=lambda item: item['label'])
    return items


if __name__ == '__main__':
    plugin.run()
    plugin.set_view_mode(500)
