from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_person_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='certificate',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='certificate'),
        ),
    ]
