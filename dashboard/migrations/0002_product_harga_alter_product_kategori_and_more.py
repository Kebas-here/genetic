# Generated by Django 4.2.2 on 2023-07-08 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='harga',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='kategori',
            field=models.CharField(choices=[('smartphone', 'smartphone'), ('aksesoris', 'aksesoris'), ('perangkat lain', 'perangkat lain')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='kuantitas',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='nama',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='noproduk',
            field=models.AutoField(primary_key=True),
        ),
    ]
