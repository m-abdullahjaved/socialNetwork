import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models.Profile import Profile
from ..models.Post import Post
from ..models.Comment import Comment
from ..models.Like_Post import LikePost
from ..models.FollowersCount import FollowersCount
from itertools import chain


# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    data = {}
    data['user_profile'] = user_profile
    data['post'] = Post.get_all_Posts()

    user_following_list = [] # users you are following
    feed = [] # posts of users you are following

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list: # [ 'Abdullah', 'Khadija', 'Ameer']
        feed_list = Post.objects.filter(user=usernames) # all posts of Abdullah,
        feed.append(feed_list) # append all posts of user

    feeds = list(chain(*feed))

    # User suggestions starts here

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_list = [x for x in list(suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_list)


    username_profile = []
    username_profile_list = []

    for users in final_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)

    suggestion_username_profile_list = list(chain(*username_profile_list))

    data['suggestion'] = suggestion_username_profile_list[:4]

    comments_by_post = {}
    for post in data['post']:
        comments = Comment.get_comments_by_Post(post.id)
        comments_by_post[str(post.id)] = comments
        #print(comments)

    data['posts'] = feeds
    data['comments_by_post'] = comments_by_post
    print(data['comments_by_post'])
    return render(request, 'index.html', data)


@login_required(login_url='signin')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            image = user_profile.image
        else:
            image = request.FILES.get('image')

        Bio = request.POST['Bio']
        Location = request.POST['Loc']

        user_profile.image = image
        user_profile.bio = Bio
        user_profile.location = Location
        user_profile.save()
        messages.info(request, "Profile Updated Successfully")
    data = {}
    data['user_profile'] = user_profile
    return render(request, 'setting.html', data)

def signin(request):
    if request.method == 'POST':
        user = request.POST['name']
        password = request.POST['pass']

        user = auth.authenticate(username=user, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')


    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        password2 = request.POST['pass2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                messages.info(request, 'User Created Successfully')
                return redirect('signin')

        else:
            messages.info(request, "Password didn't Match")
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def add_comment(request):
    if request.method == 'POST':
        pid = request.POST['p_id']
        comment = request.POST['Comment']
        author = Profile.objects.get(user=request.user)

        new_comment = Comment.objects.create(PostId = Post(pid), Author = author, Content = comment)
        new_comment.save()

    return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk
    button = ""

    if FollowersCount.objects.filter(follower= follower, user=user).first():
        button = 'Unfollow'
    else:
        button = 'Follow'

    followers = len(FollowersCount.objects.filter(user=pk))
    following = FollowersCount.count_following(pk)
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button': button,
        'follower': followers,
        'following': following
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        user = request.POST['user']
        follower = request.POST['follower']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            follower = FollowersCount.objects.get(follower=follower, user=user)
            follower.delete()
        else:
            follower = FollowersCount.objects.create(follower=follower, user=user)
            follower.save()

        return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url="signin")
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption = caption)
        new_post.save()

    return redirect('/')


@login_required(login_url="signin")
def likepost(request):
    p_id = request.GET.get('p_id')
    username = request.user.username

    post = Post.objects.get(id=p_id)

    like_filter = LikePost.objects.filter(post_id=p_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=p_id, username=username)
        new_like.save()
        post.likes = post.likes + 1
        post.save()

    else:
        like_filter.delete()
        post.likes = post.likes - 1
        post.save()

    return redirect('/')

