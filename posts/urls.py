from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    path("new/", views.CreatePostView.as_view(), name="create"),
    path("by/<username>/",views.UserPosts.as_view(),name="for_user"),
    path("by/<username>/<int:pk>/",views.PostDetailView.as_view(),name="post_detail"),
    path("delete/<int:pk>/",views.PostDeleteView.as_view(),name="delete"),
    path('by/<username>/<int:pk>/comment',views.add_comment_to_post,name='add_comment_to_post'),
    path('comment/<int:pk>/approve',views.comment_approve,name='comment_approve'),
    path('comment/<int:pk>/remove',views.comment_remove,name='comment_remove'),
]
