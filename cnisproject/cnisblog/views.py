from django.shortcuts import render


posts = [
    {
        'author': 'Rastine Pinlac',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Shenn Tinsay',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'August 28, 2018'
    },
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'cnisblog/home.html', context)


def about(request):
    return render(request, 'cnisblog/about.html', {'title': 'About'})


def signup(request):
    return render(request, 'cnisblog/signup.html')
