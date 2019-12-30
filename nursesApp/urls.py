from django.urls import path, re_path, reverse
from . import views
from django.contrib import admin

app_name = 'nursesApp'

urlpatterns = [
path('',views.NurseshomeView.as_view(),name='nurses'),
path('contributors/',views.ContributorView.as_view(),name='contributors'),
path('members/',views.MemberView.as_view(),name='members'),
path('winners/',views.WinnerView.as_view(),name='winners'),
path('contactus/',views.MsgView.as_view(),name='contactus'),
path('create_member/',views.CreatememberView.as_view(),name='create_member'),
path('members/<int:pk>/',views.MemberDetailView.as_view(),name='memberDetail'),
path('members/update/<int:pk>/',views.MemberUpdateView.as_view(),name='memberUpdate'),
path('members/delete/<int:pk>/',views.MemberDeleteView.as_view(),name='memberDelete'),
path('upload',views.member_upload,name='upload'),
path('contact/', views.contact, name='contact'),
path('success/', views.success, name='success'),
]
