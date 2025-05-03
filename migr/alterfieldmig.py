from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', 'slugfieldmig.py'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
    ]