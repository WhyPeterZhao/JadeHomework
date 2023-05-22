from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0003_remove_comment_pre_comment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="video_id",
            new_name="video",
        ),
    ]
