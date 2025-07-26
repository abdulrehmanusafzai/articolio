from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Contact
from blog.models import Post

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')
    
def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        content = request.POST["content"]
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 8:
            messages.error(request, "Please fill the form correcctly.")
        else:
            contact = Contact(name = name, email = email, phone = phone, content = content)
            contact.save()
            messages.success(request, "Your feedback was received.")
    return render(request, 'home/contact.html')
    
def search(request):
    query = request.GET.get("query")
    if len(query) > 80:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains = query)
        allPostscontent = Post.objects.filter(content__icontains = query)
        allPosts = allPostsTitle.union(allPostscontent)
    if allPosts.count() == 0:
        messages.warning(request, "Try diffetent key words.")
    context = {"allPosts": allPosts, "query": query}
    return render(request, 'home/search.html', context)

def handleSignup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if len(username) > 10:
            messages.error(request, "Username must be smaller than 10 characters")
            return redirect("home")

        if not username.isalnum():
            messages.error(request, "Username must be only alphanumeric")
            return redirect("home")

        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your account has been created")
            return redirect("home")
    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == "POST":
        loginUsername = request.POST["loginUsername"]
        loginPassword = request.POST["loginPassword"]

        user = authenticate(username = loginUsername, password = loginPassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Logging in complete")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("home")
    else: 
        return HttpResponse("404 - Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Logging out complete")
    return redirect("home")
