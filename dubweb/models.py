from django.db import models
# from django.contrib.auth.models import User


class UserProfile(models.Model):
    user_id = models.CharField(unique=True, max_length=80, primary_key=True)
    user_name = models.CharField(max_length=80)
    user_head = models.URLField(blank=False)

    def __unicode__(self):
        return u'%s %s' % (self.uid, self.user_name)


class Film(models.Model):
    title = models.CharField(max_length=80)
    film_id = models.CharField(max_length=80, unique=True, primary_key=True)
    film_url = models.URLField(blank=False)
    image_url = models.URLField(blank=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # user_id = models.CharField(max_length=80)
    play_count = models.IntegerField(default=0)
    good_count = models.IntegerField(default=0)
    # coo_user_Id = models.ForeignKey(UserProfile)
    # publish_time = models.DateTimeField(auto_now_add=False)
    # update_time = models.DateTimeField(auto_now=True)
    # tags = models.ManyToManyField('Tag', blank=True)
    # content = models.TextField()

    def __unicode__(self):
        return u'%s %s %s %s' % (self.title, self.film_id, self.film_url, self.user_id)
