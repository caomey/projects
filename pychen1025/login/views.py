from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def pychen_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('amazon:主页')
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
    else:
        return render(request, 'login.html')
