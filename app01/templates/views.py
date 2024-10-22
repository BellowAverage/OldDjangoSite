from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import user
import os
import re
from django.conf import settings
from app01 import gpt_handle, db_handle
import json
from django.http import JsonResponse
import time
import pandas as pd

def sentiment_inquiry(request):
    return render(request, "sentiment_query.html")

def search_results(request):
    # Retrieve query parameters from the URL
    text_query = request.GET.get('text_query', '')
    min_length = request.GET.get('min_length', '')
    max_length = request.GET.get('max_length', '')

    # Your logic to process the search query and get results
    # ...
    
    '''
    data = {
        'column1': ['Value1', 'Value2'],
        'column2': ['Value3', 'Value4']
    }
    '''

    query_results = pd.read_excel("")
    
    # query_results = text_query

    query_results_list = query_results.to_dict(orient='records')
    
    # Assuming you have a variable named 'query_results' with the search results
    return render(request, 'sentiment_inquiry.html', {'query_results': query_results_list})


# Create your views here.
def redirect2index(request):
    return index(request)


def index(request):
    # ls = user.objects.get(user_account="admin")
    # print(ls.user_id)
    # item = ls.item_set.get(id=1)
    # return HttpResponse("<h1>%s</h1><br></br><p>%s</p>" % (ls.name, item.text))
    # return render(response, "app01/list.html", {"name": ls.name})

    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

    if re.search(r'mobile|android|iphone|ipod|blackberry|iemobile|opera mini|windows phone', user_agent):
        # template_name = 'index_mobile.html'
        template_name = 'index.html'
    else:
        template_name = 'index.html'

    # with open('media/blog_info.json', 'r') as json_file:
    #     blogs = json.load(json_file)
    blogs = db_handle.db_handle(["tech", "bus", "misc"], num=6)

    context = {'blogs': blogs}
    return render(request, template_name, context)
    # return render(request, "index.html", context)


def download_file(request, file_name):
    # Define the file path on the server
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # Open the file and create a response with the file content
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response


def article_viewer(request, blog_name):
    # with open('media/blog_info.json', 'r') as json_file:
    #     blogs = json.load(json_file)
    visitor_ip = get_client_ip(request)

    blogs = db_handle.db_handle(["tech", "bus", "misc"])
    trusted_ip = []
    with open("media/ip_log.txt") as file:
        # 读取文件的每一行
        lines = file.readlines()

        # 初始化一个空数组来存储IP地址部分

    # 遍历每一行并提取IP地址部分
    for line in lines:
        parts = line.split()
        if len(parts) >= 1:
            ip = parts[0]
            trusted_ip.append(ip)

    if blog_name == "call_backend_function":
        call_backend_function(request)

    if blog_name == "all-blogs":
        context = {'viewer': visitor_ip, 'blogs': blogs, 'trusted_ip': trusted_ip}
        return render(request, "blog_table.html", context=context)

    else:
        context = {}
        for blog in blogs:
            if blog.get("title") == blog_name:
                context = {'blog': blog}
                if blog.get("encryption"):
                    return render(request, "blog_viewer.html", context=context)
                if not blog.get("encryption"):
                    return render(request, "blog_viewer_for_pdf.html", context=context)


def call_backend_function(request):
    # 获取访问者的IP地址
    visitor_ip = get_client_ip(request)
    # 写入IP地址到文件
    write_ip_to_file(visitor_ip)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def write_ip_to_file(ip):
    file_path = 'media/ip_log.txt'  # 指定要保存IP地址的文件路径
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    with open(file_path, 'a') as file:
        file.write(ip + ' ')
        file.write(str(current_time) + '\n')


def chat_gpt_request_handle(request, question):
    return HttpResponse(gpt_handle.gpt_response(question))
    # return HttpResponse(question)
    # return HttpResponse("hi")
