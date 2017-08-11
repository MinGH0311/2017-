# -*- encoding: utf-8 -*-

import base64
from .models import user_info
from django.shortcuts import render, redirect
import hashlib
import random
import smtplib
from email.mime.text import MIMEText
import email.utils
import json

def get_current_user(request):
    try:
        cur_user = request.COOKIES.get('ec')
    except Exception, e:
        print e
        return -1
    try:
        user = user_info.objects.get(user_email=base64.b64decode(cur_user))
    except Exception, e:
        print e
        return -1
    return user

def login(request):
    if request.method == 'POST':
        try:
            user = user_info.objects.get(user_id=request.POST.get('user_id'),
                                         user_pw=hashlib.md5(request.POST.get('user_pw')).hexdigest())
            http = redirect('/')
            http.set_cookie(key="ic", value=hashlib.md5(user.user_id).hexdigest())
            http.set_cookie(key="pc", value=hashlib.md5(user.user_email).hexdigest())
            http.set_cookie(key="ec", value=base64.b64encode(user.user_email))
            return http
        except Exception, e:
            print e
            message = {'error': 'Incorrect Id or Password', 'title':'ML(MyLanguage) Login'}
            return render(request, 'login.html', message)
    return render(request, 'login.html', {'title':'ML(MyLanguage) Login'})

def register(request):
    ctx = {'title':'회원가입'}
    if request.method == 'POST':
        try:
            user_info.objects.get(user_email=request.POST.get('user_email'))
            message = {'error': 'Email address is already inuse', 'title':'Error'}
            return render(request, 'register.html', message)
        except Exception, e:
            print e
            new_user = user_info()
            new_user.user_id = request.POST.get('user_id')
            new_user.user_pw = hashlib.md5(request.POST.get('user_pw')).hexdigest()
            new_user.user_email = request.POST.get('user_email')
            new_user.save()
            return redirect('/login/')
    return render(request, 'register.html', ctx)

def find_id(request):
    ctx = {'title':"아이디/비밀번호 찾기"}
    if request.method == 'POST':
        key_pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        tmp_id = ''
        tmp_pw = ''
        try:
            with open('./LangPi/Secret', 'r') as f:
                data = f.read()
            data = json.loads(data)
            user = user_info.objects.get(user_email=request.POST.get('user_email'))
            for _ in range(10):
                tmp_id += key_pool[random.randrange(0, len(key_pool))]
                tmp_pw += key_pool[random.randrange(0, len(key_pool))]
            message = 'Your new ID: %s\nYour new Password: %s\n' % (tmp_id, tmp_pw)
            msg = MIMEText(message)
            msg['To'] = email.utils.formataddr(('To User', request.POST.get('user_email')))
            msg['From'] = email.utils.formataddr(('From Mylang Web', 'parksjin01@naver.com'))
            msg['Subject'] = 'Your temporary ID and Password'
            smtp = smtplib.SMTP_SSL('smtp.naver.com', 465)
            smtp.ehlo()
            smtp.login(data['id'], data['pw'])
            smtp.sendmail('parksjin01@naver.com', [request.POST.get('user_email')], msg.as_string())
            smtp.close()
            user.user_id = tmp_id
            user.user_pw = hashlib.md5(tmp_pw).hexdigest()
            user.save()
        except Exception, e:
            print e
        return redirect('/')
    return render(request, 'find-id.html', ctx)

def change_id(request):
    ctx = {'title':'아이디 변경'}
    ctx['user_id'] = get_current_user(request).user_id
    if request.method == 'POST':
        next_id = request.POST.get('user_id')
        next_pw = hashlib.md5(request.POST.get('user_pw')).hexdigest()
        cur_email = base64.b64decode(request.COOKIES.get('ec'))
        user = user_info.objects.get(user_email=cur_email)
        user.user_id = next_id
        user.user_pw = next_pw
        user.save()
        return redirect('/')
    return render(request, 'change-id.html', ctx)