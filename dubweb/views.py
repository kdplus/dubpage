# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.core import serializers

from .models import UserProfile, Film
import urllib.request
import json
import hashlib


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getUrllibFun(url):
    headers = {'User-agent': 'dubbingshow/9.11.603/fec3a4bf99edefbe(android10;PAFM00;29;1080*2340;official)/5216981'}
    req = urllib.request.Request(url, headers=headers)
    res_data = urllib.request.urlopen(req, timeout=20)
    res = res_data.read()
    res_data.close()
    return res


def get_md5(str):
    digest = hashlib.md5()
    digest.update(str)
    sign = digest.hexdigest()
    return sign


def update_ones_films(userId="5216981"):
    appkey = "193dd7cc7845df55"
    spaceUserId = userId
    token = "eedb1f6271458da491e36580531cce9a"
    extra = "|d62bcbe08764808e"
    # jret_m = ""
    jret = []
    for pg in range(100):
        api = "http://a.api1.peiyinxiu.com/Api/Film/GetMyFilms?"
        param = "appkey=%s&pg=%d&spaceUserId=%s&token=%s&type=0&userId=%s" % (appkey, pg+1, spaceUserId, token, userId)
        sign = get_md5((param + extra).encode("utf8"))
        url = api+param+"&sign="+sign
        restdata = getUrllibFun(url)
        new_jret = json.loads(restdata)["data"]
        if len(new_jret) == 0:
            break
        jret += new_jret
    print("Films get:", len(jret))
    return jret
    # jret_m += (json.dumps(jret, indent=4, separators=(',', ': '), ensure_ascii=False))
    # with open("filmslist.json", "w+") as f:
    #     f.write(jret_m.encode('utf8')


@require_http_methods(["GET"])
def add_user(request):
    response = {}
    try:
        input_user_id = request.GET.get('user_id')
        user_has_image = False 
        try:
            user = UserProfile.objects.get(user_id=input_user_id)
        except UserProfile.DoesNotExist:
            user = None
        if user is None: 
            user = UserProfile(user_id=request.GET.get('user_id'))
            user.save()
            user_has_image = False
        films_info_list = update_ones_films(user.user_id)
        print(len(films_info_list))
        for f_info in films_info_list:
            if not user_has_image:
                user.user_head = f_info["user_head"]
                user.user_name = f_info["user_name"]#.encode("utf8")
                user.save()
                user_has_image = True

            try:
                film = Film.objects.get(film_id=str(f_info["film_id"]))
            except Film.DoesNotExist:
                film = None
            if film is None:
                film = Film(film_id=str(f_info["film_id"]))
            film.film_url = "http://peiyinxiu.com/m/" + film.film_id
            film.user = user
            film.title = f_info["title"] #.encode("utf8")
            film.image_url = f_info["image_url"]
            film.play_count = f_info["play_count"]
            film.good_count = f_info["good_count"]
            film.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        print(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_films(request):
    response = {}
    try:
        input_user_id = request.GET.get('user_id')
        user = None
        if input_user_id != "":
            user = get_object_or_404(UserProfile, user_id=input_user_id)
            films = Film.objects.filter(user=user).extra(
                select={'film_id_i': 'CAST(film_id AS INTEGER)'}
            ).order_by('film_id_i')[::-1]
        else:
            films = Film.objects.extra(
                select={'film_id_i': 'CAST(film_id AS INTEGER)'}
            ).order_by('film_id_i')[::-1]
        response['films'] = json.loads(serializers.serialize("json", films))
        for f in response['films']:
            userpk = f['fields']['user']
            user = get_object_or_404(UserProfile, user_id=userpk)
            f['fields']['user'] = user.user_name
            f['fields']['user_head'] = user.user_head
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
