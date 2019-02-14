# -*- coding=utf-8 -*-
# author:Ben_tiax
# QQ:495463070

import subprocess
import json
import time
import os

try:
    import requests
except ImportError:
    print('install requests ...')
    subprocess.check_output("pip install requests",shell=True)
    import requests
    print('install completed')
    

try:
    from tqdm import tqdm
except ImportError:
    print('install tqdm ...')
    subprocess.check_output("pip install tqdm",shell=True)
    from tqdm import tqdm
    print('install completed')

try:
    import mutagen
except ImportError:
    print('install mutagen ...')
    subprocess.check_output("pip install mutagen",shell=True)
    import mutagen
    print('install completed')
   
try:
    import mutagen
except ImportError:
    print('install mutagen ...')
    subprocess.check_output("pip install mutagen",shell=True)
    import mutagen 
    print('install completed')





def read_local_path(input_path):
    list_input_path = [x for x in os.walk(input_path)]
    message_list = []
    song_title_list = []
    for i in list_input_path:
        current_path, dir_in_path, file_list = i
        for file in file_list:
            song_path = current_path + '\\' + file

            splits = file.split('.')
            song_title = ''.join(splits[:-1])
            song_type = splits[-1]

            song_type_list = ['flac', 'mp3', 'm4a', 'wav', 'dff', 'dsf']
            if song_type not in song_type_list:
                continue
            else:
                message = get_message(song_path, song_title, song_type)
                message_list.append(message)
                song_title_list.append(song_title)
    return message_list, song_title_list


def get_message(song_path, song_title, song_type):
    message, title, artist, album = '', '', '', ''
    opensong = mutagen.File(song_path)
    if not opensong:
        return song_title
    keys = opensong.keys()

    if song_type == 'flac':
        title = opensong['title'][0] if 'title' in keys else ''
        artist = opensong['artist'][0] if 'artist' in keys else ''
        album = opensong['album'][0] if 'album' in keys else ''
    elif song_type == 'mp3':
        title = str(opensong['TIT2']) if 'TIT2' in keys else ''
        artist = str(opensong['TPE1']) if 'TPE1' in keys else ''
        album = str(opensong['TALB']) if 'TALB' in keys else ''
    elif song_type == 'm4a':
        title = opensong['©nam'][0] if '©nam' in keys else ''
        artist = opensong['©ART'][0] if '©ART' in keys else ''
        album = opensong['©alb'][0] if '©alb' in keys else ''
    else:
        title = song_title

    if title and (artist or album):
        message = title + ' ' + artist + ' ' + album
    elif not title:
        message = song_title
    return message


def get_song_id(message):
    global search_song_url, header_search
    song_id = []
    raw_data = 's={}&limit=10&type=1&offset=0'.format(message).encode('utf-8')
    response_json = requests.post(search_song_url, data=raw_data, headers=header_search)
    try:
        data_json = json.loads(response_json.text)
    except:
        return 

    if 'songs' in data_json['result'].keys():
        for i in data_json['result']['songs']:
            if (i['name'].lower() in message.lower()):
                song_id = i['id']
                break
        return song_id
    else:
        get_song_id(message.split(' ')[0])


def get_lrc(song_id):
    global header_search
    if not song_id:
        return
    song_lrc_url = 'http://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1'.format(song_id)
    r = requests.get(song_lrc_url, headers=header_search)

    try:
        dicta = json.loads(r.text)
    except:
        return 

    if 'lrc' in dicta.keys():
        lyrics = dicta['lrc']['lyric'].split('\n')
        if 'lyric' in dicta['tlyric'].keys():
            if not dicta['tlyric']['lyric']:
                return lyrics 
            translation = dicta['tlyric']['lyric'].split('\n')
            list_lrc = cn_jp_merge(lyrics, translation)
        else:
            list_lrc = lyrics
        return list_lrc


