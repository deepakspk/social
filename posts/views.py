from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.views.generic import (View, ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView)

# pip install django-braces

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class ThanksMsg(TemplateView):
    template_name = 'thanksformsg.html'

class PostListView(generic.ListView):
    template_name = 'index.html'
    model = models.Post
    select_related = ("user", "group")
    context_object_name = 'post_list'

    def get_queryset(self):
        return models.Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView,self).get_context_data(*args,**kwargs)
        context['posts'] = models.Post.objects.all()
        context['groups'] = models.Group.objects.all()
        return context

class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetailView(generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'posts/post_detail.html'
    form_class = forms.PostForm
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)


#######################################
## Functions that require a pk match ##
#######################################

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('posts:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('posts:post_detail', pk=post_pk)
