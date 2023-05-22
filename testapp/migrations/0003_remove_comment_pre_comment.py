from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0002_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="pre_comment",
        ),
    ]
