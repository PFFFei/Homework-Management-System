from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify
from datetime import datetime
import uuid
import os
from ckeditor_uploader.fields import RichTextUploadingField

'''
    自定义上传文件的存储路径
'''
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    sub_folder = 'file'
    if ext.lower() in ["jpg", "png", "gif"]:
        sub_folder = "avatar"
    if ext.lower() in ["pdf", "docx","xlsx"]:
        sub_folder = "document"
    return os.path.join(str(instance.course.teacher.id), sub_folder, filename)

class Role(models.Model):
    ROLE_CHOICES = (
        (0,'学生'),
        (1,'教师')
    )
    user = models.OneToOneField(User,related_name='role',on_delete=models.CASCADE)
    role = models.SmallIntegerField(choices=ROLE_CHOICES,default=0,verbose_name='角色')

    def __str__(self):
    	return str(self.role)

'''
    定义一个抽象类，字段为各个表的公共字段，这个类并不会在数据库中建表
'''
class UserAbstractModel(models.Model):
    GENDER_CHOICES = (
        (0,'男'),
        (1,'女')
    )
    name = models.CharField('姓名',default='', max_length=50)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES,default=0,verbose_name='性别')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('最后更改时间', auto_now=True)
    description = models.TextField('个人描述',null=True)
    photo = models.ImageField('用户头像',upload_to=user_directory_path,blank=True)

    class Meta:
        abstract = True

class Teacher(UserAbstractModel):
    user = models.OneToOneField(Role,related_name='teacher',on_delete=models.CASCADE)
    ranks = models.CharField(default='无', max_length=50,verbose_name='职称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='教师表'
        verbose_name_plural = verbose_name

class Student(UserAbstractModel):
    user = models.OneToOneField(Role,related_name='student',on_delete=models.CASCADE)
    classes = models.CharField('班级',default='', max_length=50)

    def __str__(self):
        return self.user.user.username

    def get_course_count(self):
    	return Course.objects.filter(student__id=self.id).count()

    class Meta:
        verbose_name='学生表'
        verbose_name_plural = verbose_name

class Course(models.Model):
    OPENED_CHOICES = (
        (0,'公开'),
        (1,'不公开')
    )
    cname = models.CharField(verbose_name='课程名称', max_length=50,null=False)
    classes =  models.CharField(verbose_name='班级',default='', max_length=50)
    description = models.TextField(verbose_name='课程描述',)
    opened = models.SmallIntegerField('公开状态',choices=OPENED_CHOICES,default=0)
    teacher = models.ForeignKey(Teacher,related_name="course",on_delete=models.CASCADE)
    student = models.ManyToManyField(Student,blank=True)
    
    def __str__(self):
        return self.cname

    def get_absolute_url(self):
        return reverse('project:course_detail', args=[str(self.pk)])

    # @property把homework_count伪装成属性
    @property
    def homework_count(self):
        return Homework.objects.filter(homework_id=self.id).count()

    class Meta:
        verbose_name='课程'
        verbose_name_plural = verbose_name

class WorkAbstractModel(models.Model):
    body = RichTextUploadingField('正文')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    file = models.FileField('文件',upload_to=user_directory_path,blank=True)

    class Meta:
        abstract = True

class Homework(WorkAbstractModel):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    GROUP_CHOICES = (
        (0,'个人'),
        (1,'小组')
    )
    title = models.CharField('标题', max_length=200)# unique=True
    slug = models.SlugField('摘要', max_length=60, blank=True)
    published = models.DateTimeField('发布时间', null=True)
    status = models.CharField('作业状态', max_length=1, choices=STATUS_CHOICES, default='p')
    group = models.SmallIntegerField('组队状态',choices=GROUP_CHOICES,default=0)
    views = models.PositiveIntegerField('浏览量', default=0)
    course = models.ForeignKey(Course,related_name="homework",on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    # 快速获取文件格式
    def get_format(self):
        return self.file.url.split('.')[-1].upper()

    # 利用unidecode对中文解码，利用slugify方法根据标题手动生成slug
    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    # Django的 CreateView 和 UpdateView 在完成对象的创建或编辑后会自动跳转到这个绝对url
    def get_absolute_url(self):
        return reverse('project:homework_detail', args=[str(self.course.id),str(self.pk)])

    def clean(self):
        if self.status == 'd' and self.published is not None:
            self.published = None
            # raise ValidationError('草稿没有发布日期. 发布日期已清空。')
        if self.status == 'p' and self.published is None:
            self.published = datetime.now()

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def publish(self):
        self.status = 'p'
        self.published = datetime.now()
        self.save(update_fields=['status', 'published'])

    class Meta:
        ordering = ['-modified']
        verbose_name = "作业"
        verbose_name_plural = verbose_name

class Handin(WorkAbstractModel):
    author = models.ForeignKey(Student,related_name="handin",on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name="handin",on_delete=models.CASCADE)
    homework =  models.ForeignKey(Homework,related_name="handin",on_delete=models.CASCADE)
    score = models.IntegerField('分数',null=True)

    def __str__(self):
        return self.author.name

    def get_format(self):
        return self.file.url.split('.')[-1].upper()

    def get_absolute_url(self):
        return reverse('project:handin_detail', args=[str(self.homework.course.id),str(self.homework.pk),str(self.pk)])

    class Meta:
        verbose_name = "作答"
        verbose_name_plural = verbose_name

class Comment(models.Model):
    homework = models.ForeignKey(Homework,related_name="comment",on_delete=models.CASCADE)
    text = models.TextField('评论内容')
    created = models.DateTimeField('评论时间',auto_now_add=True)
    username = models.CharField('用户名称',max_length=50)

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

class Group(models.Model):
    EDIT_CHOICES = (
        (0,'不可编辑'),
        (1,'可编辑')
    )
    leader = models.ForeignKey(Teacher,related_name="leader",on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name="group",on_delete=models.CASCADE)
    member = models.ManyToManyField(Student,blank=True)
    edit = models.SmallIntegerField(choices=EDIT_CHOICES,default=1,verbose_name='编辑状态')

    def __str__(self):
        return self.leader.name

    def get_absolute_url(self):
        return reverse('project:group_list', args=[str(self.course.id)])

    class Meta:
        verbose_name = "组队"
        verbose_name_plural = verbose_name
