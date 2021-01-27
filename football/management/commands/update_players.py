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
                    points = row['FantasyPoints'])
                info.save()