def cn_jp_merge(lyrics,translation):
    list_lrc = []
    for j in lyrics:
        for k in translation:
            if j.split(']')[0] == k.split(']')[0]:
                list_lrc.append(j+'_'+''.join(k.split(']')[1:]))
                continue
    return list_lrc

header_search = {
    'Cookie': '_ntes_nnid=9c84ad50f02e90d1f136bf987059c316,1527561382785; _ntes_nuid=9c84ad50f02e90d1f136bf987059c316; P_INFO=q495463070@163.com|1527751416|0|other|00&99|jis&1527415600&other#jis&320100#10#0#0|&0|mail163|q495463070@163.com; mail_psc_fingerprint=7a8bff06c33866179897fa5cfed2778b; _iuqxldmzr_=32; __gads=ID=557781b4bdcac750:T=1531289909:S=ALNI_MZaI9VGHq9nQ33R6ywIs6syFZdO_Q; vjuids=1257bf6e28.16487fdaf7f.0.04b0bc26b2148; vjlast=1531289907.1534728026.23; WM_TID=YJRtPzqsxDXrn5QQ3GtI9oX4OJMGPt3A; usertrack=ezq0pFuGRdWKV6XuA7PrAg==; _ga=GA1.2.706084343.1535526356; vinfo_n_f_l_n3=4bdf4b7dcafc8897.1.3.1531289907149.1535683663294.1535685817807; __utma=94650624.680157290.1527561383.1547114270.1547170350.22; __utmz=94650624.1547170350.22.8.utmcsr=moehuan.club|utmccn=(referral)|utmcmd=referral|utmcct=/; WM_NI=L1g8b3LmMVAqQn3%2BqJAn%2BN2kTHcR4Dc9L%2Btm3QxRB%2B5kmM%2FMNXToYK2FzcDZcOQvtT3no%2FxAJ6DqmAeKIi9E8qUTIPyFIVNZFNp%2BujEtN59J9BOFAY6eBpNr%2FJZL9ZRraTQ%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed8aa678999acbbf249b8ef8fa2c15e978e9b85f774a8baa990c63bbc9b96bbdb2af0fea7c3b92a90efa9d9e13990b383b7c47b93b2fdccf44283b2e5afb1619898adb3b750a1e784ccf767f18fb8b3c121f7b5a3aeae478e889c90dc41f29ab684c752a1919f97f760f1b2a1d0fb4b8aea8c92f04ba795878abc4ffcaf9bb5cc5cbb9a87b7cd528692c0ccf86287ac82d6bc42fb9e81a7c453f6bb8e91cd7aed9696adbc5292aeafb5d437e2a3; playerid=28408762; __remember_me=true; MUSIC_U=eb667f83f0557efb26088e05ada5725987f95d7859a2feb91339200023e58c9b4bb29680971e5ca76745344ffb87d5a7af9e62a8590fd08a; __csrf=64cc4dc7844e3f6767d884b3af253299; JSESSIONID-WYYY=Fp6c6yzJ0y4S6TRPchoj8HvRmvMnqAPI7KV0C9cMT%2BbVbyWhCHsl8UC0ctAcdkJ0UK%2BPkqzJxZYNFFwrJ770G73Jb1IKDvdDTjKujfypU6ImfG3bJXMiXeVwU0zc87odWq%5C3qI7PBKQ0sl33J%5CsZRKnnnwuIzB3OxEsrIiv990qnxCaI%3A1548841497007',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'Referer': 'http://music.163.com/'}
search_song_url = 'http://music.163.com/api/search/get/'

path = os.getcwd()

message_list, song_title_list = read_local_path(path)


for _,k in enumerate(tqdm(song_title_list)):
    mid_list_lrc = get_lrc(get_song_id(message_list[_]))
    if mid_list_lrc:
        list_lrc = sorted(mid_list_lrc)

        if not os.path.exists('{}\\lrc'.format(path)):
            os.mkdir('{}\\lrc'.format(path))

        if list_lrc:
            file = '{}\\lrc\\{}.lrc'.format(path, k)
            with open(file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(list_lrc))

input()
