from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmailVerifyRecord",
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
                ("code", models.CharField(max_length=20, verbose_name="验证码")),
                ("email", models.EmailField(max_length=50, verbose_name="邮箱")),
                (
                    "send_type",
                    models.CharField(
                        choices=[("register", "注册账号"), ("forget", "找回密码")],
                        default="register",
                        max_length=10,
                    ),
                ),
                (
                    "send_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="时间"),
                ),
            ],
            options={
                "verbose_name": "邮箱验证码",
                "verbose_name_plural": "邮箱验证码",
            },
        ),
        migrations.CreateModel(
            name="User",
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
                ("name", models.CharField(max_length=128, unique=True)),
                ("password", models.CharField(max_length=256)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "sex",
                    models.CharField(
                        choices=[("male", "男"), ("female", "女")],
                        default="男",
                        max_length=32,
                    ),
                ),
                ("c_time", models.DateTimeField(auto_now_add=True)),
                ("is_staff", models.BooleanField(default=0, verbose_name="active")),
            ],
            options={
                "verbose_name": "用户",
                "verbose_name_plural": "用户",
                "ordering": ["-c_time"],
            },
        ),
        migrations.CreateModel(
            name="Video",
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
                (
                    "title",
                    models.CharField(max_length=150, unique=True, verbose_name="视频名"),
                ),
                ("cover_url", models.URLField(max_length=500, verbose_name="封面url")),
                ("video_url", models.URLField(max_length=500, verbose_name="视频url")),
                ("duration", models.DurationField(verbose_name="视频时长")),
                (
                    "profile",
                    models.TextField(blank=True, null=True, verbose_name="视频简介"),
                ),
            ],
            options={
                "verbose_name": "视频",
                "verbose_name_plural": "视频",
            },
        ),
    ]
