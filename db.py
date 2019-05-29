#!/usr/bin/env python
#coding:utf-8
 
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homework.settings")
 
import django
if django.VERSION >= (1, 7):				#自动判断版本
    django.setup()


# import xlrd
# filename = "user.xlsx"
# workbook = xlrd.open_workbook(filename)
# print(workbook.sheet_names())          	#查看所有sheet
# booksheet = workbook.sheet_by_index(0)  	#用索引取第一个sheet或sheet_by_name('Sheet 1')
# cell_1 = booksheet.cell_value(0,0)     	#读单元格数据
# cell_2 = booksheet.cell_value(1,3)
# row = booksheet.row_values(1)


def main():
	from django.contrib.auth.models import User
	from project.models import Role,Student,Teacher
	import xlrd
	filename = "user.xlsx"
	workbook = xlrd.open_workbook(filename)
	booksheet = workbook.sheet_by_index(0) 
	for i in range(7):
		row = booksheet.row_values(i+1)
		role = int(row[4])
		if role:
			user = User.objects.create_user(username=row[0], password=row[1])
			role = Role(role=int(role),user=user)
			role.save()
			teacher = Teacher(user=role)
			teacher.name = row[2]
			teacher.gender = int(row[3])
			teacher.save()
		else:
			
			user = User.objects.create_user(username=row[0], password=row[1])
			role = Role(role=int(role),user=user)
			role.save()
			student = Student(user=role)
			student.name = row[2]
			student.gender = int(row[3])
			student.save()

if __name__ == '__main__':
	main()
	print("Done!")