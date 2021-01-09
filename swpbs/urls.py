"""swpbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clientegy.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('home/',index,name='home'),
    path('freelancer_registration/',freelancer_registration,name='freelancer_registration'),
    path('client_registration/',client_registration,name='client_registration'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('client_post_project/',post_project,name='client_post_project'),
    path('client_posted_projects/',posted_project,name='client_posted_projects'),
    path('viewproject_client/<int:project_id>/',project_view_client,name='viewproject_client'),
    path('delete_project/<int:project_id>/',project_delete,name='delete_project'),
    path('view_all_projects_dev/',dev_posted_projects,name='view_all_projects_dev'),
    path('view_project_dev/<int:project_id>/',project_view_dev, name= "view_project_dev"),
    path('applied_projects/',applied_projects,name='applied_projects'),
    path('self_profile_dev/',self_dev_profile,name='self_profile_dev'),
    path('edit_profile_dev/',edit_profile_dev,name='edit_profile_dev'),
    path('self_profile_client/', self_client_profile,name='self_profile_client'),
    path('edit_profile_client/',edit_profile_client,name='edit_profile_client'),
    path('selected_freelancer_client/<int:psid>/',confirmation,name='selected_freelancer_client'),
    path('bill_final/<int:psid>/',bill_final,name='bill_final'),
    path('client_finalized_projects/',finalized_project,name='client_finalized_projects'),
    path('dev_selected_projects/',selected_project_dev,name='dev_selected_projects'),
    path('view_dev_profile/<int:dev_id>/',view_dev_profile,name='view_dev_profile'),
    path('viewdev_profile/<int:dev_id>/',viewdev_profile),
    path('view_client_profile/<int:client_id>/',view_client_profile,name='view_client_profile'),
    path('view_bill/<int:final_bid_id>/',view_bill,name= 'view_bill'),
    path('view_bill_dev/<int:final_bid_id>/',view_bill_dev,name= 'view_bill_dev'),
    path('mark_as_completed/<int:final_bid_id>/',project_mark_completed,name='mark_as_completed'),
    path('review/<int:final_bid_id>/',review,name='review'),
    path('feedback/<int:final_bid_id>/',feedback,name='feedback'),




]
