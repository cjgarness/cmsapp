from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_page_show_in_navbar'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='show_in_page_list',
            field=models.BooleanField(default=True),
        ),
    ]
