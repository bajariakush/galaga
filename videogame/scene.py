"""Scene objects for making games with PyGame."""

import pygame
import random
import math
from pygame.sprite import Sprite, Group
from videogame import rgbcolors


# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html

pygame.init()


class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(self, screen, background_color, screen_flags=None,
                 soundtrack=None):
        """Scene initializer"""
        self._screen = screen
        if not screen_flags:
            screen_flags = pygame.SCALED
        self._background = pygame.Surface(self._screen.get_size(),
                                          flags=screen_flags)
        self._background.fill(background_color)
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack
        self._render_updates = None

    def draw(self):
        """Draw the scene."""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Process a game event by the scene."""
        # This should be commented out or removed since it
        # generates a lot of noise.
        # print(str(event))
        if event.type == pygame.QUIT:
            print("Good Bye!")
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Bye bye!")
            self._is_valid = False

    def is_valid(self):
        """Is the scene valid? A valid scene can be used to play a scene."""
        return self._is_valid

    def render_updates(self):
        """Render all sprite updates."""

    def update_scene(self):
        """Update the scene state."""

    def start_scene(self):
        """Start the scene."""
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.35)
            except pygame.error as pygame_error:
                print("\n".join(pygame_error.args))
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(loops=-1, fade_ms=500)

    def end_scene(self):
        """End the scene."""
        if self._soundtrack and pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()

    def frame_rate(self):
        """Return the frame rate the scene desires."""
        return self._frame_rate


class PressAnyKeyToExitScene(Scene):
    """Empty scene where it will invalidate when a key is pressed."""

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self._is_valid = False


class TitleScene(Scene):
    """Title scene for the game"""

    def __init__(
        self, screen, message, color, size=72, background_color=rgbcolors.black
    ):
        """Initialize the title scene"""
        soundtrack = "assets/sounds/theme.mp3"
        super().__init__(screen, background_color, soundtrack=soundtrack)
        self._message = message
        self._color = color
        self._size = size
        self._blinker_timer = 0
        self._blink_visible = True

        # background object setup
        self.background = Background()
        self.background_group = pygame.sprite.Group()
        self.background_group.add(self.background)

    def update_scene(self):
        """Update the blinking arrow"""
        self._blinker_timer += 1
        if self._blinker_timer >= 30:
            self._blink_visible = not self._blink_visible
            self._blinker_timer = 0
        self.background_group.update()

    def draw(self):
        """Draw the title scene with blinking arrow"""
        super().draw()
        self.background_group.draw(self._screen)
        title_font = pygame.font.SysFont("pub.ttf", self._size * 2)
        option_font = pygame.font.SysFont("pub.ttf", int(self._size * 0.8))
        hint_font = pygame.font.SysFont("pub.ttf", int(self._size * 0.4))

        # Render title and "1 Player" text
        title_surface = title_font.render(self._message, True, self._color)
        option_surface = option_font.render("1 PLAYER", True, rgbcolors.white)
        hint_surface = hint_font.render("(Press Enter to Start)",
                                        True, rgbcolors.white)

        # Position them
        title_rect = title_surface.get_rect(
            center=(self._screen.get_width() // 2, self._screen.get_height()
                    // 2 - 300)
        )
        option_rect = option_surface.get_rect(
            center=(self._screen.get_width() // 2, self._screen.get_height()
                    // 2 + 40)
        )
        hint_rect = hint_surface.get_rect(
            center=(self._screen.get_width() // 2, self._screen.get_height()
                    // 2 + 100)
        )

        self._screen.blit(title_surface, title_rect)
        self._screen.blit(option_surface, option_rect)
        self._screen.blit(hint_surface, hint_rect)

        # Blinking arrow
        if self._blink_visible:
            arrow_font = pygame.font.SysFont("pub.ttf", int(self._size * 0.5))
            arrow_surface = arrow_font.render(">", True, rgbcolors.white)
            arrow_rect = arrow_surface.get_rect(
                midright=(option_rect.left - 20, option_rect.centery - 3.5)
            )
            self._screen.blit(arrow_surface, arrow_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_KP1
                or event.key == pygame.K_1
                or event.key == pygame.K_RETURN
            ):
                return "START_1P"
        return None


class GameScene(Scene):
    player_death_sound = pygame.mixer.Sound("assets/sounds/player_death.mp3")
    """Game scene for the game"""

    def __init__(self, screen):
        """Move game setup here"""
        soundtrack = "assets/sounds/gameplay.mp3"
        super().__init__(
            screen, background_color=rgbcolors.black, soundtrack=soundtrack
        )
        self._screen = screen
        self.lives = 3
        self.lives_group = pygame.sprite.Group()
        self.respawn_timer = 0
        self.is_respawning = False
        self.intro_timer = 0
        self.start_descent = False
        self.intro_tar_pos = (1100 // 2, 1300 - 100)
        self.intro_moving = False
        self.player_control_enable = True
        self.enemy_spawner = EnemySpawner()
        self.enemy_spawner.wave_size = 40
        self.enemy_spawner.spawn_wave()
        self.score = 0
        self.level = 1
        self.speed_multiplier = 1.0
        self.extra_life = 10000
        self.game_over = False

        # create ship to right of screen
        self.intro_ships = pygame.sprite.Group()
        self.intro_done = False

        # background object setup
        self.background = Background()
        self.background_group = pygame.sprite.Group()
        self.background_group.add(self.background)

        # intro ships setup (3 in a row, leftmost descends)
        self.intro_ships = pygame.sprite.Group()
        start_x = 950
        start_y = 650
        spacing = 90

        for i in range(3):
            ship = Ship()
            ship.rect.centery = start_y
            ship.rect.centerx = start_x + (i - 1) * spacing
            ship.vel_y = 0

            if i == 0:
                self.intro_left_ship = ship
            self.lives_group.add(ship)
            self.intro_ships.add(ship)

        # store the leftmost ship as the player (to control after intro)
        self.player = list(self.intro_ships)[0]
        self.sprite_group = pygame.sprite.Group()

        # enemy spawner setup
        self.intro_done = False

        # handle game over
        if self.lives > 0:
            self.is_respawning = True
            self.respawn_timer = 180
        else:
            self.game_over = True

    def handle_event(self, event):
        # handle game over
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.__init__(self._screen)  # reset the game scene
            return None

        if not self.player_control_enable:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.player.vel_x = -self.player.speed
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.vel_x = +self.player.speed
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.player.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.player.vel_x = 0
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.vel_x = 0

    def player_death(self):
        GameScene.player_death_sound.play()
        self.lives -= 1
        self.level += 1
        # remove one of the extra life icons
        if self.lives_group:
            ship_lost = self.lives_group.sprites()[-1]
            self.lives_group.remove(ship_lost)

        # remove dead player ship from sprite group
        if self.player in self.sprite_group:
            self.sprite_group.remove(self.player)

        # reset intro ship
        if self.player in self.intro_ships:
            self.intro_ships.remove(self.player)

        # reset lives group
        if self.player in self.lives_group:
            self.lives_group.remove(self.player)

        if self.lives > 0:
            self.is_respawning = True
            self.respawn_timer = 180
        else:
            self.game_over = True
            print("Game Over!")

    def update_scene(self):
        """Update the game scene"""
        self.background_group.update()
        if not self.is_respawning:
            self.enemy_spawner.enemy_group.update()
            self.enemy_spawner.update()
            self.sprite_group.update()
            self.lives_group.update()
            self.intro_ships.update()
            self.player.bullets.update()

        # loop for intro ships
        if not self.intro_done:
            self.intro_timer += 1

        # start descent of player ship after 3 seconds
        if self.intro_timer >= 180 and not self.start_descent:
            self.start_descent = True
            self.player.vel_y = 2

        # move player ship to the bottom middle
        self.intro_timer += 1
        if self.intro_timer == 180:
            self.intro_moving = True

        if not self.intro_done and self.intro_moving:
            self.intro_left_ship.rect.y += self.intro_left_ship.vel_y
        if self.intro_left_ship.rect.y >= 1200:
            self.intro_left_ship.rect.y = 1200
            self.intro_left_ship.vel_y = 0
            self.intro_done = True
            self.player_control_enable = True

        if self.intro_moving:
            ship = self.intro_left_ship
            target_x, target_y = self.intro_tar_pos
            dx = target_x - ship.rect.centerx
            dy = target_y - ship.rect.centery
            distance = (dx**2 + dy**2) ** 0.5

            speed = 4
            if distance > speed:
                ship.rect.centerx += int(dx / distance * speed)
                ship.rect.centery += int(dy / distance * speed)
            else:
                ship.rect.center = (target_x, target_y)
                self.intro_moving = False
                self.intro_done = True
                self.player = ship
                self.sprite_group.add(ship)
                self.player.vel_y = 0
                self.player_control_enable = True
                self.intro_ships.remove(ship)

        # handle scoring and extra life
        hits = pygame.sprite.groupcollide(
            self.enemy_spawner.enemy_group, self.player.bullets, True, True
        )
        for enemy in hits:
            if getattr(enemy, "state", "") == "formation":
                self.score += 50
            elif getattr(enemy, "state", "") == "diving":
                self.score += 150  # or random.randint(100, 200) for variety
            EnemyPath.hit_sound.play()
            if self.score >= self.extra_life:
                self.lives += 1
                self.extra_life += 10000

        # Periodically trigger a dive
        dive_chance = 0.01 + 0.002 * (self.level - 1)
        if self.intro_done and random.random() < dive_chance:
            formation_enemies = [
                e
                for e in self.enemy_spawner.enemy_group
                if getattr(e, "state", "") == "formation"
            ]
            if formation_enemies:
                diver = random.choice(formation_enemies)
                diver.state = "diving"
                diver.dive_path = self.create_dive_path(
                    diver.rect.center, self.player.rect.center,
                    diver.formation_pos
                )
                diver.dive_point = 0

        # check for collision
        if self.intro_done and pygame.sprite.spritecollideany(
            self.player, self.enemy_spawner.enemy_group
        ):
            self.player_death()
            # clear enemies on player death
            self.enemy_spawner.enemy_group.empty()

            self.enemy_spawner.wave_size = min(
                self.enemy_spawner.wave_size + 15, 80
            )  # increase difficulty
            self.enemy_spawner.spawn_wave(self.speed_multiplier)
            # respawn enemies

            # wait 3 seconds
            self.is_respawning = True
            self.respawn_timer = 180

        if self.is_respawning:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.is_respawning = False
                self.enemy_spawner.spawn_wave()

            # reset player position
            if self.player in self.sprite_group:
                self.sprite_group.remove(self.player)
            if self.player in self.intro_ships:
                self.intro_ships.remove(self.player)

            # prepare new player ship
            new_player = Ship()
            new_player.rect.centerx = 1100 // 2
            new_player.rect.y = 1200
            self.player = new_player
            self.sprite_group.add(self.player)
            self.player.bullets.empty()

        # add level progression
        if (
            self.intro_done
            and not self.is_respawning
            and len(self.enemy_spawner.enemy_group) == 0
        ):
            self.level += 1
            self.enemy_spawner.wave_size = min(40 + self.level * 5, 80)
            self.speed_multiplier = (
                1.0 + (self.level - 1) * 0.15
            )  # Increase speed by 15% each level
            self.is_respawning = True
            self.respawn_timer = 120

        if self.is_respawning:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.is_respawning = False
                self.enemy_spawner.spawn_wave()

        # handle game over
        if self.game_over:
            return

    def create_dive_path(self, start, target, end):
        # Simple dive: go toward player, then back to formation
        path = []
        mid_x = (start[0] + target[0]) // 2
        mid_y = (start[1] + target[1]) // 2 + 200  # curve down
        path.append((mid_x, mid_y))
        path.append(target)
        path.append((mid_x, mid_y))
        path.append(end)
        return path

    def draw(self):
        """draw game scene"""
        self.background_group.draw(self._screen)
        if not self.intro_done:
            self.intro_ships.draw(self._screen)
        else:
            if not self.is_respawning:
                self.sprite_group.draw(self._screen)
                self.player.bullets.draw(self._screen)
                self.enemy_spawner.enemy_group.draw(self._screen)
            self.lives_group.draw(self._screen)

        # draw score and level
        font = pygame.font.SysFont("pub.ttf", 36)
        score_surface = font.render(f"Score: {self.score}",
                                    True, rgbcolors.orange)
        level_surface = font.render(f"Level: {self.level}",
                                    True, rgbcolors.white)
        self._screen.blit(score_surface, (20, 20))
        self._screen.blit(level_surface, (20, 60))

        # handle game over
        if self.game_over:
            game_over_font = pygame.font.SysFont("pub.ttf", 72)
            game_over_surface = game_over_font.render("GAME OVER",
                                                      True, rgbcolors.red)
            game_over_rect = game_over_surface.get_rect(
                center=(self._screen.get_width() // 2,
                        self._screen.get_height() // 2)
            )
            self._screen.blit(game_over_surface, game_over_rect)

            restart_font = pygame.font.SysFont("pub.ttf", 36)
            restart_surface = restart_font.render(
                "Press R to Restart", True, rgbcolors.white
            )
            restart_rect = restart_surface.get_rect(
                center=(
                    self._screen.get_width() // 2,
                    self._screen.get_height() // 2 + 50,
                )
            )
            self._screen.blit(restart_surface, restart_rect)


class Ship(pygame.sprite.Sprite):
    shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.mp3")
    """Ship spirite for the game"""

    def __init__(self):
        """Initialize the ship sprite"""
        super(Ship, self).__init__()
        self.image = pygame.image.load("assets/images/player_ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = 1100 // 2
        self.rect.y = 1300 - self.rect.height
        self.bullets = pygame.sprite.Group()
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5

    def update(self):
        """update ship sprite"""
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.rect.y <= 0:
                self.bullets.remove(bullet)
        self.rect.x += self.vel_x
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x >= 1100 - self.rect.width:
            self.rect.x = 1100 - self.rect.width
        self.rect.y += self.vel_y

    def shoot(self):
        """shooting bullets from the ship"""
        if len(self.bullets) == 0:
            new_bullet = Bullet()
            new_bullet.rect.x = self.rect.x + (self.rect.width // 2) - 3
            new_bullet.rect.y = self.rect.y
            self.bullets.add(new_bullet)
            Ship.shoot_sound.play()


class Star(pygame.sprite.Sprite):
    """Star sprite for the game"""

    def __init__(self):
        """Initialize the star sprite"""
        super(Star, self).__init__()
        self.width = random.randrange(2, 4)
        self.height = self.width
        self.size = (self.width, self.height)
        self.image = pygame.Surface(self.size)
        self.color = rgbcolors.random_color()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 1100)
        self.vel_x = 0
        self.vel_y = random.randrange(1, 20)

    def update(self):
        """update star sprite"""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y


class Background(pygame.sprite.Sprite):
    """Background sprite for the game"""

    def __init__(self):
        """Initialize the background sprite"""
        super(Background, self).__init__()
        self.image = pygame.Surface((1100, 1300))
        self.color = rgbcolors.black
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.stars = pygame.sprite.Group()
        self.timer = random.randrange(1, 10)

    def update(self):
        """update background sprite"""
        for star in self.stars:
            if star.rect.y >= 1300:
                self.stars.remove(star)
        self.stars.update()
        if self.timer == 0:
            new_star = Star()
            self.stars.add(new_star)
            self.timer = random.randrange(1, 10)
        self.image.fill(self.color)
        self.stars.draw(self.image)
        self.timer -= 1


class Bullet(pygame.sprite.Sprite):
    """Bullet sprite for the game"""

    def __init__(self):
        """Initialize the bullet sprite"""
        super(Bullet, self).__init__()
        self.width = 4
        self.height = self.width
        self.size = (self.width, self.height)
        self.image = pygame.Surface(self.size)
        self.color = rgbcolors.white
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = -8

    def update(self):
        """update the bullet sprite"""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y


class Enemy(pygame.sprite.Sprite):
    """Enemy sprite for the game"""

    def __init__(self):
        """Initialize the enemy sprite"""
        super(Enemy, self).__init__()
        self.image = pygame.image.load("assets/images/enemy_ship1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 1100 - self.rect.width)
        self.rect.y = -self.rect.height
        self.vel_x = 0
        self.vel_y = random.randrange(2, 5)

    def update(self):
        """update the enemy sprite"""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y


class EnemySpawner:
    """Enemy spawner for the game"""

    def __init__(self):
        """Initialize the enemy spawner"""
        self.enemy_group = pygame.sprite.Group()
        self.wave_size = 40
        self.formation_y = 200
        self.formation_spacing = 60

    def spawn_wave(self, speed_multiplier=1.0):
        """sspawn a wave of enemies"""
        max_cols = 5
        rows = 4
        cols = min(max_cols, (self.wave_size + rows - 1) // rows)

        start_y = 100
        spacing_x = 150
        spacing_y = 90

        # calculate total width of the formation for centering
        formation_width = (cols - 1) * spacing_x
        start_x = (1100 - formation_width) // 2

        count = 0
        for row in range(rows):
            for col in range(cols):
                if count >= self.wave_size:
                    break
                formation_x = start_x + col * spacing_x
                formation_y = start_y + row * spacing_y
                formation_pos = (formation_x, formation_y)
                new_enemy = EnemyPath(
                    start_x=formation_x,
                    start_y=-70,
                    flip=False,
                    formation_pos=formation_pos,
                    speed_multiplier=speed_multiplier,
                )
                self.enemy_group.add(new_enemy)
                count += 1

    def update(self):
        """update the enemy spawner"""
        self.enemy_group.update()


class EnemyPath(pygame.sprite.Sprite):
    hit_sound = pygame.mixer.Sound("assets/sounds/explosion.mp3")
    """Enemy path sprite for the game"""

    def __init__(
        self,
        start_x,
        start_y,
        flip=False,
        formation_pos=(550, 200),
        speed_multiplier=1.0,
    ):
        """Initialize the enemy path sprite"""
        super().__init__()
        self.image = pygame.image.load("assets/images/enemy_ship1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.path = self.create_arc_path(start_x, start_y, flip, formation_pos)
        self.current_point = 0
        self.rect.center = self.path[0]
        self.speed = 4
        self.formation_pos = formation_pos
        self.state = "entering"
        self.dive_path = []
        self.dive_point = 0
        self.speed = 4 * speed_multiplier

    def create_arc_path(self, start_x, start_y, flip, formation_pos):
        """create a loop path for the enemy"""
        path = []
        lopps = 1.5
        points_per_loop = 40
        total_points = int(lopps * points_per_loop)
        spiral_radius = 180
        vertical_drop = 350

        center_x = start_x
        center_y = start_y + 100

        for i in range(total_points):
            angle = (i / points_per_loop) * 2 * math.pi
            if flip:
                angle = -angle  # Reverse spiral for right side
            radius = spiral_radius * (1 - i / total_points)  # Spiral inward
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle) + (vertical_drop * i / total_points)
            path.append((int(x), int(y)))

        final_x, final_y = path[-1]
        steps = 40
        dx = (formation_pos[0] - final_x) / steps
        dy = (formation_pos[1] - final_y) / steps
        for i in range(steps):
            path.append((int(final_x + dx * i), int(final_y + dy * i)))

        return path

    def update(self):
        if self.state == "entering":
            if self.current_point < len(self.path) - 1:
                target_x, target_y = self.path[self.current_point]
                dx = target_x - self.rect.centerx
                dy = target_y - self.rect.centery
                distance = (dx**2 + dy**2) ** 0.5
                if distance < self.speed:
                    self.rect.center = (target_x, target_y)
                    self.current_point += 1
                else:
                    self.rect.centerx += dx / distance * self.speed
                    self.rect.centery += dy / distance * self.speed
            else:
                self.state = "formation"
                self.rect.center = self.formation_pos
        elif self.state == "formation":
            # stay in formation
            self.rect.center = self.formation_pos
        elif self.state == "diving":
            # follow dive path
            if self.dive_point < len(self.dive_path):
                target_x, target_y = self.dive_path[self.dive_point]
                dx = target_x - self.rect.centerx
                dy = target_y - self.rect.centery
                distance = (dx**2 + dy**2) ** 0.5
                if distance < self.speed:
                    self.rect.center = (target_x, target_y)
                    self.dive_point += 1
                else:
                    self.rect.centerx += dx / distance * self.speed
                    self.rect.centery += dy / distance * self.speed
            else:
                # return to formation
                self.state = "formation"
                self.rect.center = self.formation_pos
