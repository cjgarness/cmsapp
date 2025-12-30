# Generated migration for contact app

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('company', models.CharField(blank=True, max_length=200, null=True)),
                ('inquiry_type', models.CharField(choices=[('question', 'General Question'), ('service', 'Service Inquiry'), ('support', 'Support Request'), ('feedback', 'Feedback'), ('partnership', 'Partnership Inquiry'), ('other', 'Other')], default='question', max_length=20)),
                ('subject', models.CharField(max_length=300)),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('new', 'New'), ('read', 'Read'), ('responded', 'Responded'), ('closed', 'Closed')], default='new', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('responded_at', models.DateTimeField(blank=True, null=True)),
                ('admin_notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Contact Inquiries',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ContactConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_email', models.EmailField(help_text='Email address where inquiries will be sent', max_length=254)),
                ('admin_name', models.CharField(default='Admin', help_text='Name to display in email signatures', max_length=200)),
                ('send_confirmation_email', models.BooleanField(default=True, help_text='Send confirmation emails to inquirers')),
                ('enable_sms_notifications', models.BooleanField(default=False, help_text='Enable SMS notifications for new inquiries')),
                ('sms_phone_number', models.CharField(blank=True, help_text='Phone number to receive SMS notifications (Twilio format: +1234567890)', max_length=20, null=True)),
                ('sms_api_key', models.CharField(blank=True, help_text='Twilio API key (stored securely)', max_length=255, null=True)),
                ('enable_contact_form', models.BooleanField(default=True, help_text='Enable or disable the contact form')),
                ('auto_response_enabled', models.BooleanField(default=True, help_text='Send automatic responses to inquiries')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Contact Configuration',
                'verbose_name_plural': 'Contact Configuration',
            },
        ),
        migrations.AddIndex(
            model_name='contactinquiry',
            index=models.Index(fields=['-created_at'], name='contact_con_created_idx'),
        ),
        migrations.AddIndex(
            model_name='contactinquiry',
            index=models.Index(fields=['status'], name='contact_con_status_idx'),
        ),
    ]
