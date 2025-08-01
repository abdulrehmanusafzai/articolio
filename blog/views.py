from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from blog.templatetags import extras
from .models import Post, BlogComment


# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {"allPosts": allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug = slug).first()
    comments = BlogComment.objects.filter(post = post, parent = None)
    replies = BlogComment.objects.filter(post = post).exclude(parent = None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {"post": post, "comments": comments, "user": request.user, "replyDict": replyDict}
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        parentSno = request.POST.get("parentSno")
        post = Post.objects.get(sno = postSno)
        if parentSno == "":
            comment = BlogComment(comment = comment, user = user, post = post)
            messages.success(request, "Comment Posted")
        else:
            parent = BlogComment.objects.get(sno = parentSno)
            comment = BlogComment(comment = comment, user = user, post = post, parent = parent)
            messages.success(request, "Reply Posted")
        comment.save()
    return redirect(f'/blog/{post.slug}')
