from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView


from .forms import AddPostForm
from .models import *

menu = [{'title': 'About site', 'url_name': 'about'},
        {'title': 'Add page', 'url_name': 'add_page'},
        {'title': 'Feedback', 'url_name': 'contact'},
        {'title': 'Log in', 'url_name': 'login'}]


class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Main page'
        context['cat_selected'] = 0
        return context

    def queryset(self):
        return Women.objects.filter(is_published=True)

# def index(request):
#     posts = Women.objects.all()
#
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Main page',
#                'cat_selected': 0,
#                }
#     return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'About page'})

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Page'
        context['menu'] = menu
        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     context = {'form': form,
#                'menu': menu,
#                'title': 'Add an article'
#                }
#
#     return render(request, 'women/addpage.html', context=context)


def contact(request):
    return HttpResponse('Feedback')


def login(request):
    return HttpResponse('Login')


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Page Not Found</h1>')

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id
#     }
#
#     return render(request, 'women/post.html', context=context)

class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context
class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Category - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)
#
#     dict = {'title': 'Отображение по рубрикам',
#             'posts': posts,
#             'menu': menu,
#             'cat_selected': cat_slug
#             }
#
#     return render(request, 'women/index.html', context=dict)
