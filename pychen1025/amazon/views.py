from django.shortcuts import render, redirect
from .models import AsinInfo
from .models import GmMonitor
from .models import MonitorAsin
from django.http import HttpResponse
import django.utils.timezone as timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def collect(request, asin):
    # collection == 0不收藏collection == 1收藏
    a = AsinInfo.objects.get(asin=asin)
    a.collection = request.POST['collection']
    a.save()
    return HttpResponse('OK')


def alibaba(request, asin):
    # 1688链接统一放到需要监测的asin库monitor_asin中
    a = MonitorAsin.objects.get(asin=asin)
    a.alibaba_link = request.POST['1688']
    a.save()
    if request.POST['url'] == 'index':  # 如果是主页爬取的asin还需修改链接，用于home呈现链接
        # 货源链接存放在了2个数据库
        a = AsinInfo.objects.get(asin=asin)
        a.alibaba_link = request.POST['1688']
        a.save()
    return HttpResponse('OK')


def monitor(request, asin):
    # asin_info监测的asin和手动监测asin都存放在monitor_asin里面
    if request.POST['monitor'] == '取消监测':
        a = MonitorAsin.objects.get(asin=asin)
        a.delete()
        # 分辨不了哪个是手动添加的，取消监测
    elif request.POST['monitor'] == '开始监测':
        a = MonitorAsin.objects.create(asin=asin, update_time=timezone.now(), alibaba_link='0')
        a.save()
    return HttpResponse('OK')


def readInfo(request, update_time):
    # 只需要每个日期取出一个值用来存储阅读记录即可，遍历时只要有一个值就可以
    read_rows = request.POST['read_rows']
    a = AsinInfo.objects.filter(update_time__contains=update_time)[0]
    a.readinfo = read_rows
    a.save()
    return HttpResponse('OK')

@login_required
# 跟卖数据，交互的数据库为:amazon -> asin_info
def home(request):
    update_time = AsinInfo.objects.order_by('update_time').values_list('update_time')
    update_time = list(map(lambda x: x[0][:10], update_time))
    update_time = sorted(list(set(update_time)), reverse=True)
    print(update_time)
    asin_list = AsinInfo.objects.filter(update_time__contains=update_time[0]).order_by('rank')  # 默认取出最新一天找的跟卖
    if request.POST:
        asin_list = AsinInfo.objects.filter(update_time__contains=request.POST['date']).order_by('rank')
        if request.POST['collection'] == '已收藏的产品':
            asin_list = AsinInfo.objects.filter(collection='1').order_by('-rank')
            count = len(asin_list)
            content = {'跟卖listings': asin_list, '数据获取时间': update_time, '选择时间': request.POST['date'], '计数': count,
                       'collection': 1}
            return render(request, 'index.html', content)
        count = len(asin_list)
        content = {'跟卖listings': asin_list, '数据获取时间': update_time, '选择时间': request.POST['date'], '计数': count,
                   'collection': 0}
        return render(request, 'index.html', content)
    else:
        count = len(asin_list)
        content = {'跟卖listings': asin_list, '数据获取时间': update_time, '选择时间': update_time[0], '计数': count, 'collection': 0}
        return render(request, 'index.html', content)


