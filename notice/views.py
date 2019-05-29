from django.shortcuts import render
from django.views.generic import DetailView,ListView
from .models import Notice
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

class NoticeList(ListView):
    paginate_by = 2
    def get_queryset(self):
        return Notice.objects.all().order_by("-created")

class NoticeDetail(DetailView):
    model = Notice

def notice_search(request):
    q = request.GET.get('q', None)
    if q:
        notice_list = Notice.objects.filter(Q(title__icontains=q) |
                                                Q(body__icontains=q))
        context = {'notice_list': notice_list,'number':len(notice_list),'q':q}
        return render(request, 'notice/notice_search.html', context)

    return render(request, 'notice/notice_search.html',)
