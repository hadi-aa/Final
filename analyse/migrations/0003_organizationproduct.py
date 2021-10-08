# Generated by Django 3.2.8 on 2021-10-06 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyse', '0002_delete_organizationproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyse.organization')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyse.product')),
            ],
        ),
    ]
