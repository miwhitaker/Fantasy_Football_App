from django.db import models
from .teams import team_names
import json
from django.contrib.auth.models import User

class Players(models.Model):
    name = models.CharField(max_length = 100)
    team = models.CharField(max_length = 20)
    position = models.CharField(max_length = 10)
    pass_yds = models.FloatField()
    pass_tds = models.IntegerField()
    interceptions = models.IntegerField()
    fumbles = models.IntegerField()
    rush_yds = models.FloatField()
    rush_tds = models.IntegerField()
    rec_yds = models.FloatField()
    rec_tds = models.IntegerField()
    points = models.FloatField()
    rostered_by = models.CharField(max_length = 50, default = '0')

    def __str__(self):
        return json.dumps({'name': self.name,
                            'team': team_names[self.team],
                            'position': self.position,
                            'passingyds': self.pass_yds,
                            'passingtds': self.pass_tds,
                            'rushingyds': self.rush_yds,
                            'rushingtds': self.rush_tds,
                            'recyds': self.rec_yds,
                            'rectds': self.rec_tds,
                            'interceptions': self.interceptions,
                            'fumbles': self.fumbles,
                            'id': self.id})


class Week(models.Model):
    week = models.IntegerField()
    name = models.CharField(max_length = 100)
    team = models.CharField(max_length = 20)
    position = models.CharField(max_length = 10)
    pass_yds = models.DecimalField(max_digits = 6, decimal_places = 2)
    pass_tds = models.IntegerField()
    interceptions = models.IntegerField()
    fumbles = models.IntegerField()
    rush_yds = models.DecimalField(max_digits = 6, decimal_places = 2)
    rush_tds = models.IntegerField()
    rec_yds = models.DecimalField(max_digits = 6, decimal_places = 2)
    rec_tds = models.IntegerField()
    points = models.DecimalField(max_digits = 6, decimal_places = 2)


class Record(models.Model):
    week = models.IntegerField()
    username = models.CharField(max_length = 100)
    win = models.IntegerField()
    loss = models.IntegerField()
    tie = models.IntegerField()
    points = models.DecimalField(max_digits = 6, decimal_places = 2)