#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .youkujs import *
from ykdl.extractor import VideoExtractor
from ykdl.videoinfo import VideoInfo
from ykdl.util.html import get_content

import json
import base64, time

class Acorig(VideoExtractor):
    name = u"AcFun 优酷合作视频"

    client_id = '908a519d032263f8'
    ct = 85
    refer = 'http://player-vod.cn-beijing.aliyuncs.com/player/2017030915/core/cloud.swf'
    key = "8bdc7e1a"

    def prepare(self):
        info = VideoInfo(self.name)
        self.vid, self.embsig = self.vid

        api = "http://aauth-vod.cn-beijing.aliyuncs.com/acfun/web?vid={}&ct={}&time={}&sign={}&ev=3".format(self.vid, self.ct,int(time.time()*1000), self.embsig)
        data = rc4(self.key, base64.b64decode(json.loads(get_content(api, charset='utf-8'))['data']))
        stream_data = json.loads(data)
        info.title = stream_data['video']['title']
        for s in stream_data['stream']:
            if 'segs' in s:
                stream_type = stream_code_to_id[s['stream_type']]
                stream_urls=[]
                for x in s['segs']:
                    stream_urls.append((x['url'],x['total_milliseconds_video']))
                size = s['total_size']
                info.stream_types.append(stream_type)
                info.streams[stream_type] = {'container': 'mp4', 'video_profile': stream_code_to_profiles[stream_type], 'src': stream_urls, 'size' : size}
        info.stream_types = sorted(info.stream_types, key=ids.index)
        return info

site = Acorig()
