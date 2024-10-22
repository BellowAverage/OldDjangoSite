from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import user
import os
import re
from django.conf import settings
from app01 import gpt_handle, db_handle
import json
from django.http import JsonResponse
import time
import pandas as pd
from django.template.loader import render_to_string

def test(request):
    return render(request, 'test.html')


def steamdb(request):
    from app01.utils import steamdb
    import re

    # df = steamdb.topsellers()
    df = steamdb.offline_topsellers()

    df['Final Price'] = df['累计充值rmb']

    games = df['玩家pid'].tolist()
    discounts = df['Final Price'].astype(float).tolist()

    context = {'games': games, 'discounts': discounts}

    return render(request, 'echart.html', context)


def steamdb_overview(request):
    keys = ['text_query', 'min_length', 'max_length', 'sentiment', 'gpt_class']

    context = {}

    if request.method == 'GET':
        for key in keys:
            context[key] = request.GET.get(key)
    else:
        for key in keys:
            context[key] = None

    return render(request, "steamdb_overview.html", context)


# --------------------------------------------------------
# test section

def sl_sentiment(request):
    return render(request, "xd_menu.html")


def gyh(request):
    return render(request, "static/index.html")


# ---------------------------------------------------------
# login section

def login_home(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES:
        context = {'username': request.COOKIES['username'],
                   'login_status': request.COOKIES.get('login_status'), }
        return render(request, 'login_home.html', context)
    else:
        return render(request, 'login_home.html')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == "POST":
        username = request.POST.get('email')

        context = {
            'username': username,
            'login_status': True,
        }

        response = render(request, 'login.html', context)

        response.set_cookie('username', username)
        response.set_cookie('login_status', True)

        return response

    # return render(request, 'login.html')


def logout(request):
    response = HttpResponseRedirect(reverse('login'))

    response.delete_cookie('username')
    response.delete_cookie('login_status')

    return response

# ---------------------------------------------------------
# rank_sqlGenerator section

def rank_sqlGenerator(request):
    return render(request, "rank_sqlGenerator.html")


def rank_sqlGenerator_form_handle(request):
    from app01.utils.RankSqlGenerator import SQLGenerator

    profession = request.GET.get('profession', '')
    date = request.GET.get('date', '')
    noStudio = request.GET.get('noStudio')
    active3Days = request.GET.get('active3Days')

    generator = SQLGenerator(date=str(date), profession=str(profession), if_studio_flag=str(noStudio), if_active_days_3d=str(active3Days))
    sql_res = generator.generate_sql()
    
    # Prepare the context with the result of SQL generation
    context = {
        "profession": str(profession),
        "date": date,
        "noStudio": noStudio,
        "active3Days": active3Days,
        "sql_res": sql_res
    }

    return JsonResponse(context)


# ---------------------------------------------------------
# data_diagram section

def data_source_selection(request):
    if request.method == 'POST':

        selected_data_source = request.POST.get('data_source_selection')
        text_data = str(selected_data_source)

        try:
            
            with open('media/output.txt', 'w', encoding='utf-8') as file:
                # 写入字符串
                file.write(text_data)
                sentiment_query(request)

            # 可选：返回成功的响应
            return JsonResponse({'status': 'success', 'message': 'Data source selected.'})
        except IOError as e:
            # 可选：如果出现错误，返回错误的响应
            return JsonResponse({'status': 'error', 'message': str(e)})

    # 如果请求方法不是POST，返回错误或者其他逻辑
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def upload_handle(request):
    if request.method == 'POST':
        try:
            
            csv_file = request.FILES['csvFile']
            if not csv_file.name.endswith('.csv'):
                return JsonResponse({'error': '请上传.csv格式的文件~'}, status=400)

            data = pd.read_csv(csv_file, encoding='utf-8')
            save_name = 'media/xd_data_set/' + str(csv_file.name)
            data.to_csv(save_name, encoding='utf-8', index=False)

            return JsonResponse({'success': '文件上传成功！'})
        except Exception as e:
            return JsonResponse({'error': f'文件上传失败：{str(e)}'}, status=500)

    return JsonResponse({'error': '未知错误，请联系管理员~'}, status=400)


def data_diagram(request):
    return render(request, "data_diagram.html")


# ---------------------------------------------------------
# sentiment_query section

def sentiment_query_0(request):
    text_query = ''
    min_length = '0'
    max_length = '100'
    sentiment_direction = 'all'
    minLength_level = '0'
    maxLength_level = '60'
    minLength_rmb = '0'
    maxLength_rmb = '100000'

    directory = 'media/xd_data_set'
    file_names = []
    for filename in os.listdir(directory):
        file_names.append(filename)
    
    
    data_source_selection = "铃兰反馈数据_0325.csv"
    file_address = "media/xd_data_set/" + data_source_selection
    df_res = pd.read_csv(file_address, usecols=["Source"])
    unique_values = df_res['Source'].unique().tolist()
    

    dict_return = {"text_query": text_query, "min_length": min_length,
                   "max_length": max_length, "sentiment": sentiment_direction, "IsFirst": "True",
                   "minLength_level": minLength_level,
                   "maxLength_level": maxLength_level, "minLength_rmb": minLength_rmb,
                   "maxLength_rmb": maxLength_rmb, "data_set_names": file_names, "unique_values": unique_values}

    
    
    return render(request, 'sentiment_query.html', {'dict_return': dict_return})


def sentiment_query_sql(request):
    from app01.utils.mysqlconn import GetFromMySQL, GetFromMySQLNoPandas

    text_query_sql = request.GET.get('text_query_sql', '')

    # df_res = GetFromMySQL(text_query_sql)
    #
    # query_results_list = df_res.to_dict(orient='records')

    query_results_list = GetFromMySQLNoPandas(text_query_sql)

    html = render_to_string('partials/search_results.html',
                            {'query_results': query_results_list})

    # Return the HTML snippet as a response
    return HttpResponse(html)


def sentiment_query(request):
    from app01.utils.mysqlconn import GetFromMySQL, GetFromMySQLNoPandas
    from app01.utils.sqlGenerator import ljyGetFromMySql
    import os
    # Retrieve query parameters from the URL

    data_source_selection = request.GET.get('data_source_selection', '')
    text_query = request.GET.get('text_query', '')
    min_length = request.GET.get('min_length', '')
    max_length = request.GET.get('max_length', '')
    sentiment_direction = request.GET.get('sentiment', '')
    minLength_level = request.GET.get('minLength_level', '')
    maxLength_level = request.GET.get('maxLength_level', '')
    minLength_rmb = request.GET.get('minLength_rmb', '')
    maxLength_rmb = request.GET.get('maxLength_rmb', '')
    sentiment_source = request.GET.get('sentiment_source', '')

    if text_query == '':
        text_query = ''
    if min_length == '':
        min_length = '0'
    if max_length == '':
        max_length = '100'

    if minLength_level == '':
        minLength_level = '0'
    if maxLength_level == '':
        maxLength_level = '60'

    if minLength_rmb == '':
        minLength_rmb = '0'
    if maxLength_rmb == '':
        maxLength_rmb = '100000'

    if sentiment_direction == '':
        sentiment_direction = 'all'

    if sentiment_source == '':
        sentiment_source = 'all'

    if data_source_selection == '':
        data_source_selection = "铃兰反馈测试上传文件.csv"

    directory = 'media/xd_data_set'
    file_names = []
    for filename in os.listdir(directory):
        file_names.append(filename)


    # df_a = pd.read_excel("media/PositiveComments.xlsx")
    # df_b = pd.read_excel("media/NegativeComments.xlsx")
    # df_res = pd.concat([df_a, df_b], ignore_index=True)

    # query = 'SELECT * FROM dim_sentiment'

    # use sql

    '''
    query = ljyGetFromMySql(text_query, min_length, max_length, sentiment_direction, minLength_level, maxLength_level,
                            minLength_rmb,
                            maxLength_rmb)

    query_results_list = GetFromMySQLNoPandas(query)
    '''

    # use pandas

    file_address = "media/xd_data_set/" + data_source_selection
    df_res = pd.read_csv(file_address)
    # df_res = pd.read_csv("media/xd_data_set/铃兰反馈测试上传文件.csv")

    # df_res = pd.read_excel("media/PositiveComments.xlsx")
    # df_res = pd.read_excel("media/Comments.xlsx")

    # if sentiment_direction == "all":
    #     # df_a = pd.read_excel("media/PositiveComments.xlsx")
    #     # df_b = pd.read_excel("media/NegativeComments.xlsx")
    #     # df_res = pd.concat([df_a, df_b], ignore_index=True)
    #     # df_res = GetFromMySQL(query)
    #     pass

    # df_res.to_excel("media/Comments.xlsx")

    # -------------------------------------------------------

    if sentiment_direction == "Positive":
        # df_res = pd.read_excel("media/PositiveComments.xlsx")
        df_res = df_res[df_res["情感分类"] == "满意"]

    elif sentiment_direction == "Negative":
        # df_res = pd.read_excel("media/NegativeComments.xlsx")
        df_res = df_res[(df_res["情感分类"] == "不满") | (df_res["情感分类"] == "极不满")]

    if text_query:
        df_res = df_res[df_res["评论内容"].str.contains(text_query)]

    if min_length:
        min_length = int(min_length)
    else:
        min_length = 0

    if max_length:
        max_length = int(max_length)
    else:
        max_length = float('inf')

    if minLength_level:
        minLength_level = int(minLength_level)
    else:
        minLength_level = 0

    if maxLength_level:
        maxLength_level = int(maxLength_level)
    else:
        maxLength_level = float('inf')

    if minLength_rmb:
        minLength_rmb = int(minLength_rmb)
    else:
        minLength_rmb = 0

    if maxLength_rmb:
        maxLength_rmb = int(maxLength_rmb)
    else:
        maxLength_rmb = float('inf')

    df_res = df_res[(df_res["评论内容"].str.len() >= min_length) &
                    (df_res["评论内容"].str.len() <= max_length)]

    df_res = df_res[(df_res["玩家等级"] >= minLength_level) &
                    (df_res["玩家等级"] <= maxLength_level)]

    df_res = df_res[(df_res["累计充值rmb"] >= minLength_rmb) &
                    (df_res["累计充值rmb"] <= maxLength_rmb)]
    
    unique_values = df_res['Source'].unique().tolist()
    
    # test log
    with open("media/test_log.txt", "w") as file:
        for value in unique_values:
            file.write(str(value) + "\n")

    if sentiment_source != "all":
        for value in unique_values:
            if sentiment_source == value:
                df_res = df_res[df_res["Source"] == value]

    # query_results_list = df_res.to_dict(orient='records')

    query_results_list = df_res.to_dict(orient='records')
    # -------------------------------------------------------
    
    dict_return = {"text_query": text_query, "min_length": min_length,
                   "max_length": max_length, "sentiment": sentiment_direction, "minLength_level": minLength_level,
                   "maxLength_level": maxLength_level, "minLength_rmb": minLength_rmb,
                   "maxLength_rmb": maxLength_rmb, "sentiment_source": sentiment_source, "data_set_names": file_names, "unique_values": unique_values}

    html = render_to_string('partials/search_results.html',
                            {'query_results': query_results_list, 'dict_return': dict_return})

    # Return the HTML snippet as a response
    return HttpResponse(html)


# ---------------------------------------------------------

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
        response = HttpResponse(
            f.read(), content_type='application/force-download')
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
        context = {'viewer': visitor_ip,
                   'blogs': blogs, 'trusted_ip': trusted_ip}
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
