# Generated by Django 4.2.3 on 2023-09-06 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item_track', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='client',
            name='state',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='client',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='item',
            name='expiration_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='stock',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='movemets',
            name='client',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='item_track.client'),
        ),
        migrations.AlterField(
            model_name='movemets',
            name='item',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='item_track.item'),
        ),
        migrations.AlterField(
            model_name='movemets',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='movemets',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='movemets',
            name='treatment',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='item_track.treatment'),
        ),
        migrations.AlterField(
            model_name='movemets',
            name='type',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='client',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='item_track.client'),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='payment_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='payment_comments',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='payment_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='payment_method',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='payment_reference',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='payment_status',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
