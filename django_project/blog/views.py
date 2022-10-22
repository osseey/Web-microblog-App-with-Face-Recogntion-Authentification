import os
from django.urls import path, include
import face_recognition
import cv2 
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from users.forms import LoginForm
import users
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
import os
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.http import HttpResponse
from pathlib import Path
import os
from PIL import Image
from django.contrib.auth.models import User

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# initialize the camera
def facedect(loc):
        cam = cv2.VideoCapture(0)   # 0 -> index of camera
        s, img = cam.read()
        if s:    # frame captured without any errors
                cv2.namedWindow("cam-test")
                cv2.imshow("cam-test",img)
                #cv2.waitKey(0)
                cv2.destroyWindow("cam-test")
                cv2.imwrite("filename.jpg",img)

                #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                #MEDIA_ROOT =os.path.join(BASE_DIR,'pages')

                print(MEDIA_ROOT,loc)
                loc=(str(MEDIA_ROOT)+loc)
                print(loc)
                #print("/home/light/codes/web/djangoproject/mysite/pages/media/profil_images/IMG_20180330_1600482-01.jpg")
                face_1_image = face_recognition.load_image_file(loc)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

                #

                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
                top,right, bottom, left= (face_recognition.face_locations(img))[0]
                face_image=img[top:bottom,left:right]
                pil_image= Image.fromarray(face_image)
                pil_image.save("face.jpg")
                
                print(check)
                if check[0]:
                        return True

                else :
                        return False 

#Create your views here






@login_required
def login2(request):
        
	return render(request,'users/login2.html', {'title': 'Face Recognition'})


@login_required
def home(request):
        context={
		'posts':Post.objects.all()
        }
                 
        return render(request,'blog/home.html',context)


class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by= 5
    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        name= str(post.author)
        if facedect('/profile_pics/'+name+'.jpg'):
        #if self.request.user == post.author:
            return True

        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/home/'

    def test_func(self):
        post = self.get_object()
        name= str(post.author)
        if facedect('/profile_pics/'+name+'.jpg'):
        #if self.request.user == post.author or self.request.user == "Josepha_3" :
            return True
        else:
                if facedect('/profile_pics/Josepha_3.jpg'):
                        return True
        return False


def base2(request):
	return render(request,'blog/base2.html', {'title': 'Welcome'})

def about(request):
	return render(request,'blog/about.html', {'title': 'About'})
