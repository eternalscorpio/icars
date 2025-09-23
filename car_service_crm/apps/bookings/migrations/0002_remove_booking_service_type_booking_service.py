# apps/bookings/migrations/0002_auto_...py
from django.db import migrations, models
import django.db.models.deletion
from datetime import timedelta

def migrate_service_types(apps, schema_editor):
    Booking = apps.get_model('bookings', 'Booking')
    Service = apps.get_model('services', 'Service')
    service_map = {
        'Oil Change': ('Oil Change', 'Standard oil change service', 50.00, timedelta(hours=1)),
        'Tire Rotation': ('Tire Rotation', 'Rotate tires for even wear', 30.00, timedelta(minutes=45)),
        'Engine Repair': ('Engine Repair', 'Comprehensive engine diagnostics and repair', 200.00, timedelta(hours=3)),
        'AC Service': ('AC Service', 'Air conditioning system maintenance', 100.00, timedelta(hours=1, minutes=30)),
    }
    for service_type, (name, description, price, duration) in service_map.items():
        service, created = Service.objects.get_or_create(
            name=name,
            defaults={'description': description, 'price': price, 'duration': duration}
        )
        Booking.objects.filter(service_type=service_type).update(service=service)
    try:
        default_service = Service.objects.get(name='Default Service')
    except Service.DoesNotExist:
        default_service = Service.objects.create(
            name='Default Service',
            description='Temporary default service for migration',
            price=0.00,
            duration=timedelta(hours=1)
        )
    Booking.objects.filter(service__isnull=True).update(service=default_service)

def reverse_migrate_service_types(apps, schema_editor):
    Booking = apps.get_model('bookings', 'Booking')
    Service = apps.get_model('services', 'Service')
    service_map = {
        'Oil Change': 'Oil Change',
        'Tire Rotation': 'Tire Rotation',
        'Engine Repair': 'Engine Repair',
        'AC Service': 'AC Service',
    }
    for service_name, service_type in service_map.items():
        try:
            service = Service.objects.get(name=service_name)
            Booking.objects.filter(service=service).update(service_type=service_type)
        except Service.DoesNotExist:
            pass
    try:
        default_service = Service.objects.get(name='Default Service')
        Booking.objects.filter(service=default_service).update(service_type='Unknown')
    except Service.DoesNotExist:
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('bookings', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='Booking',
            name='service',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='bookings',
                to='services.service',
                verbose_name='Service',
            ),
        ),
        migrations.RunPython(
            code=migrate_service_types,
            reverse_code=reverse_migrate_service_types,
        ),
        migrations.AlterField(
            model_name='Booking',
            name='service',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='bookings',
                to='services.service',
                verbose_name='Service',
            ),
        ),
        migrations.RemoveField(
            model_name='Booking',
            name='service_type',
        ),
    ]