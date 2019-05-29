# Generated by Django 2.0.5 on 2019-04-15 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_handin_course'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': '课程', 'verbose_name_plural': '课程'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': '组队', 'verbose_name_plural': '组队'},
        ),
        migrations.AlterModelOptions(
            name='handin',
            options={'verbose_name': '作答', 'verbose_name_plural': '作答'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': '学生表', 'verbose_name_plural': '学生表'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': '教师表', 'verbose_name_plural': '教师表'},
        ),
    ]
