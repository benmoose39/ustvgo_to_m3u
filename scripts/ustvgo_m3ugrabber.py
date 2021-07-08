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

import requests

def grab(name, code, logo):
    data = {'stream': code}
    m3u = requests.post('https://ustvgo.tv/data.php', data=data).text
    print(f'\n#EXTINF:-1 tvg-id="{code}" group-title="ustvgo" tvg-logo="{logo}", {name}')
    print(m3u)


print('#EXTM3U x-tvg-url="https://raw.githubusercontent.com/nomoney4me/ustvgo/main/output/ustvgo_epg.xml"')
print(banner)
with open('../ustvgo_channel_info.txt') as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        line = line.split('|')
        name = line[0].strip()
        code = line[1].strip()
        logo = line[2].strip()
        grab(name, code, logo)
