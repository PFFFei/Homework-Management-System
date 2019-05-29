from django.urls import path,re_path
from . import views


app_name = 'notice'
urlpatterns = [
    path('notice/', views.NoticeList.as_view(), name='notice'),
    re_path(r'^notice/(?P<pk>[0-9]+)/$', views.NoticeDetail.as_view(), name='detail'),
    
    # 通知搜索
    path('notice/search/', views.notice_search, name='notice_search'),

]