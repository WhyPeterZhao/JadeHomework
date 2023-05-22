from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0004_rename_video_id_comment_video"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="is_valid",
            field=models.BooleanField(default=False, verbose_name="是否通过审核"),
        ),
    ]
