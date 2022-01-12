import requests
import os
from flask import Flask, request

SERVER_IP = '10.10.10.10'   # Edit this line
PORT = 9000

basepath = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

@app.route('/ustvgo.m3u')
def playlist_generator():
    playlist = '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/Theitfixer85/myepg/master/blueepg.xml.gz"'
    info_file = f'{basepath}/ustvgo_channel_info.txt'
    with open(info_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line = line.split('|')
            name = line[0].strip()
            code = line[1].strip()
            logo = line[2].strip()
            playlist += f'\n#EXTINF:-1 tvg-id="{code}" group-title="ustvgo" tvg-logo="{logo}", {name}'
            playlist += f'\nhttp://{SERVER_IP}:{PORT}/channels?id={code}'
    return playlist

@app.route('/channels')
def getChannel():
    code = request.args.get('id')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Referer': 'https://ustvgo.tv/'
    }
    pl = requests.get(f'https://ustvgo.tv/player.php?stream={code}', headers=headers).text
    pl = pl.replace('\n', '').split("var hls_src='")[1].split("'")[0]
    base = pl.split('playlist.m3u8')[0]
    head = '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=818009,RESOLUTION=640x360,CODECS="avc1.64001f,mp4a.40.2"\n'
    m3u = requests.get(pl).text.strip().split('\n')[-1]
    return head + base + m3u

if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