@login_required
# 跟卖监测网页，交互的数据库为:amazon -> gm_monitor
def chart(request):
    # chart页面渲染需要用到两个数据库的信息，一个是gm_monitor的监测信息，一个是monitor_asin的阿里巴巴链接，
    # 可以将两个数据库信息的信息在views中加工到一起，去templates中变量计算很麻烦，因为监测asin是唯一的，顺序可以对上，所以合并到一起不难
    # 获取阿里巴巴链接信息，数据库为amazon->monitor_asin
    # 获取跟卖信息  ,数据库为amazon->monitor_asin
    asin_list = MonitorAsin.objects.values_list('asin')  # 默认取出所有的asin
    asin_list = list(map(lambda x: x[0], asin_list))  # 将QuerySet迭代转换成列表
    count = len(asin_list)
    gmMonitor = []
    a = 24  # 默认显示24小时
    if request.POST:
        if request.POST['time'] == '48小时':
            a = 48
        elif request.POST['time'] == '一周':
            a = 168
    for asin in asin_list:
        dict = {}
        asin_info = GmMonitor.objects.filter(asin=asin).order_by('-update_time')[:a]  # 每个asin最后24个值，代表24个小时
        alibaba_link = MonitorAsin.objects.filter(asin=asin).values_list('alibaba_link')[0][0]  # monitor_asin数据库的数据
        img = asin_info.values_list('img')
        img = list(map(lambda x: x[0], img))
        if len(img) == 0:
            continue
        else:
            img = img[0]
        brand = asin_info.values_list('brand')[0][0]
        rank = asin_info.values_list('ranks')[0][0]
        price = asin_info.values_list('price')[0][0]
        registered = asin_info.values_list('registered')[0][0]
        # 取出所有卖家
        sellers = asin_info.values_list('seller')
        sellers = list(map(lambda x: x[0], sellers))  # 将QuerySet迭代转换成列表
        sellers = list(set(sellers))  # sellers去重
        sellers = ','.join(sellers)
        dict['asin'] = asin
        dict['img'] = img
        dict['brand'] = brand
        dict['rank'] = rank
        dict['price'] = price
        dict['registered'] = registered
        dict['alibaba_link'] = alibaba_link
        dict['sellers'] = sellers
        # 判断品牌是否变化
        brand = asin_info.values_list('brand')
        brand = list(map(lambda x: x[0], brand))  # 将QuerySet迭代转换成列表
        brand = list(set(brand))  # sellers去重
        if len(brand) > 1:
            if 'null' not in brand:
                brand_change = 'YES'
        else:
            brand_change = 'NO'
        # 判断标题是否变化
        title = asin_info.values_list('title')
        title = list(map(lambda x: x[0], title))  # 将QuerySet迭代转换成列表
        title = list(set(title))  # sellers去重
        if len(title) > 1:
            if 'null' not in brand:
                title_change = 'YES'
        else:
            title_change = 'NO'
        # 判断图片是否变化
        img = asin_info.values_list('img')
        img = list(map(lambda x: x[0], img))  # 将QuerySet迭代转换成列表
        while 'null' in img:
            img.remove('null')
        img = list(map(lambda x: x.split('I/')[-1].split('.')[0], img))  # 过滤尺寸的变化
        img = list(set(img))  # sellers去重
        if len(img) > 1:
            img_change = 'YES'
        else:
            img_change = 'NO'
        dict['brand_change'] = brand_change
        dict['title_change'] = title_change
        dict['img_change'] = img_change
        # 时间坐标轴
        update_time = asin_info.values_list('update_time')
        update_time = list(map(lambda x: x[0][8:13].replace(' ', '-'), update_time))
        dict['li_time'] = list(reversed(update_time))
        gmMonitor.append(dict)
        ranks = asin_info.values_list('ranks')
        ranks = list(map(lambda x: x[0], ranks))
        seller = asin_info.values_list('seller')
        seller = list(map(lambda x: x[0], seller))
        price = asin_info.values_list('price')
        price = list(map(lambda x: x[0], price))
        seller1 = asin_info.values_list('seller1')
        seller1 = list(map(lambda x: x[0], seller1))
        price1 = asin_info.values_list('price1')
        price1 = list(map(lambda x: x[0], price1))
        y, p1, s1, P1, S1, P2, S2 = seller_match(update_time, ranks, seller, seller1, price, price1)
        dict['ranks'] = list(reversed(y))
        dict['p1'] = list(reversed(p1))
        dict['s1'] = s1
        dict['P1'] = list(reversed(P1))
        dict['S1'] = S1
        dict['P2'] = list(reversed(P2))
        dict['S2'] = S2
    content = {'data': gmMonitor, '计数': count}
    return render(request, 'hightchart.html', content)


def seller_match(times, ranks, sellers, seller1s, prices, price1s):
    x = times  # 时间列表
    y = ranks  # 排名列表
    s1 = sellers  # 购物车卖家
    s2 = seller1s  # 卖家2价格列表0
    p1 = prices  # 购物车价格列表
    p2 = price1s  # 卖家2
    li = []  # 按时间段来新建一个列表，每个时间段一个字典，包含 买家对应价格的键值对
    for i in range(len(x)):
        dict = {}
        dict[s1[i]] = p1[i]
        dict[s2[i]] = p2[i]
        li.append(dict)
    # print(li)
    seller_set = list(set(s1))
    # print(seller_set)
    P1 = []
    P2 = []
    if len(seller_set) == 1:  # 购物车一直是一个人的
        # print('购物车一直没变')
        P1 = p1
        P2 = p2
        S1 = seller_set[0]
        seller_set2 = list(set(s2))
        while 'null' in seller_set2:
            seller_set2.remove('null')
        if seller_set2:
            S2 = seller_set2[0]
        else:
            S2 = 'null'
    else:
        # print('有人跟卖')
        S1 = seller_set[0]
        S2 = seller_set[1]
        for i in li:
            if seller_set[0] in i:
                P1.append(i[seller_set[0]])
            else:
                P1.append(0)
            if seller_set[1] in i:
                P2.append(i[seller_set[1]])
            else:
                P2.append(0)
    # 将排名转换成数字
    for i in range(len(y)):
        y[i] = int(y[i])
    # 将价格转换成数字
    for i in range(len(p1)):
        p1[i] = float(p1[i])
    for i in range(len(P1)):
        P1[i] = float(P1[i])
    for i in range(len(P2)):
        P2[i] = float(P2[i])
    return y, p1, s1, P1, S1, P2, S2
