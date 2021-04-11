import time
import requests
import os
HA_HOST = os.environ.get('HA_HOST')
HA_TOKEN = os.environ.get('HA_TOKEN')

HTTP_BASE = "http://{}".format(HA_HOST)
headers = {
    "Authorization": "Bearer {}".format(HA_TOKEN),
    "content-type": "application/json",
}


class HA:
    def get_temp(self):
        url = '{}/api/states/sensor.hue_motion_sensor_1_temperature'.format(HTTP_BASE)
        resp = requests.get(url, headers=headers)
        resp_json = resp.json()
        temp = resp_json['state']
        return temp

    def get_now_playing(self):
        url = '{}/api/states/media_player.bedroom_speaker'.format(HTTP_BASE)
        resp = requests.get(url, headers=headers)
        resp_json = resp.json()
        attr = resp_json['attributes']
        artist = attr.get('media_artist',attr.get('media_album_artist', ''))
        title = attr.get('media_title','')
        state = resp_json['state']
        if state == 'playing':
            return '%s - %s' %(artist, title)
        else:
            return None
        return resp_json
