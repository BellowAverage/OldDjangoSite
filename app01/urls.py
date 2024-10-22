from django.urls import path

from . import views

urlpatterns = [
    # path("<str:name>", views.index, name="index"),
    # path("v1/", views.view1, name="view 1"),
    path("", views.redirect2index, name="redirect2index"),
    path("index/", views.index, name="index"),
    # path("index/home", views.home, name="home"),
    # path("create/", views.create, name="create"),
    path('download/<str:file_name>', views.download_file, name='file_download'),
    path('ai_voice_assistant_handle/<str:question>', views.chat_gpt_request_handle, name="ai_str"),
    # path('ai_voice_assistant_handle/', views.chat_gpt_request_handle, name="ai"),
    path('blog/<str:blog_name>', views.article_viewer, name="article_viewer"),
    path('xd/sentiment_query/query/', views.sentiment_query, name='sentiment_query'),
    path('xd/sentiment_query/querysql/', views.sentiment_query_sql, name='sentiment_query_sql'),
    path('xd/sentiment_query/', views.sentiment_query_0, name='sentiment_query_0'),
    path('xd/SLSentiment', views.sl_sentiment, name='sl_sentiment'),
    path('xd/DataDiagram', views.data_diagram, name='data_diagram'),
    path('steamdb/overview/', views.steamdb_overview, name='steamdb_overview'),
    path('steamdb/', views.steamdb, name='steamdb'),
    path('gyh/', views.gyh, name='gyh'),
    path('xd/login_home/', views.login_home, name='login_home'),
    path('xd/login', views.login, name='login'),
    path('xd/logout', views.logout, name='logout'),
    path('upload_handle/', views.upload_handle, name='upload_handle'),
    path('data_source_selection/', views.data_source_selection, name='data_source_selection'),
    path('test/', views.test, name='test'),
    path('xd/RankSqlGenerator', views.rank_sqlGenerator, name='rank_sqlGenerator'),
    path('xd/RankSqlGenerator/generate/', views.rank_sqlGenerator_form_handle, name='rank_sqlGenerator_form_handle'),

    # path('my-ajax-endpoint/', views.my_ajax_endpoint, name='my_ajax_endpoint'),
    # path('call_backend_function', views.call_backend_function, name='call_backend_function'),
    # 其他URL配置
]
