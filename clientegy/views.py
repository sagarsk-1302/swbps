from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from clientegy.models import *
from django.urls import reverse
# Create your views here.
def index(request):
    return render(request,'index.html')

def freelancer_registration(request):
    registered = False
    username_exists = False
    email_exists = False
    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        ph_no = request.POST['phoneNo']
        password = request.POST['password']
        experience = request.POST['experience']
        domain = request.POST['service']
        charging_basis = request.POST['cost']
        try:
            User.objects.get(email = email)
            email_exists = True
        except User.DoesNotExist:
            try:
                User.objects.get(username = username)
                username_exists = True
            except User.DoesNotExist:
                user = User.objects.create(username= username,email=email)
                user.set_password(password)
                user.save()
                Developer.objects.create(user=user,age=age,exp=experience,domain=domain,charging_basis=charging_basis,phone_no=ph_no)
                registered = True
            finally:
                return render(request,'freelancer_registration.html',{'registered':registered,"username_exists":username_exists,
                                                                        "email_exists":email_exists})
        finally:
            return render(request,'freelancer_registration.html',{'registered':registered,"username_exists":username_exists,
                                                                        "email_exists":email_exists})
    else:
        return render(request,'freelancer_registration.html',{'registered':registered,"username_exists":username_exists,
                                                                        "email_exists":email_exists})

def client_registration(request):
    registered = False
    username_exists = False
    email_exists = False
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        ph_no = request.POST['phoneNo']
        password = request.POST['password']
        try:
            User.objects.get(email = email)
            email_exists = True
        except User.DoesNotExist:
            try:
                User.objects.get(username = username)
                username_exists = True
            except User.DoesNotExist:
                user = User.objects.create_user(username= username,email=email,password=password)
                user.save()
                Client.objects.create(user=user,age=age,phone_no=ph_no)
                registered = True
                print('client created')
            finally:
                return render(request,'client_registration.html',{'registered':registered,"username_exists":username_exists,
                                                                        "email_exists":email_exists})
        finally:
            return render(request,'client_registration.html',{'registered':registered,"username_exists":username_exists,
                                                                        "email_exists":email_exists})
    else:
        return render(request,'client_registration.html',{'registered':registered,"username_exists":username_exists,
                                                                        "email_exists":email_exists})

def user_login(request):
    credentials_failed = False
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = None
        if User.objects.filter(email=email).exists:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                try:
                    Developer.objects.get(user=user)
                    print('you are developer') # check for developer instance
                    return HttpResponseRedirect(reverse('view_all_projects_dev'))
                except Developer.DoesNotExist:
                    #check for client instance coz even admin instance can cause conflict
                    # Client.objects.get(user=user)
                    print('you are client')
                    return HttpResponseRedirect(reverse('client_post_project'))
            else:
                return HttpResponse(r"ACCOUNT IS NOT LOGGED IN \n <a href=\"{% url 'login' %}\">To retry click here.</a> ")
        else:
            credentials_failed = True
    return render(request,'login.html',{'credentials_failed':credentials_failed})


@login_required
def user_logout(request):
    logout(request)
    return redirect('/home/') #redirects to index after logging out


#CLIENT VIEWS

