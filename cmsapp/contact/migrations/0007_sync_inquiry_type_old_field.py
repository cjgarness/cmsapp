# Generated migration to sync inquiry_type_old field that already exists in DB

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_alter_inquirytype_options_and_more'),
    ]

    operations = [
        # This migration syncs Django's state with the existing database field
        # The field inquiry_type_old already exists in the database with NOT NULL constraint
        # We're adding it to the model definition to match reality
        migrations.AddField(
            model_name='contactinquiry',
            name='inquiry_type_old',
            field=models.CharField(default='general', help_text='Deprecated: Use inquiry_type ForeignKey instead', max_length=50),
        ),
    ]
