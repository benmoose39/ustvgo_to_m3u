import requests
import os
from flask import Flask, request

SERVER_IP = '10.10.10.10'   # Edit this line
PORT = 9000

headers = {'Referer':'https://ustvgo.tv/'}

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
    head = '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=818009,RESOLUTION=640x360,CODECS="avc1.64001f,mp4a.40.2"\n'
    sample = requests.get(f'https://ustvgo.tv/player.php?stream={code}', headers=headers).text
    try:
        pl = sample.split("hls_src='")[1].split("'")[0]
        res = requests.get(pl)
        base = pl.split('playlist.m3u8')[0]
        m3u = res.text.strip().split('\n')[-1]
    except Exception as e:
        m3u = 'https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u'
        return head + m3u
    return head + base + m3u

if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
