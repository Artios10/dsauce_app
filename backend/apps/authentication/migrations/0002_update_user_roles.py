from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[('admin', 'Admin'), ('merchant', 'Merchant'), ('customer', 'Customer')],
                default='customer',
                max_length=20,
            ),
        ),
    ]
