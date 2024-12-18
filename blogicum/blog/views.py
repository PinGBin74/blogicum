from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from django.utils import timezone


def post_query():
    """Вернуть результат запроса
    к таблице blog_post.
    """
    date_now = timezone.now()
    query_set = (
        Post.objects.select_related(
            "category",
            "location",
            "author",
        )
        .only(
            "title",
            "text",
            "pub_date",
            "author__username",
            "category__title",
            "category__slug",
            "location__name",
        )
        .filter(
            pub_date__lte=date_now,
            is_published=True,
            category__is_published=True,
        )
    )
    return query_set


def category_query():
    """Вернуть результат запроса
    к таблице blog_category.
    """
    query_set = Category.objects.values("title", "description").filter(
        is_published=True
    )
    return query_set


def index(request):
    """Выводит записи на главную."""
    template = "blog/index.html"
    post_list = post_query().order_by("-pub_date")[:5]
    context = {"post_list": post_list}
    return render(request, template, context)


def post_detail(request, id):
    """Выводит отдельную страницу поста."""
    template = "blog/detail.html"
    post = get_object_or_404(
        post_query(),
        pk=id,
    )
    context = {"post": post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """Выводит страницу категории."""
    template = "blog/category.html"
    category = get_object_or_404(
        category_query(),
        slug=category_slug,
    )
    post_list = (
        post_query().filter(category__slug=category_slug)
        .order_by("-pub_date")
        [:10]
    )
    context = {"category": category, "post_list": post_list}
    return render(request, template, context)
