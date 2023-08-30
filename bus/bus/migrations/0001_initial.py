# Generated by Django 4.2.4 on 2023-08-29 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusRunningTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_id', models.FloatField()),
                ('deviceid', models.FloatField()),
                ('direction', models.FloatField()),
                ('segment', models.FloatField()),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('run_time_in_seconds', models.FloatField()),
                ('length', models.FloatField()),
                ('day_of_week', models.FloatField()),
                ('time_of_day', models.FloatField()),
                ('Sunday_holiday', models.FloatField()),
                ('saturday', models.IntegerField()),
                ('weekday_end', models.IntegerField()),
                ('week_no', models.FloatField()),
                ('rt_w_1', models.FloatField()),
                ('rt_w_2', models.FloatField()),
                ('rt_w_3', models.FloatField()),
                ('rt_t_1', models.FloatField()),
                ('rt_t_2', models.FloatField()),
                ('rt_n_1', models.FloatField()),
                ('rt_n_2', models.FloatField()),
                ('rt_n_3', models.FloatField()),
                ('hour_of_day', models.FloatField()),
                ('day', models.FloatField()),
                ('month', models.FloatField()),
                ('temp', models.FloatField()),
                ('precip', models.FloatField()),
                ('windspeed', models.FloatField()),
                ('conditions', models.CharField(max_length=255)),
                ('dt_n_1', models.FloatField()),
            ],
            options={
                'db_table': 'bus_running_times',
            },
        ),
    ]