import requests
import os
from flask import Flask, request

SERVER_IP = '10.10.10.10'   # Edit this line
PORT = 9000

headers = {'Referer':'https://ustvgo.tv/'}

basepath = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

novpn_sample = ''
vpn_sample = ''

def getSample():
    vpn = False
    headers = {'Referer':'https://ustvgo.tv/'}
    src = requests.get('https://ustvgo.tv/player.php?stream=CNN', headers=headers).text
    global novpn_sample
    novpn_sample = src.split("hls_src='")[1].split("'")[0]
    src = requests.get('https://ustvgo.tv/player.php?stream=BET', headers=headers).text
    global vpn_sample
    if '.m3u8' in src:
        vpn_sample = src.split("hls_src='")[1].split("'")[0]
    else:
        vpn_sample = 'https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u'

getSample()

@app.route('/ustvgo.m3u')
def playlist_generator():
    playlist = '#EXTM3U x-tvg-url="https://www.kcpcdr.com/ustvgo.xml.gz"'
    #info_file = f'{basepath}/ustvgo_channel_info.txt'
    info_file = 'https://raw.githubusercontent.com/benmoose39/ustvgo_to_m3u/main/ustvgo_channel_info.txt'
    file = requests.get(info_file).text.split('\r\n')

    for line in file:
        line = line.strip()
        if not line:
            continue
        line = line.split('|')
        name = line[0].strip()
        code = line[1].strip()
        logo = line[2].strip()
        requirevpn = line[-1].strip()
        isvpn = 'false'
        if requirevpn == 'VPN':
            isvpn = 'true'
        playlist += f'\n#EXTINF:-1 tvg-id="{code}" group-title="ustvgo" tvg-logo="{logo}", {name}'
        playlist += f'\nhttp://{SERVER_IP}:{PORT}/channels?id={code}&isvpn={isvpn}'
    return playlist

@app.route('/channels')
def getChannel():
    code = request.args.get('id')
    isvpn = request.args.get('isvpn')
    head = '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=818009,RESOLUTION=640x360,CODECS="avc1.64001f,mp4a.40.2"\n'
    try:
        if isvpn == 'true':
            sample = vpn_sample.replace('BET',code)
            res = requests.get(sample)
            base = sample.split('playlist.m3u8')[0]
        elif isvpn == 'false':
            sample = novpn_sample.replace('CNN',code)
            res = requests.get(sample)
            base = sample.split('playlist.m3u8')[0]
        m3u = res.text.strip().split('\n')[-1]
    except Exception as e:
        m3u = 'https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u'
        return head + m3u
    return head + base + m3u


if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
