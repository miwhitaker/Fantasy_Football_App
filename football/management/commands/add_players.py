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
                info = Players(
                    name = row['Player'], 
                    team = row['Tm'], 
                    position = row['Pos'], 
                    pass_yds = int(float(row['PassingYds'])), 
                    pass_tds = int(float(row['PassingTD'])), 
                    interceptions = int(float(row['Int'])), 
                    fumbles = int(float(row['FumblesLost'])), 
                    rush_yds = int(float(row['RushingYds'])), 
                    rush_tds = int(float(row['RushingTD'])), 
                    rec_yds = int(float(row['ReceivingYds'])), 
                    rec_tds = int(float(row['ReceivingTD'])))
                info.save()
        
#remove the print statements(not lines themselves), nobody wants to see all that