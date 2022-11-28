from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_filmwork_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.TextField(choices=[('male', 'male'), ('female', 'female')], null=True, verbose_name='gender'),
        ),
    ]
