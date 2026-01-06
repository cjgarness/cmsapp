from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0003_domainsetting_show_background_watermark'),
    ]

    operations = [
        migrations.AddField(
            model_name='domainsetting',
            name='enable_alert_email',
            field=models.BooleanField(default=True, help_text="Send email alerts to this domain's contact email"),
        ),
        migrations.AddField(
            model_name='domainsetting',
            name='enable_alert_sms',
            field=models.BooleanField(default=False, help_text="Send SMS alerts to this domain's contact phone"),
        ),
    ]
