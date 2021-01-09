from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Developer(models.Model):
    dev_id = models.AutoField(primary_key = True)
    user = models.OneToOneField(User,on_delete = models.CASCADE) #contains basic fields like name,password and email field
    age = models.PositiveIntegerField() 
    exp = models.TextField() #experience of developer like beginner, intermediate and expert
    charging_basis = models.TextField() #hourly or contract basis
    domain = models.TextField() #domain in which the developer would prefer app, desktop or web 
    phone_no = models.CharField(max_length = 10)
    # sample_project_url = models.URLField(blank = True)

    def __str__(self):
        return self.user.username

class Client(models.Model):
    client_id = models.AutoField(primary_key = True)
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    age = models.PositiveIntegerField() 
    phone_no = models.CharField(max_length = 10)

    def __str__(self):
        return self.user.username

class Project(models.Model): # project model
    project_id = models.AutoField(primary_key = True)
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    domain = models.TextField() # app, desktop or web 
    lvl_exp = models.TextField()
    offered_price = models.IntegerField()
    proj_selected_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PSRecord(models.Model): #a collection of all the bids of all the projects
    bid_price = models.PositiveIntegerField()
    dev_id = models.ForeignKey(Developer,on_delete=models.CASCADE)
    dev_name = models.TextField()
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE)

    def __str__(self):
        return self.project_id.title+" "+self.dev_name

class Final_bid(models.Model) : #after selection of a developer and finalising the projects
    date = models.DateField(auto_now_add= True) #finalised project date
    bid_price = models.PositiveIntegerField() 
    dev_id = models.ForeignKey(Developer,on_delete=models.DO_NOTHING)
    client_id = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    project_id = models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    project_finished = models.BooleanField(default=False) # check if the project is completed
    review = models.TextField(blank=True) #review from client
    feedback = models.TextField(blank= True) #feedback from developer

    def __str__(self):
        return self.project_id.title