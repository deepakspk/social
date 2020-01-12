from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Contributor(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    t= models.IntegerField(null=True,blank=True,default=0)
    y = models.IntegerField(null=True,blank=True,default=0)
    n = models.IntegerField(null=True,blank=True,default=0)
    m = models.IntegerField(null=True,blank=True,default=0)
    u = models.IntegerField(null=True,blank=True,default=0)
    remarks = models.CharField(max_length=200,null=True,blank=True)
    win_date = models.DateField(null=True,blank=True)
    img = models.ImageField(upload_to='pics',null=True,blank=True)
    new = models.BooleanField(null=True,blank=True,default=False)
    email = models.EmailField(max_length=70,blank=True,null=True)

    def __str__ (self):
        return self.name

    def get_absolute_url(self):
        return reverse("nursesApp:contributorDetail", kwargs={'pk':self.pk})

class Member(models.Model):
    name = models.CharField(max_length=160)
    joined_on = models.DateField()
    added_by = models.ForeignKey(Contributor, related_name='contributors', on_delete=models.CASCADE,null=True,blank=True)
    NURSE_CHOICES = (('Y', 'Yes'),('N', 'No'),('M', 'Maybe'),)
    nurse = models.CharField(max_length=1, choices=NURSE_CHOICES)
    position = models.CharField(max_length=200)
    remarks = models.CharField(max_length=200,null=True,blank=True)
    url = models.URLField()
    img = models.ImageField(upload_to='pics',null=True,blank=True)
    new = models.BooleanField(null=True,blank=True,default=False)
    email = models.EmailField(max_length=70,blank=True,null=True)

    def __str__ (self):
        return self.name

    def get_absolute_url(self):
        return reverse("nursesApp:memberDetail", kwargs={'pk':self.pk})

@receiver(post_save,sender=Member)
def addToContributor(sender, instance, *args, **kwargs):
    getMember = Member.objects.get(id=instance.id)
    try:
        checkContrib = Contributor.objects.get(name=getMember.added_by)
        checkContrib.t += 1
        if getMember.nurse == "Y":
            checkContrib.y += 1
        elif getMember.nurse == "N":
            checkContrib.n += 1
        else:
            checkContrib.m += 1
        checkContrib.save()
        Contributor.objects.create(name=getMember.name)
    except Contributor.DoesNotExist:
        Contributor.objects.create(name=getMember.name)

class Msg(models.Model):
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField()

    def __str__ (self):
        return self.name
