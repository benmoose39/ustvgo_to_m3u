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

def getSample():
    vpn = False
    headers = {'Referer':'https://ustvgo.tv/'}
    src = s.get('https://ustvgo.tv/player.php?stream=CNN', headers=headers).text
    global novpn_sample
    novpn_sample = src.split("hls_src='")[1].split("'")[0]
    src = s.get('https://ustvgo.tv/player.php?stream=BET', headers=headers).text
    global vpn_sample
    if '.m3u8' in src:
        vpn_sample = src.split("hls_src='")[1].split("'")[0]
    else:
        vpn_sample = 'https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u'

def grab(line):
    if not vpn_sample:
        getSample()
    name = line[0].strip()
    code = line[1].strip()
    logo = line[2].strip()
    if line[-1].strip() == 'VPN':
        m3u = vpn_sample.replace('BET', code)
    else:
        m3u = novpn_sample.replace('CNN', code)
    playlist.write(f'\n#EXTINF:-1 tvg-id="{code}" group-title="ustvgo" tvg-logo="{logo}", {name}')
    playlist.write(f'\n{m3u}')

s = requests.Session()

info_file = 'https://raw.githubusercontent.com/benmoose39/ustvgo_to_m3u/main/ustvgo_channel_info.txt'
file = s.get(info_file).text.split('\r\n')
total = len(list(filter(lambda x:x, file)))

with open('../ustvgo.m3u', 'w') as playlist:
    print('[*] Generating your playlist, please wait...\n')
    playlist.write('#EXTM3U x-tvg-url="https://www.kcpcdr.com/ustvgo.xml.gz"')
    playlist.write(f'\n{banner}\n')
    pbar = tqdm(total=total)
    vpn_sample = ''
    novpn_sample = ''
    for line in file:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        line = line.split('|')
        pbar.update(1)
        grab(line)
    pbar.close()
    print('\n[SUCCESS] Playlist is generated!\n')
    done()
        
