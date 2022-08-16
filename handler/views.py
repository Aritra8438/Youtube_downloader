import os
from django.shortcuts import render
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from pytube import YouTube

qSet = "to_be_asigned"
title = "to_be_asigned"

def index(request):
    return render(request,'index.html')

def choose(request):
    global qSet
    global title
    link = request.GET.get('link')
    try:
        youtube = YouTube(
            link,
            use_oauth=False,
            allow_oauth_cache=True
        )
    except:
        return render(request,'failure.html')
    res_list = []
    qSet = youtube.streams.filter(subtype='mp4')
    for q in qSet:
        res_list.append(q.resolution)
    res_list = list(filter(lambda item: item is not None,res_list))
    res_set = set(res_list)
    title = youtube.title
    return render(request, 'result.html',{'title': youtube.title, 'resolutions': ' '.join(res_set)})

def getFile(request):
    global qSet
    res = request.GET.get('res')
    video = qSet.filter(resolution=res).first()
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    path = 'temp/download.mp4'
    abs_path = os.path.join(BASE_DIR,path)
    try:
        os.remove(abs_path)
    except:
        pass
    try:
        abs_path = video.download('temp/', filename='download.mp4')
        file = FileWrapper(open(path, 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename=' + title + '.mp4'
        os.remove(abs_path)
        return response
    except:
        return render(request,'failure.html')
