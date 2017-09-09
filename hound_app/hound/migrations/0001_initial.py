# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-24 21:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('assigned_id', models.IntegerField(blank=True, default=0)),
                ('street', models.CharField(blank=True, max_length=60)),
                ('country_addr', models.CharField(blank=True, default='', max_length=10)),
                ('state_addr', models.CharField(blank=True, default='', max_length=20)),
                ('city_addr', models.CharField(blank=True, default='', max_length=20)),
                ('zip_code', models.IntegerField(blank=True, default=0, null=True)),
                ('ext', models.CharField(blank=True, max_length=8, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('date', models.DateField(default=datetime.datetime.now)),
                ('date_id', models.AutoField(null=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('assigned_id', models.IntegerField(default=0)),
                ('phone_number', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id_documents', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('assigned_id', models.IntegerField(blank=True, default=0)),
                ('id', models.CharField(blank=True, default='', max_length=20)),
                ('rfc', models.CharField(blank=True, default='', max_length=10)),
                ('curp', models.CharField(blank=True, default='', max_length=18)),
                ('license_no', models.CharField(blank=True, default='', max_length=20)),
                ('license_issue_date', models.DateField(blank=True, null=True)),
                ('license_exp_date', models.DateField(blank=True, null=True)),
                ('license_type', models.CharField(blank=True, default='', max_length=10)),
                ('passport_no', models.CharField(blank=True, default='', max_length=30)),
                ('passport_issue_date', models.DateField(blank=True, null=True)),
                ('passport_exp_date', models.DateField(blank=True, null=True)),
                ('dot', models.BooleanField(default=False)),
                ('criminal_record', models.BooleanField(default=False)),
                ('prints_img', models.CharField(blank=True, default='hound/images/default.jpg', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('assigned_id', models.IntegerField(blank=True, default=0)),
                ('name', models.CharField(max_length=20)),
                ('middle_name', models.CharField(blank=True, max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=20)),
                ('state', models.CharField(blank=True, default='', max_length=20)),
                ('city', models.CharField(blank=True, default='', max_length=20)),
                ('email_address', models.EmailField(blank=True, max_length=254)),
                ('profile_img', models.CharField(blank=True, default='hound/images/default.jpg', max_length=100, verbose_name='Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='DriverStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('assigned_id', models.IntegerField(blank=True, default=0)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('leave_reason', models.TextField(blank=True, default='')),
                ('expired', models.BooleanField(default=False)),
                ('id_driver', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hound.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='Prints',
            fields=[
                ('id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('user_id', models.CharField(blank=True, default='none', max_length=5)),
                ('prints', models.FileField(blank=True, default='/hound/images/default.jpg', null=True, upload_to='')),
                ('path', models.CharField(blank=True, default='/hound/images/default.jpg', max_length=100)),
                ('gen_id', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('user_id', models.CharField(blank=True, default='none', max_length=5)),
                ('profile', models.FileField(blank=True, default='/hound/images/default.jpg', null=True, upload_to='')),
                ('path', models.CharField(blank=True, default='/hound/images/default.jpg', max_length=100)),
                ('type', models.CharField(blank=True, default='none', max_length=10)),
                ('gen_id', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reset',
            fields=[
                ('token', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('economic_no', models.IntegerField(blank=True, default=0)),
                ('plate_no', models.CharField(blank=True, default='', max_length=10)),
                ('country', models.CharField(blank=True, default='', max_length=10)),
                ('state', models.CharField(blank=True, default='', max_length=20)),
                ('year', models.IntegerField(blank=True, choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036)], default=0, null=True)),
                ('capacity', models.IntegerField(blank=True, default=0, null=True)),
                ('type', models.CharField(blank=True, default='', max_length=30)),
                ('client_name', models.CharField(blank=True, default='', max_length=20)),
                ('client_last_name', models.CharField(blank=True, default='', max_length=20)),
                ('use', models.CharField(blank=True, default='', max_length=20)),
                ('status', models.CharField(blank=True, default='', max_length=35)),
                ('active', models.BooleanField(default=True)),
                ('rent_date', models.DateField(blank=True, null=True)),
                ('deliver_date', models.DateField(blank=True, null=True)),
                ('start_service_date', models.DateField(blank=True, null=True)),
                ('end_service_date', models.DateField(blank=True, null=True)),
                ('profile_img', models.CharField(blank=True, default='hound/images/default.jpg', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('trip_id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('assigned_id', models.IntegerField(blank=True, default=0, null=True)),
                ('vehicle_no', models.IntegerField(blank=True, default=0, null=True)),
                ('trailer_no', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('start_time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('end_time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('origin', models.CharField(default='', max_length=35)),
                ('destiny', models.CharField(default='', max_length=35)),
                ('trip_type', models.CharField(default='', max_length=20)),
                ('status', models.CharField(blank=True, choices=[('CANCELED', 'CANCELED'), ('DELIVERED', 'DELIVERED'), ('PENDING', 'PENDING')], default='PENDING', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=32, unique=True, verbose_name='Url')),
                ('expires', models.DateTimeField(verbose_name='Expires')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=512)),
                ('name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('company', models.CharField(blank=True, default='', max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('payed', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('profile_img', models.CharField(blank=True, default='hound/images/default.jpg', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vacations',
            fields=[
                ('vacation_id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('assigned_id', models.IntegerField(blank=True, default=0)),
                ('year', models.IntegerField(choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036)], default=0)),
                ('no_days', models.IntegerField(default=0)),
                ('payment_rate', models.IntegerField(default=0)),
                ('taken_days', models.IntegerField(blank=True, default=0, null=True)),
                ('amount_payed', models.IntegerField(default=0)),
                ('payed', models.BooleanField(default=False)),
                ('exchange_rate', models.CharField(choices=[('DLL', 'DLL'), ('MXN', 'MXN')], default='DLL', max_length=5)),
                ('id_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hound.Driver')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.User')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, null=True, primary_key=True, serialize=False)),
                ('economic_no', models.IntegerField(blank=True, default=0)),
                ('vin', models.CharField(blank=True, default='', max_length=17)),
                ('plate_no', models.CharField(blank=True, default='', max_length=10)),
                ('country', models.CharField(blank=True, default='', max_length=10)),
                ('state', models.CharField(blank=True, default='', max_length=20)),
                ('year', models.IntegerField(blank=True, choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036)], default=0, null=True)),
                ('model', models.CharField(blank=True, default='', max_length=30)),
                ('brand', models.CharField(blank=True, default='', max_length=30)),
                ('type', models.CharField(blank=True, default='', max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('status', models.CharField(blank=True, default='', max_length=35)),
                ('profile_img', models.CharField(blank=True, default='hound/images/default.jpg', max_length=100)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.User')),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.User'),
        ),
        migrations.AddField(
            model_name='trailer',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.User'),
        ),
        migrations.AddField(
            model_name='driverstatus',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.User'),
        ),
        migrations.AddField(
            model_name='driver',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.User'),
        ),
        migrations.AddField(
            model_name='documents',
            name='id_driver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hound.Driver'),
        ),
        migrations.AddField(
            model_name='documents',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.User'),
        ),
        migrations.AddField(
            model_name='directory',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.User'),
        ),
        migrations.AddField(
            model_name='date',
            name='vacation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.Vacations'),
        ),
        migrations.AddField(
            model_name='address',
            name='id_driver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hound.Driver'),
        ),
        migrations.AddField(
            model_name='address',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hound.User'),
        ),
    ]
