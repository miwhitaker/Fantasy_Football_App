import csv
from football.models import Week1
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('C:/Users/ollup/Desktop/Class stuff/NFL Stats/weekly/2019/week1.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            print(csv_reader)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    f'Column names are {", ".join(row)}'
                f'\t{row}'
                info = Week1(
                    name = row['Player'], 
                    team = row['Tm'], 
                    position = row['Pos'], 
                    pass_yds = float(row['PassingYds']), 
                    pass_tds = int(float(row['PassingTD'])), 
                    interceptions = int(float(row['Int'])), 
                    fumbles = int(float(row['FL'])), 
                    rush_yds = float(row['RushingYds']), 
                    rush_tds = int(float(row['RushingTD'])), 
                    rec_yds = float(row['ReceivingYds']), 
                    rec_tds = int(float(row['ReceivingTD'])),
                    points = float(row['StandardFantasyPoints']))
                info.save()
                print('working')