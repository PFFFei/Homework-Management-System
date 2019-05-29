from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView
from .models import Teacher,Student,Course,Homework,Handin,Comment,Group,Role
from .forms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm,CourseForm,HomeworkForm,HandinForm,CommentForm,GroupForm
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy

import uuid
from django.http import JsonResponse
from PIL import Image
import os
import json

def index(request):
    return render(request,'project/index.html')

def register(request):
    if request.method == 'POST':
        # 验证表单RegistrationForm的数据是否有效
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            role = form.cleaned_data['role']
            # 使用内置User自带create_user方法创建用户，不需要使用save()
            user = User.objects.create_user(username=username, password=password)
            role_profile = Role(role=int(role),user=user)
            role_profile.save()
            # 如果直接使用objects.create()方法后不需要使用save()
            if int(role) == 0:
                user_profile = Student(user=role_profile)
                user_profile.save()
            else:
                user_profile = Teacher(user=role_profile)
                user_profile.save()
            #  注册成功，通过HttpResponseRedirect方法转到登陆页面
            return HttpResponseRedirect("/login/")
    else:
        form = RegistrationForm()
    return render(request, 'project/registration.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 调用Django自带的auth.authenticate() 来验证用户名和密码是否正确
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
            	# 调用auth.login()来进行登录
                auth.login(request, user)
                # 登录成功，转到用户个人信息页面
                # []是有序的可reverse，{}是无序的
                return HttpResponseRedirect(reverse('project:index'))
                # return HttpResponseRedirect(reverse('ducoments:article_list'))
            else:
                # 登陆失败
                return render(request, 'project/login.html', {'form': form,'message': '密码错误，请重试！'})
    else:
    	# 如果用户没有提交表单或不是通过POST方法提交表单，转到登录页面，生成一张空的LoginForm
        form = LoginForm()
    return render(request, 'project/login.html', {'form': form})

@login_required
def profile(request,pk):
	user = get_object_or_404(User,pk=pk)
	return render(request,'project/profile.html',{'user':user})

@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    # user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            if request.user.role.role == 0:
                user.role.student.name = form.cleaned_data['name']
                user.role.student.gender = form.cleaned_data['gender']
                user.role.student.save()
                return HttpResponseRedirect(reverse('project:profile', args=[user.id]))
            else:
                user.role.teacher.name = form.cleaned_data['name']
                user.role.teacher.gender = form.cleaned_data['gender']
                user.role.teacher.save()
                return HttpResponseRedirect(reverse('project:profile', args=[user.id]))
    else:
        if request.user.role.role == 0:
            default_data = {'name': user.role.student.name, 
                            'gender': user.role.student.gender,
                        }
        else:
            default_data = {'name': user.role.teacher.name, 
                            'gender': user.role.teacher.gender,
                        }
        form = ProfileForm(default_data)

    return render(request, 'project/profile_update.html', {'form': form, 'user': user})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data['old_password']
            username = user.username
            
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect("/login/")

            else:
                return render(request, 'project/pwd_change.html', {'form': form,'user': user, 'message': '原密码错误，请重新输入！'})
    else:
        form = PwdChangeForm()

    return render(request, 'project/pwd_change.html', {'form': form, 'user': user})
'''
展示对象列表（比如所有用户，所有文章）- ListView
展示某个对象的详细信息（比如用户资料，比如文章详情) - DetailView
通过表单创建某个对象（比如创建用户，新建文章）- CreateView
通过表单更新某个对象信息（比如修改密码，修改文字内容）- UpdateView
用户填写表单后转到某个完成页面 - FormView
删除某个对象 - DeleteView
'''
'''
class IndexView(ListView):

    model = Article

def index(request):
    queryset = Article.objects.all()
    return render(request, 'blog/article_list.html', {"object_list": queryset})

提取了需要显示的对象列表或数据集(queryset): Article.objects.all()
指定了用来显示对象列表的模板名称(template_name): 默认app_name/model_name_list.html
指定了内容对象名称(context_object_name):默认值object_list

通过重写queryset, template_name和context_object_name来完成ListView的自定义
1.通过更具体的get_object()方法来返回一个更具体的对象
2.通过重写get_queryset方法传递额外的参数或内容
3.通过重写get_context_data方法传递额外的参数或内容
'''

class CourseList(ListView):
    paginate_by = 5
    template_name = 'project/course_list.html'

    def get_queryset(self):
        return Course.objects.filter(opened=0).order_by("id")

@method_decorator(login_required, name='dispatch')
class CourseListSelf(ListView):
    paginate_by = 5
    template_name = 'project/course_list_self.html'

    def get_queryset(self):
        if self.request.user.role.role == 1:
            return Course.objects.filter(teacher=self.request.user.role.teacher).order_by("id")
        else:
            return Course.objects.filter(student=self.request.user.role.student).order_by("id")

"""
DetailView视图不能使用@login_required这个装饰器
DetailView用来展示一个具体对象的详细信息。它需要URL提供访问某个对象的具体参数（如pk, slug值）
默认的模板是app/model_name_detail.html
默认的内容对象名字context_object_name是model_name
如指定了queryset, 那么返回的object是queryset.get(pk = id), 而不是model.objects.get(pk = id)。
"""
class CourseDetail(DetailView):
    model = Course
    template_name = 'project/course_detail.html'

"""
CreateView默认的模板是model_name_form.html, 默认的context_object_name是form
<form method="post">{% csrf_token %}
    {{ form.as_p }}#将表单渲染成< p >标签
    <input type="submit" value="Save" />
</form>
通过重写template_name和form_class来完成CreateView的自定义
"""
@method_decorator(login_required, name='dispatch')
class CourseCreate(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'project/course_form.html'

    # 将创建对象的用户与model里的user结合
    def form_valid(self,form):
        form.instance.teacher = self.request.user.role.teacher
        return super().form_valid(form)

"""
UpdateView一般通过某个表单更新现有对象的信息，更新完成后会转到对象详细信息页面。它需要URL提供访问某个对象的具体参数（如pk, slug值）
UpdateView和CreateView很类似，比如默认模板都是model_name_form.html
1.CreateView显示的表单是空表单，UpdateView中的表单会显示现有对象的数据。
2.用户提交表单后，CreateView转向对象列表，UpdateView转向对象详细信息页面
"""
@method_decorator(login_required, name='dispatch')
class CourseUpdate(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'project/course_form.html'

    def get_object(self,queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj

    # def form_valid(self, form):
    #    form.do_sth()
    #    return super().form_valid(form)

"""
DeleteView一般用来删除某个具体对象。它要求用户点击确认后再删除一个对象。使用这个通用视图，需要定义模型的名称model和成功删除对象后的返回的URL。
默认模板是myapp/model_confirm_delete.html
"""
@method_decorator(login_required, name='dispatch')
class CourseDelete(DeleteView):
    model = Course
    get = DeleteView.post
    success_url = reverse_lazy('project:course_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj

@method_decorator(login_required, name='dispatch')
class HomeworkList(ListView):
    def get_queryset(self):
        return Homework.objects.filter(course__id=self.kwargs['pk']).filter(status='p').order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        homework = [x for x in self.get_queryset()]
        judge = [0 for i in range(len(homework))]
        handin = Handin.objects.filter(course__id=self.kwargs['pk']).filter(author=self.request.user.role.student)
        for handin in handin:
            if handin.homework in homework:
                judge[homework.index(handin.homework)] = 1

        # zip 函数将两个列表合并，返回一个 tuple
        info = list(zip(homework,judge))
        if Group.objects.filter(course=course,member=self.request.user.role.student):
            group = Group.objects.get(course=course,member=self.request.user.role.student).member.all()
        else:
            group = ''
        context.update({
            'course':course,
            'judge':judge,
            'info':info,
            'group':group,
        })
        return context

@method_decorator(login_required, name='dispatch')
class HomeworkListPublished(ListView):
    template_name = 'project/homework_list_published.html'
    paginate_by = 5

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.course.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj

    def get_queryset(self):
        return Homework.objects.filter(course__id=self.kwargs['pk']).filter(status='p').order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        context.update({
            'course':course,
        })
        return context

@method_decorator(login_required, name='dispatch')
class HomeworkListDraft(ListView):
    paginate_by = 5
    template_name = 'project/homework_list_publishing.html'

    # 用户只能看到自己的文章草稿。当用户查看别人的文章草稿时，返回http 404错误
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.course.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj

    def get_queryset(self):
        return Homework.objects.filter(course__id=self.kwargs['pk']).filter(status='d').order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        context.update({
            'course':course,
        })
        return context

class HomeworkDetail(DetailView):
    model = Homework
    template_name = 'project/homework_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.viewed()
        return obj

    # 覆写 get_context_data 的目的是因为除了将 homework 传递给模板外（DetailView 已经帮我们完成），
    # 还要把评论表单、homework 下的评论列表传递给模板。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pkr'])
        form = CommentForm()
        comment_list = self.object.comment.filter(homework=self.object)
        context.update({
            'course':course,
            'form': form,
            'comment_list': comment_list
        })
        return context

@method_decorator(login_required, name='dispatch')
class HomeworkCreate(CreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'project/homework_form.html'

    def form_valid(self, form):
        form.instance.course = Course.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class HomeworkUpdate(UpdateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'project/homework_form.html'

@method_decorator(login_required, name='dispatch')
class HomeworkDelete(DeleteView):
    model = Homework
    get = DeleteView.post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.course.teacher != self.request.user.role.teacher:
            raise Http404()
        return obj

    def get_success_url(self):
        return reverse_lazy('project:homework_list_published',args=[str(self.kwargs['pkr'])])
    # 不需要确认模板直接删除
    # def get(self,request,*args,**kwargs):
    #     return self.post(request,*args,**kwargs)

@login_required()
def homework_publish(request, pk,pkr):
    homework = get_object_or_404(Homework, pk=pk)
    homework.publish()
    return redirect(reverse('project:homework_detail', args=[str(pkr),str(pk)]))

@login_required()
def homework_search(request):
    pass

@login_required
def homework_comment(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    comment_list = homework.comment.filter(homework=homework)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            """
            commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            将评论和被评论的文章关联起来。
            """
            comment.homework = homework
            if request.user.role.role == 1:
                comment.username = request.user.role.teacher.name
            else:
                comment.username = request.user.role.student.name
            comment.save()
            """
            重定向到 homework 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            然后重定向到 get_absolute_url 方法返回的 URL。
            """
            return redirect(homework)
        else:
            """
            检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            因此传三个模板变量给 detail.html，
            一个是作业（Homework），一个是评论列表，一个是表单 form
            注意这里没有用到homework.comment_set.all() 方法：homework.comment_set.all() 反向查询全部评论。
            而用到了related_name的反向查询
            """
            context = {'homework': homework,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'homework/homework_detail.html', context=context)
    """
    不是 homework 请求，说明用户没有提交数据，重定向到文章详情页。
    """
    return redirect(homework)

def course_select(request,pk):
    course = get_object_or_404(Course,pk=pk)
    user = get_object_or_404(User,pk=request.user.id)
    course.student.add(user.role.student)
    return HttpResponseRedirect(reverse('project:course_list_self', args=[user.id]))

def course_cancel(request,pk):
    course = get_object_or_404(Course,pk=pk)
    user = get_object_or_404(User,pk=request.user.id)
    course.student.remove(user.role.student)
    return HttpResponseRedirect(reverse('project:course_list_self', args=[user.id]))

@method_decorator(login_required, name='dispatch')
class HomeworkHandin(ListView):
    model = Handin
    template_name = 'project/homework_handin_count.html'

    def get_queryset(self):
        return Handin.objects.filter(course__id=self.kwargs['pkr']).filter(homework__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homework = Homework.objects.get(id=self.kwargs['pk'])
        context.update({
            'homework':homework,
        })
        return context

@method_decorator(login_required, name='dispatch')
class HandinList(ListView):
    paginate_by = 5
    template_name = 'project/handin_list.html'

    def get_queryset(self):
        return Homework.objects.get(id=self.kwargs['pk']).handin.all()

@method_decorator(login_required, name='dispatch')
class HandinListDone(ListView):
    template_name = 'project/handin_list_done.html'
    paginate_by = 5

    def get_queryset(self):
        return Handin.objects.filter(course__id=self.kwargs['pk']).filter(author=self.request.user.role.student).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        if Group.objects.filter(course=course,member=self.request.user.role.student):
            group = Group.objects.get(course=course,member=self.request.user.role.student).member.all()
        else:
            group = ''
        context.update({
            'course':course,
            'group':group,
        })
        return context

@method_decorator(login_required, name='dispatch')
class HandinCreate(CreateView):
    model = Handin
    form_class = HandinForm
    template_name = 'project/handin_form.html'

    def form_valid(self, form):
        homework = Homework.objects.get(id=self.kwargs['pk'])
        course = Course.objects.get(id=self.kwargs['pkr'])
        if homework.group == 0:
            form.instance.course = course
            form.instance.homework = homework
            form.instance.author = self.request.user.role.student
            return super().form_valid(form)
        else:
            # 小组作业，一人提交则全部提交
            form.instance.course = course
            form.instance.homework = homework
            form.instance.author = self.request.user.role.student
            if Group.objects.filter(course=course,member=self.request.user.role.student):
                group = Group.objects.get(course=course,member=self.request.user.role.student).member.all()
                for each in group:
                    if each != self.request.user.role.student:
                        Handin.objects.get_or_create(course=course,homework=homework,author=each)
                return super().form_valid(form)
            else:
                form.instance.course = course
                form.instance.homework = homework
                form.instance.author = self.request.user.role.student
                return super().form_valid(form)

class HandinDetail(DetailView):
    model = Handin
    template_name = "project/handin_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homework = Homework.objects.get(id=self.kwargs['pkr'])
        context.update({
            'homework':homework,
        })
        return context

@method_decorator(login_required, name='dispatch')
class HandinUpdate(UpdateView):
    model = Handin
    form_class = HandinForm
    template_name = 'project/handin_form.html'

@method_decorator(login_required, name='dispatch')
class HandinDelete(DeleteView):
    model = Handin

    def get_success_url(self):
        return reverse_lazy('project:homework_list',args=[str(self.kwargs['pka'])])

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user.role.student:
            raise Http404()
        return obj

    def get(self,request,*args,**kwargs):
        return self.post(request,*args,**kwargs)

@method_decorator(login_required, name='dispatch')
class GroupList(ListView):
    paginate_by = 5
    template_name = 'project/group.html'

    def get_queryset(self):
        return Group.objects.filter(course__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        group = [x for x in self.get_queryset()]
        group_list = []
        for each in group:
            group_list.append(each.member.all())
        info = list(zip(group,group_list))
        context.update({
            'course':course,
            'info':info,
        })
        return context

@method_decorator(login_required, name='dispatch')
class GroupCreate(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'project/group_form.html'

    def form_valid(self, form):
        form.instance.course = Course.objects.get(id=self.kwargs['pk'])
        form.instance.leader = self.request.user.role.teacher
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        context.update({
            'course':course,
        })
        return context

def course_group_create(request,pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'GET':
        course_students = course.student.all()
        groups = Group.objects.filter(course=course)
        members = []
        for group in groups:
            for member in group.member.all():
                members.append(member)
        students = [x for x in course_students if x not in members]
        print(students)
        return render(request,'project/group_course_form.html',{'students':students,'course':course})
    elif request.method == 'POST':
        students = request.POST.getlist('students')
        new_group = Group.objects.create(leader=course.teacher,course=course)
        for student in students:
            new_group.member.add(Student.objects.get(id=student))

        group = [x for x in Group.objects.filter(course=course)]
        group_list = []
        for each in group:
            group_list.append(each.member.all())
        info = list(zip(group,group_list))
        context = {
            'course':course,
            'info':info,
        }
        return render(request,'project/group.html',context=context)

@method_decorator(login_required, name='dispatch')
class GroupDelete(DeleteView):
    model = Group
    get = DeleteView.post
    def get_success_url(self):
        return reverse_lazy('project:group_list',args=[str(self.kwargs['pkr'])])

def course_student(request,pk):
    course = Course.objects.get(pk=pk)
    student = course.student.all()
    return render(request,'project/course_student.html',context={'student':student,'course':course})

