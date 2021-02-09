from football.models import Players, Record
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_players = Players.objects.all()
        
        for player in all_players:
            player.rostered_by = '0'
            player.save()

        Record.objects.all().delete()
        

