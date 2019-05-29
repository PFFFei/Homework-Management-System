from django.urls import re_path,path
from . import views

app_name = 'project'
urlpatterns = [

    # 登陆、注册 以及 信息、密码修改
    path('',views.index,name='index'),
    re_path(r'^register/$',views.register,name='register'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^user/(?P<pk>\d+)/profile/$', views.profile, name='profile'),
    re_path(r'^user/(?P<pk>\d+)/profile/update/$', views.profile_update, name='profile_update'),
    re_path(r'^user/(?P<pk>\d+)/pwdchange/$', views.pwd_change, name='pwd_change'),
    re_path(r'^logout/$', views.logout, name='logout'),

    # 教师创建课程 增 删 查 改
    path('course/', views.CourseList.as_view(), name='course_list'),
    re_path(r'^user/(?P<pk>\d+)/course/$', views.CourseListSelf.as_view(), name='course_list_self'),
    re_path(r'^course/create/$',views.CourseCreate.as_view(), name='course_create'),
    re_path(r'^course/(?P<pk>\d+)/$',views.CourseDetail.as_view(), name='course_detail'),
    re_path(r'^course/(?P<pk>\d+)/update/$',views.CourseUpdate.as_view(), name='course_update'),
    re_path(r'^course/(?P<pk>\d+)/delete$',views.CourseDelete.as_view(), name='course_delete'),
    re_path(r'^course/(?P<pk>\d+)/select$', views.course_select, name='course_select'),
    re_path(r'^course/(?P<pk>\d+)/cancel$', views.course_cancel, name='course_cancel'),

    # 教师发布作业 增 删 查 改
    re_path(r'^course/(?P<pk>\d+)/list$', views.HomeworkList.as_view(), name='homework_list'),
    re_path(r'^course/(?P<pk>\d+)/homework/create/$',views.HomeworkCreate.as_view(), name='homework_create'),
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/$',views.HomeworkDetail.as_view(), name='homework_detail'),
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/update/$',views.HomeworkUpdate.as_view(), name='homework_update'),
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/delete$',views.HomeworkDelete.as_view(), name='homework_delete'),
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/publish/$',views.homework_publish, name='homework_publish'),
    re_path(r'^course/(?P<pk>\d+)/homework/draft/$', views.HomeworkListDraft.as_view(), name='homework_list_publishing'),
    re_path(r'^course/(?P<pk>\d+)/homework/publish/$', views.HomeworkListPublished.as_view(), name='homework_list_published'),
    
    re_path(r'^search/$', views.homework_search, name='homework_search'),
    # 课程作业的评论功能
    re_path(r'^comment/(?P<pk>[0-9]+)/$', views.homework_comment, name='homework_comment'),
    # 学生作业统计
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/count$', views.HomeworkHandin.as_view(), name='homework_handin_count'),

    # 学生提交作业 增 删 查 改
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/list$', views.HandinList.as_view(), name='handin_list'),
    re_path(r'^course/(?P<pk>\d+)/handin/list$', views.HandinListDone.as_view(), name='handin_list_done'),
    re_path(r'^course/(?P<pkr>\d+)/homework/(?P<pk>\d+)/handin/create/$',views.HandinCreate.as_view(), name='handin_create'),
    re_path(r'^course/(?P<pka>\d+)/homework/(?P<pkr>\d+)/handin/(?P<pk>\d+)/$',views.HandinDetail.as_view(), name='handin_detail'),
    re_path(r'^course/(?P<pka>\d+)/homework/(?P<pkr>\d+)/handin/(?P<pk>\d+)/update/$',views.HandinUpdate.as_view(), name='handin_update'),
    re_path(r'^course/(?P<pka>\d+)/homework/(?P<pkr>\d+)/handin/(?P<pk>\d+)/delete/$',views.HandinDelete.as_view(), name='handin_delete'),

    # 课程分组
    re_path(r'^course/(?P<pk>\d+)/student$', views.course_student, name='course_student'),
    re_path(r'^course/(?P<pk>\d+)/group$', views.GroupList.as_view(), name='group_list'),
    # re_path(r'^course/(?P<pk>\d+)/group/create/$', views.GroupCreate.as_view(), name='group_create'),
    re_path(r'^course/(?P<pkr>\d+)/group/(?P<pk>\d+)/delete/$', views.GroupDelete.as_view(), name='group_delete'),
    re_path(r'^course/(?P<pk>\d+)/course/group/create$', views.course_group_create, name='course_group_create'),
]
