from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('login', views.log_in, name='login'),
    path('question/<int:question_id>', views.question, name='question'),
    path('logout', views.log_out, name='logout'),
    path('signup', views.signup, name='signup'),
    path('ask', views.ask, name='ask'),
    path('admin/', admin.site.urls),
    path('profile/<int:profile_id>', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('my_answers', views.my_answers, name='my_answers'),
    path('my_questions', views.my_questions, name='my_questions'),
    path('follows', views.follows, name='follows'),
]
