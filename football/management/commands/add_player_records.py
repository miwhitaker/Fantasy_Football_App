from football.models import Players, Week
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        players = Players.objects.all()
        for player in players:
            for num in range(1, 6):
                try:
                    player_stats = Week.objects.filter(
                        name = player.name,
                        week = num
                        )
                except Week.DoesNotExist:
                    Week.objects.create(
                        week = num,
                        name = player.name,
                        team = player.team,
                        position = player.position,
                        pass_yds = 0,
                        pass_tds = 0,
                        interceptions = 0,
                        fumbles = 0,
                        rush_yds = 0,
                        rush_tds = 0,
                        rec_yds = 0,
                        rec_tds = 0,
                        points = 0,
                    )