# Generated by Django 4.1.3 on 2022-11-12 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChessGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, help_text='Starting date of the game', null=True)),
                ('white_elo', models.IntegerField(blank=True, null=True)),
                ('black_elo', models.IntegerField(blank=True, null=True)),
                ('hashcode', models.CharField(help_text='A hash code of the moves in the game', max_length=8)),
                ('total_ply_count', models.IntegerField()),
                ('imported_pgn', models.TextField(help_text='The imported PGN of the game')),
                ('processed_pgn', models.TextField(blank=True, help_text='The PGN after the annotator has visited it', null=True)),
                ('black', models.ForeignKey(help_text='Player of the black pieces', on_delete=django.db.models.deletion.CASCADE, related_name='black_games', to='players.chessplayer')),
                ('event', models.ForeignKey(blank=True, help_text='The tournament or match event', null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.chessevent')),
                ('round', models.ForeignKey(blank=True, help_text='The round of the tournament', null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.chessround')),
                ('white', models.ForeignKey(help_text='Player of the white pieces', on_delete=django.db.models.deletion.CASCADE, related_name='white_games', to='players.chessplayer')),
                ('winner', models.ForeignKey(blank=True, help_text='Winner of the game; None for draw', null=True, on_delete=django.db.models.deletion.CASCADE, to='players.chessplayer')),
            ],
        ),
    ]
