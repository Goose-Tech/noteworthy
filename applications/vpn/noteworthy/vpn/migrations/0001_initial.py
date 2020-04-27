# Generated by Django 3.0.5 on 2020-04-27 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VPNDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('wg_pubkey', models.CharField(max_length=44)),
                ('wg_privkey', models.CharField(max_length=44)),
                ('ipv4_address', models.GenericIPAddressField(blank=True, null=True, protocol='IPv4')),
                ('ipv4_cidr_prefix', models.CharField(blank=True, max_length=3, null=True)),
                ('ipv6_address', models.GenericIPAddressField(blank=True, null=True, protocol='IPv4')),
                ('ipv6_cidr_prefix', models.CharField(blank=True, max_length=3, null=True)),
                ('endpoint', models.GenericIPAddressField(protocol='IPv4')),
                ('endpoint_port', models.IntegerField()),
                ('allowed_ips', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
    ]
