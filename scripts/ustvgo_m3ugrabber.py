banner = r'''
                    #########################################################################
                    #      ____            _           _   __  __                           #
                    #     |  _ \ _ __ ___ (_) ___  ___| |_|  \/  | ___   ___  ___  ___      #
                    #     | |_) | '__/ _ \| |/ _ \/ __| __| |\/| |/ _ \ / _ \/ __|/ _ \     #
                    #     |  __/| | | (_) | |  __/ (__| |_| |  | | (_) | (_) \__ \  __/     #
                    #     |_|   |_|  \___// |\___|\___|\__|_|  |_|\___/ \___/|___/\___|     #
                    #                   |__/                                                #
                    #                                  >> https://github.com/benmoose39     #
                    #########################################################################
'''
print(banner)

import os
import sys


windows = False
python = 'python3'
if 'win' in sys.platform:
    windows = True
    python = 'python'

def done():
    sys.exit()
    
print('[*] Checking dependencies...')
while True:
    try:
        import requests
        from tqdm import tqdm
        break
    except ModuleNotFoundError as e:
        module = str(e)[17:-1]
        print(f'[*] Installing {module} module for python')
        #os.system(f'{python} -m pip install --upgrade pip')
        try:
            if os.system(f'{python} -m pip install {module}') != 0:
                raise error
        except Exception:
            print(f'[!] Error installing "{module}" module. Do you have pip installed?')
            input(f'[!] Playlist generation failed. Press Ctrl+C to exit...')
            done()

def grab(name, code, logo):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
            'Referer': 'https://ustvgo.tv/'
        }
        m3u = s.get(f'https://ustvgo.tv/player.php?stream={code}', headers=headers).text
        m3u = m3u.replace('\n', '').split("var hls_src='")[1].split("'")[0]
        playlist.write(f'\n#EXTINF:-1 tvg-id="{code}" group-title="ustvgo" tvg-logo="{logo}", {name}')
        playlist.write(f'\n{m3u}')
    except:
        # findersfred helped me to find this, all credits to him:
        m3u = s.get(f'https://ustvgo.tv/player.php?stream=BBCAmerica', headers=headers).text
        m3u = m3u.replace('\n', '').split("var hls_src='")[1].split("'")[0].replace('BBCAmerica', code)
        playlist.write(f'\n#EXTINF:-1 tvg-id="{code}" group-title="ustvgo" tvg-logo="{logo}", {name}')
        playlist.write(f'\n{m3u}')
        

total = 0
with open('../ustvgo_channel_info.txt') as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        total += 1

s = requests.Session()
with open('../ustvgo_channel_info.txt') as file:
    with open('../ustvgo.m3u', 'w') as playlist:
        print('[*] Generating your playlist, please wait...\n')
        playlist.write('#EXTM3U x-tvg-url="https://raw.githubusercontent.com/Theitfixer85/myepg/master/blueepg.xml.gz"')
        playlist.write(f'\n{banner}\n')
        pbar = tqdm(total=total)
        for line in file:
            line = line.strip()
            if not line or line.startswith('~~'):
                continue
            line = line.split('|')
            name = line[0].strip()
            code = line[1].strip()
            logo = line[2].strip()
            pbar.update(1)
            grab(name, code, logo)
        pbar.close()
        print('\n[SUCCESS] Playlist is generated!\n')
        done()
        
