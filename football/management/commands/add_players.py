import csv
from football.models import Players
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('C:/Users/ollup/Desktop/Class stuff/NFL Stats/yearly/2019.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            print(csv_reader)
            line_count = 0
            for row in csv_reader:
                try: 
                    if row['Pos'] == '0':
                        continue
                    info = Players(
                        name = row['Player'], 
                        team = row['Tm'], 
                        position = row['Pos'],
                        pass_yds = 0,
                        pass_tds = 0,
                        interceptions = 0,
                        fumbles = 0,
                        rush_yds = 0,
                        rush_tds = 0,
                        rec_yds = 0,
                        rec_tds = 0,
                        points = 0,)
                    info.save()
                    print('working, ', row['Player'], '"',row['Pos'],'"')
                except Exception as e:
                    print(e)
                    raise
                    