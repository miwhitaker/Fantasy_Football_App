from django.db import models

class Players(models.Model):
    name = models.CharField(max_length = 100)
    team = models.CharField(max_length = 20)
    position = models.CharField(max_length = 10)
    pass_yds = models.IntegerField()
    pass_tds = models.IntegerField()
    interceptions = models.IntegerField()
    fumbles = models.IntegerField()
    rush_yds = models.IntegerField()
    rush_tds = models.IntegerField()
    rec_yds = models.IntegerField()
    rec_tds = models.IntegerField()

