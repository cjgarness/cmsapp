# Generated migration for InquiryType model and ContactInquiry updates

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0001_initial'),
        ('contact', '0004_alter_contactinquiry_inquiry_type'),
    ]

    operations = [
        # Create the new InquiryType model
        migrations.CreateModel(
            name='InquiryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Internal identifier for this inquiry type', max_length=50)),
                ('label', models.CharField(help_text='Display name for this inquiry type', max_length=100)),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order in dropdown')),
                ('is_active', models.BooleanField(default=True, help_text='Enable/disable this inquiry type')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiry_types', to='domains.domain')),
            ],
            options={
                'verbose_name_plural': 'Inquiry Types',
            },
        ),
        
        # Add unique constraint to InquiryType
        migrations.AddConstraint(
            model_name='inquirytype',
            constraint=models.UniqueConstraint(fields=['domain', 'slug'], name='unique_domain_inquiry_slug'),
        ),
        
        # Add index to InquiryType
        migrations.AddIndex(
            model_name='inquirytype',
            index=models.Index(fields=['domain', 'is_active'], name='contact_inqu_domain_3f8a1c_idx'),
        ),
        
        # Add domain field to ContactInquiry
        migrations.AddField(
            model_name='contactinquiry',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_inquiries', to='domains.domain'),
        ),
        
        # Add inquiry_type_id ForeignKey to ContactInquiry
        migrations.AddField(
            model_name='contactinquiry',
            name='inquiry_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inquiries', to='contact.inquirytype'),
        ),
        
        # Add index to ContactInquiry for domain and status
        migrations.AddIndex(
            model_name='contactinquiry',
            index=models.Index(fields=['domain', 'status'], name='contact_cont_domain_8f4d2e_idx'),
        ),
    ]
