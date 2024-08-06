# Generated by Django 5.0.7 on 2024-07-26 16:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CasualGameListView',
            fields=[
                ('game_id', models.IntegerField(primary_key=True, serialize=False)),
                ('mode', models.PositiveSmallIntegerField()),
                ('status', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'casual_game_list_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CasualGameView',
            fields=[
                ('game_id', models.IntegerField(primary_key=True, serialize=False)),
                ('mode', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'casual_game_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GameRecordView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.IntegerField()),
                ('mode', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('started_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'game_record_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RankGameView',
            fields=[
                ('game_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'rank_game_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.PositiveSmallIntegerField(choices=[(0, 'casual_1vs1'), (1, 'casual_tournament'), (2, 'rank')])),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'AVAILABLE_WAITING'), (1, 'FULL_WAITING'), (2, 'IN_GAME'), (3, 'FINISHED'), (4, 'DELETED')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'games',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1_score', models.IntegerField()),
                ('player2_score', models.IntegerField()),
                ('player3_score', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_id', to='games.game')),
            ],
            options={
                'db_table': 'results',
            },
        ),
        migrations.AddField(
            model_name='game',
            name='match1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='result_match1', to='games.result'),
        ),
        migrations.AddField(
            model_name='game',
            name='match2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='result_match2', to='games.result'),
        ),
        migrations.AddField(
            model_name='game',
            name='match3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='result_match3', to='games.result'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='이메일 주소')),
                ('nickname', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('rating', models.PositiveIntegerField(default=0)),
                ('avatar', models.ImageField(null=True, upload_to='avatar/')),
                ('verification_code', models.CharField(blank=True, max_length=6, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('custom_1vs1_wins', models.IntegerField(default=0)),
                ('custom_tournament_wins', models.IntegerField(default=0)),
                ('rank_wins', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='custom_user_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_permissions_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='result',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner_id', to='games.user'),
        ),
        migrations.AddField(
            model_name='game',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.user'),
        ),
        migrations.AddField(
            model_name='game',
            name='player1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player1_id', to='games.user'),
        ),
        migrations.AddField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player2_id', to='games.user'),
        ),
        migrations.AddField(
            model_name='game',
            name='player3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player3_id', to='games.user'),
        ),
    ]
