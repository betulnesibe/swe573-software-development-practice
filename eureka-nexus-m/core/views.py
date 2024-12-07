from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileCreationForm, ProfileChangeForm, PostForm, WikidataTagFormSet
from django.contrib import messages
from .models import Profile, Post
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import requests
from .models import WikidataTag
from django.views.generic import DetailView

def home(request):
    recent_posts = Post.objects.all().order_by('-created_at')[:6]  # Get 6 most recent posts
    return render(request, 'core/home.html', {'recent_posts': recent_posts})

# AUTH

def signup_view(request):
    if request.method == 'POST':
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('profile')
    else:
        form = ProfileCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {"user": request.user})

from django.contrib.auth import update_session_auth_hash

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()  # Save the updated profile and password
            messages.success(request, 'Profile updated successfully!')
            # Keep the user logged in after updating the password
            if form.cleaned_data.get('new_password'):
                update_session_auth_hash(request, user)
            return redirect('profile')  # Redirect to the profile page
    else:
        form = ProfileChangeForm(instance=request.user)

    return render(request, 'core/edit_profile.html', {'form': form})




# POSTS


def post_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 10)  # Show 10 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'core/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print("Semantic tags:", list(post.wikidata_tags.all()))
    return render(request, 'core/post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        # Add these debug prints
        print("POST data:", request.POST)
        print("FILES:", request.FILES)
        
        form = PostForm(request.POST, request.FILES)
        formset = WikidataTagFormSet(request.POST, instance=Post())
        
        print("Formset initial data:", formset.initial_forms)
        print("Formset is bound:", formset.is_bound)
        
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user if not request.POST.get('anonymous') else None
            post.save()
            
            print("Post saved with ID:", post.id)
            print("Formset cleaned data:", formset.cleaned_data)
            
            formset.instance = post
            try:
                formset.save()
                print("Formset saved successfully")
                # Verify the tags were saved
                saved_tags = list(post.wikidata_tags.all())
                print("Saved tags:", saved_tags)
                for tag in saved_tags:
                    print(f"Tag details - Type: {tag.tag_type}, ID: {tag.wikidata_id}, Label: {tag.label}")
            except Exception as e:
                print("Error saving formset:", str(e))
                print("Formset errors:", formset.errors)
            
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = PostForm()
        formset = WikidataTagFormSet(instance=Post())
    
    context = {
        'form': form,
        'formset': formset,
        'colour_choices': [list(choice) for choice in Post.COLOUR_CHOICES],
        'shape_choices': [list(choice) for choice in Post.SHAPE_CHOICES],
        'condition_choices': [list(choice) for choice in Post.CONDITION_CHOICES],
        'tag_types': WikidataTag.TAG_TYPES,
    }
    
    return render(request, 'core/create_post.html', context)

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        formset = WikidataTagFormSet(request.POST, instance=post)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
        formset = WikidataTagFormSet(instance=post)
    return render(request, 'core/edit_post.html', {'form': form, 'formset': formset, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post_list')
    return render(request, 'core/delete_post.html', {'post': post})

@login_required
def update_post_status(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You do not have permission to update this post status.')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Post.STATUS_CHOICES):
            post.status = new_status
            post.save()
            messages.success(request, 'Post status updated successfully!')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('post_detail', pk=pk)




def post_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 10)  # Show 10 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'core/post_list.html', {'posts': posts})


def wikidata_search(request):
    query = request.GET.get('q', '')
    if query:
        url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={query}&language=en&format=json&limit=5"
        response = requests.get(url)
        data = response.json()
        results = data.get('search', [])
    else:
        results = []
    return JsonResponse({'results': results})

class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure semantic tags are prefetched
        context['post'].semantic_tags.all()
        return context
