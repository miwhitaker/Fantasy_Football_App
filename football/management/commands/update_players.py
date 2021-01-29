import csv
from football.models import Players
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('C:/Users/ollup/Desktop/Class stuff/NFL Stats/yearly/2018.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            print(csv_reader)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    f'Column names are {", ".join(row)}'
                f'\t{row}'
                find_player = Players.objects.filter(name=row['Player'], position=row['Pos'])
                if not find_player:
                    continue
                player = find_player[0]
                print(player)
                player.pass_yds = float(row['PassingYds'])
                player.pass_tds = int(float(row['PassingTD']))
                player.interceptions = int(float(row['Int']))
                player.fumbles = int(float(row['FumblesLost']))
                player.rush_yds = float(row['RushingYds'])
                player.rush_tds = int(float(row['RushingTD']))
                player.rec_yds = float(row['ReceivingYds'])
                player.rec_tds = int(float(row['ReceivingTD']))
                player.points = row['FantasyPoints']
                player.save()