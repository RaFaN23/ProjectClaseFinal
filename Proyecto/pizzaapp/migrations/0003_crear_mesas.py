from django.db import migrations

def crear_mesas(apps, schema_editor):
    Mesa = apps.get_model('pizzaapp', 'Mesa')
    estadoMesa = apps.get_model('pizzaapp', 'Mesa')._meta.get_field('estado').choices

    for i in range(1, 10):
        Mesa.objects.get_or_create(numero=i, defaults={'estado': 'LIBRE'})

class Migration(migrations.Migration):

    dependencies = [
        ('pizzaapp', '0001_initial'),  # Ajusta al nombre de tu migración anterior
    ]

    operations = [
        migrations.RunPython(crear_mesas),
    ]
