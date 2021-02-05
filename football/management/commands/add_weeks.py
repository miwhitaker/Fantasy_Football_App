import csv
from football.models import Week
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('C:/Users/ollup/Desktop/Class stuff/NFL Stats/weekly/2019/week5.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                info = Week(
                    week = 5,
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
                print('Added player: ' + row['Player'])