@login_required
def post_project(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        domain = request.POST['domain']
        experience_level = request.POST['experience']
        description = request.POST['description']
        offered_price = request.POST['offered_price']
        user = Client.objects.get(user= request.user)
        Project.objects.create(title = project_name,domain =domain, lvl_exp = experience_level, 
                                description = description, offered_price = offered_price,client_id=user)
    return render(request,"client_post_project.html")

@login_required
def posted_project(request):
    has_projects = True
    user = Client.objects.get(user= request.user)
    particualarClientproj= Project.objects.filter(client_id=user)
    if(len(particualarClientproj)==0):
        has_projects = False
    return render(request,'client_posted_projects.html',{'posts':particualarClientproj,'has_projects':has_projects})

@login_required
def project_view_client(request,project_id):
    projectobj=Project.objects.get(project_id=project_id)
    bidderListObj= PSRecord.objects.filter(project_id=project_id)
    return render(request,'view_single_project_client.html',{'project':projectobj,'bidders':bidderListObj})

@login_required
def project_delete(request,project_id): #verify if the current user is the owner of the project, have to be added
    projectobj=Project.objects.get(project_id=project_id)
    projectobj.delete()
    return HttpResponseRedirect(reverse('client_posted_projects'))

@login_required
def edit_profile_client(request):
    username_exists = False
    user=Client.objects.get(user=request.user)
    if request.method=='POST':
        if User.objects.filter(username=request.POST['name']).exists() and request.user.username != request.POST['name']:
            username_exists = True
        else:
            if request.user.username != request.POST['name']:
                main_user = User.objects.get(username=request.user.username)
                main_user.username=request.POST['name']
                main_user.save()
            user.ph_no=request.POST['phoneNo']
            user.age=request.POST['age']
            user.save()
            print(user.user.username)
            return HttpResponseRedirect(reverse('self_profile_client'))
    return render(request,'edit_profile_client.html',{'user':user,'username_exists':username_exists})

@login_required
def self_client_profile(request):
    user=Client.objects.get(user = request.user)
    return render( request,'self_profile_client.html',{'user':user})

@login_required
def confirmation(request,psid):
    bidderObj= PSRecord.objects.get(id=psid)
    dev_Obj=bidderObj.dev_id
    projectobj=bidderObj.project_id
    client_Obj = bidderObj.client_id
    print(bidderObj.bid_price)
    return render(request,'selected_freelancer_client.html',{'project':projectobj,'client':client_Obj,'bidder':bidderObj,
                                                            'dev':dev_Obj,'projectid':bidderObj.project_id.project_id})

@login_required
def bill_final(request,psid):
    BidObj = PSRecord.objects.get(id=psid)
    clientObj = BidObj.client_id
    devObj = BidObj.dev_id
    projectObj = BidObj.project_id
    bid_price = BidObj.bid_price
    projectObj.proj_selected_flag = True
    if(not Final_bid.objects.filter(dev_id=devObj, client_id= clientObj, bid_price=bid_price, project_id=projectObj).exists()):
        Final_bid.objects.create(dev_id=devObj, client_id= clientObj, bid_price=bid_price, project_id=projectObj)
    projectObj.save()
    return render(request,'bill_final.html',{'client':clientObj,'dev':devObj,'project':projectObj,'bid_price':bid_price})

@login_required
def finalized_project(request):
    user = Client.objects.get(user=request.user)
    particualarClientproj= Final_bid.objects.filter(client_id=user)
    return render(request,'client_finalized_projects.html',{'posts':particualarClientproj})

@login_required
def view_dev_profile(request,dev_id):
    user = Developer.objects.get(dev_id= dev_id)
    return render(request,'view_dev_profile.html',{'user':user})

@login_required
def view_bill(request,final_bid_id):
    post = Final_bid.objects.get(id= final_bid_id)
    return render(request,'view_bill_client.html',{'post':post})

@login_required
def project_mark_completed(request,final_bid_id):
    post = Final_bid.objects.get(id= final_bid_id)
    post.project_finished = True
    post.save()
    return HttpResponseRedirect(reverse('client_finalized_projects'))

@login_required
def review(request,final_bid_id):
    if request.method == 'POST':
        post = Final_bid.objects.get(id= final_bid_id)
        post.review = request.POST['review']
        post.save()
    return HttpResponseRedirect(reverse('client_finalized_projects'))

#DEVELOPER VIEWS
@login_required
def dev_posted_projects(request):
    projects_exists = True
    user = Developer.objects.get(user= request.user)
    domain=user.domain
    projectListObj=Project.objects.filter(domain=domain)
    if len(projectListObj) == 0:
        projects_exists = False
    return render(request,'view_all_projects.html',{'projects':projectListObj,'projects_exists':projects_exists})

@login_required
def project_view_dev(request,project_id): #repetitions of bidding from the same user has to be reduced
    already_bidded = False
    if PSRecord.objects.filter(project_id=Project.objects.get(project_id= project_id),dev_id= Developer.objects.get(user=request.user)).exists():
        already_bidded=True
    if request.method=='POST':
        dev_user = Developer.objects.get(user = request.user)
        dev_name=dev_user.user.username
        dev_id_obj = dev_user
        project_id_obj = Project.objects.get(project_id=project_id)
        client_id_obj = project_id_obj.client_id
        bid_price=request.POST['price']
        PSRecord.objects.create(dev_id=dev_id_obj,client_id=client_id_obj,bid_price=bid_price,project_id=project_id_obj,dev_name=dev_name)
        return HttpResponseRedirect(reverse('view_project_dev',args=[project_id]))
    else:
        projectobj = Project.objects.get(project_id=project_id)
        clientObj=projectobj.client_id
        bidderListObj= PSRecord.objects.filter(project_id=project_id)
        return render(request,'view_single_project_dev.html',{'project':projectobj,'client':clientObj,'bidders':bidderListObj,'projectid':project_id,"already_bidded":already_bidded})

@login_required
def applied_projects(request):
    if_applied = True
    user = Developer.objects.get(user= request.user)
    listOfAppliedProjects = PSRecord.objects.filter(dev_id=user.dev_id)
    if len(listOfAppliedProjects) == 0:
        if_applied = False
    NameAndPrice=[]
    for i in listOfAppliedProjects:
        lis=[]
        name=Project.objects.get(client_id=i.client_id,project_id=i.project_id.project_id).title
        lis.append(name)
        lis.append(i.bid_price)
        lis.append(i.project_id)
        NameAndPrice.append(lis)
    return render(request,'applied_projects_dev.html',{'appliedProjects':NameAndPrice,"if_applied":if_applied})

@login_required
def self_dev_profile(request):
    user=Developer.objects.get(user= request.user)
    return render(request,'self_profile_freelancer.html',{'user':user})

@login_required
def edit_profile_dev(request):# should add sample url option
    username_exists = False
    user=Developer.objects.get(user=request.user)
    if request.method=='POST':
        if User.objects.filter(username=request.POST['name']).exists() and request.user.username != request.POST['name']:
            username_exists = True
        else:
            if request.user.username != request.POST['name']:
                main_user = User.objects.get(username=request.user.username)
                main_user.username=request.POST['name']
                main_user.save()
            user.ph_no=request.POST['phoneNo']
            user.age=request.POST['age']
            user.exp = request.POST['experience']
            user.domain = request.POST['domain']
            user.charging_basis = request.POST['cost']
            user.save()
            return HttpResponseRedirect(reverse('self_profile_dev'))
    return render(request,'edit_profile_dev.html',{'user':user,"username_exists":username_exists})

@login_required
def selected_project_dev(request):
    user = Developer.objects.get(user = request.user)
    lis_of_projects = Final_bid.objects.filter(dev_id= user)
    return render(request,'hired_projects_dev.html',{'posts':lis_of_projects})

@login_required
def view_client_profile(request,client_id):
    user = Client.objects.get(client_id= client_id)
    return render(request,'view_client_profile.html',{'user':user})

@login_required
def viewdev_profile(request,dev_id):
    user = Developer.objects.get(dev_id= dev_id)
    return render(request,'viewdev_profile.html',{'user':user})

@login_required
def feedback(request,final_bid_id):
    if request.method == 'POST':
        post = Final_bid.objects.get(id=final_bid_id)
        post.feedback = request.POST['feedback']
        post.save()
    return HttpResponseRedirect(reverse('dev_selected_projects'))

@login_required
def view_bill_dev(request,final_bid_id):
    post = Final_bid.objects.get(id= final_bid_id)
    return render(request,'view_bill_dev.html',{'post':post})