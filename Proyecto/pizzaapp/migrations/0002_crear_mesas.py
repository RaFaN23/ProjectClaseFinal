from django.db import migrations

def crear_mesas(apps, schema_editor):
    Mesa = apps.get_model('pizzaapp', 'Mesa')

    for i in range(1, 10):
        Mesa.objects.get_or_create(numero=i, defaults={'estado': 'LIBRE'})  # 'LIBRE' es el valor del enum

class Migration(migrations.Migration):

    dependencies = [
        ('pizzaapp', '0001_initial'),  # Ajusta si tu archivo de migración inicial tiene otro nombre
    ]

    operations = [
        migrations.RunPython(crear_mesas),
    ]
