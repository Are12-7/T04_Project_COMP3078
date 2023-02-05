from django.db import models
from django.contrib.auth.models import User


# Name
class Debate(models.Model):
    topic = models.CharField(max_length=150)

    def __str__(self):
        return self.topic


# VILLAGE
class Village(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey(Debate, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    # Many to many / change to false in production
    sophists = models.ManyToManyField(
        User, related_name='sophists', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # Sorting elements
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title


# DISCUSSION - Messages within the village
class Message(models.Model):
    # one to many relationship
    # if the village is removed, the messages will be removed as well
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.content[0:40]
