from django.shortcuts import render, redirect
from django.http import HttpResponse
from hashlib import sha1
from .models import *
from django.http import JsonResponse, HttpResponseRedirect


def register(request):
    context = {'title': '用户注册'}
    return render(request, 'df_user/register.html', context)


# 注册处理
def register_handle(request):
    response = HttpResponse()
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')

    if upwd != ucpwd:
        return redirect('/user/register')
    s1 = sha1()
    s1.update(upwd.encode('utf8'))
    upwd3 = s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    return redirect('/user/login')


# 判断用户是否已经存在
def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


# 登录
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


# 登录处理
def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)
    # 判断如果未查到则用户名错，查到再判断密码是否正确，正确则转到用户中心
    print(len(users))
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info')
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname}
        return render(request, 'df_user/login.html', context)


def info(request):
    uemail = UserInfo.objects.get(id=request.session['user_id']).uemail
    uadress = UserInfo.objects.get(id=request.session['user_id']).uaddress
    context = {
        'title': '用户中心',
        'uemail': uemail,
        'uadress': uadress,
        'uname': request.session['user_name'],
        'page_name': 1,
        'info': 1,
    }
    return render(request, 'df_user/user_center_info.html', context)


def order(request):
    context = {'title': '用户中心', 'page_name': 1, 'order': 1}
    print(111111111111)
    return render(request, 'df_user/user_center_order.html', context)


def user_center_order(request):
    # 构造上下文
    context = {'page_name': 1, 'title': '全部订单', 'pageid': int(''),
               'order': 1, 'orderlist': '', 'plist': '',
               'pre': '', 'next': '', 'pree': '', 'lenn': '', 'nextt': ''}
    return render(request, 'df_user/user_center_order.html', context)


def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.uyoubian = post.get('uyoubian')
        user.save()
    context = {
        'title': '用户中心', 'user': user, 'page_name': 1, 'site': 1
    }
    return render(request, 'df_user/user_center_site.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')