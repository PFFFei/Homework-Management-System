from django import forms 
from django.contrib.auth.models import User 
from django.forms import ModelForm
from .models import Teacher,Student,Course,Homework,Handin,Comment,Group
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class RegistrationForm(forms.Form):
    username = forms.CharField(label=' 用户名',max_length=50)
    password1 = forms.CharField(label=' 密 码 ',widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)
    role = forms.ChoiceField(label='角色',choices=((0,'学生'),(1,'教师')))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 6:
            raise forms.validationError("用户名必须至少为6个字符！")
        elif len(username) > 50:
            raise forms.ValidationError("用户名太长！")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("用户名已存在！")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码太短！")
        elif len(password1) > 20:
            raise forms.ValidationError("密码太长！")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配，请重新输入！")

        return password2

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        filter_result =  User.objects.filter(username__exact=username)
        if not filter_result:
            raise forms.ValidationError("用户名不存在！")
        return username

class ProfileForm(forms.Form):
    name = forms.CharField(label='姓名', max_length=50, required=False)
    gender = forms.ChoiceField(label='性别',widget = forms.Select(),choices = ([('0','男'), ('1','女'), ]),required=False)

class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label=' 原 密 码 ', widget=forms.PasswordInput)
    password1 = forms.CharField(label=' 新 密 码 ', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码太短！")
        elif len(password1) > 20:
            raise forms.validationError("密码太长！")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配，请重新输入！")
        return password2

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        # 选择指定字段的所有数据 field
        fields = ['cname','classes','description','opened']
        # boostrap表单需要 form-control 这个样式
        widgets = {
            'cname': forms.TextInput(attrs={'class': 'form-control'}),
            'classes': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':'3'}),
            'opened': forms.Select(attrs={'class': 'form-control'}),
        }

class HomeworkForm(ModelForm):

    class Meta:
        model = Homework
        # 剔除指定字段的所有数据 exclude
        exclude = ['author', 'views', 'slug','published','course']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': CKEditorUploadingWidget(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '作业标题',
            'body': '作业内容',
            'status': '作业状态',
            'group': '组队状态',
            'file': '上传文件',
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ["","jpg","png","pdf", "xlsx","docx","zip","doc"]:
                raise forms.ValidationError("Only zip jpg, png, pdf, doc, docx, and xlsx files are allowed.")
            return file

class HandinForm(ModelForm):

    class Meta:
        model = Handin
        exclude = ['author','homework','course','score']
        widgets = {
            'body': CKEditorUploadingWidget(attrs={'class': 'form-control'}),
            # 'file': forms.FileInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ["","jpg","png", "pdf", "xlsx","docx","zip","doc"]:
                raise forms.ValidationError("Only zip jpg, png, pdf, doc, docx, and xlsx files are allowed")
            return file

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control','rows':'3'}),
        }
        labels = {
            'text':'评论内容',
        }

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['member']
        widgets = {
            'member':forms.CheckboxSelectMultiple(attrs={'class': 'multi-checkbox'}),
        }
        labels = {
            'member': '学生列表',
        }

