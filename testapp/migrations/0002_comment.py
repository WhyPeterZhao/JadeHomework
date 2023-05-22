from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment_content", models.TextField(verbose_name="评论内容")),
                (
                    "comment_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="评论时间"),
                ),
                (
                    "comment_author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="testapp.user",
                        verbose_name="评论者",
                    ),
                ),
                (
                    "pre_comment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="testapp.comment",
                        verbose_name="父评论id",
                    ),
                ),
                (
                    "video_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="testapp.video",
                        verbose_name="评论视频",
                    ),
                ),
            ],
            options={
                "verbose_name": "评论",
                "verbose_name_plural": "评论",
                "db_table": "comment_tb",
            },
        ),
    ]
