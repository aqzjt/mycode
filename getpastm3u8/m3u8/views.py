from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
import time
from m3u8 import models

#ts切片入库方法
@csrf_exempt
def inputts(request):
    if request.method == "GET":
        resp = {'errorcode': 102, 'detail': 'do not use get mathod'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    elif request.method == "POST":
        postbody = request.body
        postjson = json.loads(postbody)
        app = postjson["app"]
        stream = postjson['stream']
        duration = postjson['duration']
        file = postjson['file']
        if (app and stream and duration and file):
            ts = file.split("/")[8].split("-")[1].replace(".ts", "")
            print(app, stream, duration, ts)
            models.App.objects.get_or_create(app=app)
            models.Stream.objects.get_or_create(stream=stream)
            models.Ts.objects.get_or_create(app=models.App.objects.get(app=app),
                                            stream=models.Stream.objects.get(stream=stream),
                                            duration=duration, ts=int(ts))
        # 0表示回调成功
        return HttpResponse(0)

#获取指定时间戳的M3U8文件的方法
def getm3u8(request):
    starttime = request.GET.get("starttime")
    endtime = request.GET.get("endtime")
    app = request.path.split("/")[1]
    stream = request.path.split("/")[2].replace(".m3u8", "")
    print(starttime, endtime, app, stream)
    try:
        # 转化为毫秒级别的时间戳
        starttime_timestamp = time.mktime(time.strptime(starttime, "%Y-%m-%d_%H:%M:%S"))*1000
        endtime_timestamp = time.mktime(time.strptime(endtime, "%Y-%m-%d_%H:%M:%S"))*1000
        # print(starttime_timestamp,endtime_timestamp)
        if app and stream and (int(endtime_timestamp) > int(starttime_timestamp)):
            result = models.Ts.objects.filter(app__app=app).filter(stream__stream=stream). \
                filter(ts__gte=starttime_timestamp).filter(ts__lte=endtime_timestamp)
            if result.__len__() != 0:
                tslist = list()
                for i in result:
                    tslist.append({'app': app, 'stream': stream, 'duration': i.duration, 'ts': i.ts})
                m3u8file = makem3u8(tslist)
                return HttpResponse(m3u8file, content_type="video/MP2T")
            else:
                resp = {'errorcode': 100, 'detail': 'please check your app stream starttime and endtime'}
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {'errorcode': 100, 'detail': 'please check your app stream starttime and endtime'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
    except:
        resp = {'errorcode': 101, 'detail': 'please check your starttime or endtime'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

#制作M3U8文件方法
def makem3u8(tslist):
    m3u8file = "#EXTM3\n#EXT-X-VERSION:3\n#EXT-X-MEDIA-SEQUENCE:0\n#EXT-X-TARGETDURATION:15\n"
    for tsmessage in tslist:
        m3u8file = m3u8file + "#EXTINF:" + str(tsmessage["duration"]) + ", no desc\n" \
                   + tsmessage["stream"] + "-" + str(tsmessage["ts"]) + "\n"
    m3u8file = m3u8file + "#EXT-X-ENDLIST"
    print(tslist)
    return m3u8file

