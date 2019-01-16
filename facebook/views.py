from django.shortcuts import render, redirect
from facebook.models import Article, Comment

# Create your views here.

count = 0

def play2 (request):
    name = '이진문'
    global count
    count = count + 1

    age = 18

    if age < 19:
        status = '미성년자'
    else:
        status = '성인'

    diary = ['11월 22일', '11월 23일', '11월 24일']

    return render(request, 'play2.html',
                  {'name': name, 'count': count,
                   'status': status, 'diary': diary})

def profile(request):
    return render(request, 'profile.html')

def newsfeed(request):
    articles = Article.objects.all().order_by('-created_at')

    for article in articles:
        article.length = len(article.text)

    return render(request, 'newsfeed.html',{'articles' : articles})


def detail_feed(request, pk):
    article = Article.objects.get(pk = pk)
    if request.method == 'POST':
        Comment.objects.create(
            article = article,
            author = request.POST['nickname'],
            text = request.POST['reply'],
            password = request.POST['password']
        )
        return redirect(f'/feed/{article.pk}')

    return render(request, 'detail_feed.html',{'article':article})


def new_feed(request):
    if request.method == 'POST':
        if request.POST['author'] != '' and request.POST['title'] != '' and request.POST['content'] != '' and request.POST['password'] != '':

            plus_text = request.POST['content']

            new_article = Article.objects.create(
                    author=request.POST['author'],
                    title=request.POST['title'],
                    text=plus_text,
                    password=request.POST['password']
            )
        else:
            return render(request, 'fail_page.html', {'fmsg': "모두 채워주세요"})

        return redirect(f'/feed/{ new_article.pk }/')

    return render(request, 'new_feed.html')

def remove_feed(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        if article.password == request.POST['password']:
            article.delete()
            return redirect(f'/')
        else:
            return render(request,"fail.html",{ 'fmsg' : "비밀번호가 틀렸습니다"})

    return render(request, "remove_feed.html", { 'article' : article })

def edit_feed(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        if article.password == request.POST['password']:

            article.author = request.POST['author']
            article.title = request.POST['title']
            article.text = request.POST['content']
            article.save()
        else:
            return render(request,"fail.html",{ 'fmsg' : "비밀번호가 틀렸습니다"})


    return render(request, "edit_feed.html", { 'article' : article })


def fail(request):
    return render(request,'fail.html')