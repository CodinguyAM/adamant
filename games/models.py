from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):   

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)

    # Preferences

    primary_color = models.CharField(max_length = 7, default = '#03A5FC') # Color for primary player - first player or self
    secondary_color = models.CharField(max_length = 7, default = '#FC0B03') # Color for secondary player - second player
    tertiary_color = models.CharField(max_length = 7, default = '#FAD102') # Color for tertiary player - third player
    quaternary_color = models.CharField(max_length = 7, default = '#02FABC') # Color for quaternary player - fourth player

    faint_primary_color = models.CharField(max_length = 7, default = '#ABCDEF') # Color for primary elements
    faint_secondary_color = models.CharField(max_length = 7, default = '#D6C1C1') # Color for secondary elements

    superfaint_primary_color = models.CharField(max_length = 7, default = '#D5E6F7') # Color for primary element backgrounds
    superfaint_secondary_color = models.CharField(max_length = 7, default = '#EBE0E0') # Color for secondary element backgrounds

    background_color = models.CharField(max_length = 7, default = '#FFFFFF') # Color of background

    affrm_color = models.CharField(max_length = 7, default = '#639919') # Color of affirmative messages, like Wordle green
    afrm2_color = models.CharField(max_length = 7, default = '#F5E911') # Color of semi-affirmative messages, like Wordle yellow
    neutral_color = models.CharField(max_length = 7, default = '#777777') # Color of neutral messages, like Wordle grey
    negative_color = models.CharField(max_length = 7, default = '#C94040') # Color of negative messages.

    font_family = models.CharField(max_length = 30, default = 'Helvetica') # Main font family.
    heading_font = models.CharField(max_length = 30, default = 'Helvetica') # Font family for headings.

    about = models.CharField(max_length = 300, default = 'A user of Adamant Games.') # About.

class Game(models.Model):

    flattened = models.TextField() # A somewhat hacky way of storing Python data in SQL. flattened consists of a strigified version of logic.deflate_game's output. (logic.build_game can be used to re-inflate the game.).
    nplayers = models.IntegerField()
    extra_data = models.TextField() # See comment on flattened.
    ready = models.IntegerField()

    game_tli = models.CharField(max_length = 3, default='ZZZ') # Game TLI (three-letter identifier)
    code = models.CharField(max_length = 11, unique = True)
    completed = models.BooleanField()

    public_join = models.BooleanField(default = True)
    public_view = models.BooleanField(default = True)

    nmoves = models.IntegerField()

    made_by = models.ForeignKey(User, related_name='created', on_delete=models.CASCADE)

class Player(models.Model):
    # Should really be called a playership - represents a user as a player of a game, noting that user's player index.
    
    user = models.ForeignKey(User, related_name='games', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='users', on_delete=models.CASCADE)

    player_index = models.IntegerField()

    hashed_id = models.BigIntegerField()
