# Generated by Django 3.1.5 on 2021-02-04 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0005_auto_20210128_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('team', models.CharField(max_length=20)),
                ('position', models.CharField(max_length=10)),
                ('pass_yds', models.DecimalField(decimal_places=2, max_digits=6)),
                ('pass_tds', models.IntegerField()),
                ('interceptions', models.IntegerField()),
                ('fumbles', models.IntegerField()),
                ('rush_yds', models.DecimalField(decimal_places=2, max_digits=6)),
                ('rush_tds', models.IntegerField()),
                ('rec_yds', models.DecimalField(decimal_places=2, max_digits=6)),
                ('rec_tds', models.IntegerField()),
                ('points', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.DeleteModel(
            name='Week1',
        ),
        migrations.DeleteModel(
            name='Week2',
        ),
        migrations.DeleteModel(
            name='Week3',
        ),
        migrations.DeleteModel(
            name='Week4',
        ),
        migrations.DeleteModel(
            name='Week5',
        ),
    ]