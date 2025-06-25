"""Game objects to create PyGame based games."""

import warnings
import sys
import pygame
from pygame.sprite import Group
from videogame.scene import Ship
from videogame.scene import Background
from videogame.scene import EnemySpawner
from videogame.scene import TitleScene
from videogame import rgbcolors

def display_info():
    """Print out information about the display driver and video information."""
    print(f'The display is using the "{pygame.display.get_driver()}" driver.')
    print("Video Info:")
    print(pygame.display.Info())


# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


# pylint: disable=too-few-public-methods
class VideoGame:
    """Base class for creating PyGame games."""

    def __init__(
        self,
        window_width=1100,
        window_height=1300,
        window_title="Galaga",
    ):
        """Initialize a new game with the given window size and window title."""
        pygame.init()
        self._window_size = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)
        self._title = window_title
        pygame.display.set_caption(self._title)
        self._game_is_over = False
        if not pygame.font:
            warnings.warn("Fonts disabled.", RuntimeWarning)
        if not pygame.mixer:
            warnings.warn("Sound disabled.", RuntimeWarning)
        else:
            pygame.mixer.init()
        self._scene_manager = None

        # title screen setup
        self.scene = TitleScene(self._screen, "Galaga", rgbcolors.green )
        self.scene.start_scene()

    # main run loop
    def run(self):
        run = True
        while run:
            self._clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            if hasattr(self.scene, "handle_event"):
                next_scene = self.scene.handle_event(event)
                if next_scene == "START_1P":
                    self.scene.end_scene()
                    from videogame.scene import GameScene
                    self.scene = GameScene(self._screen)
                    self.scene.start_scene()

            # update current scene
            self.scene.update_scene()

            # clear screen
            self._screen.fill(rgbcolors.black)

            # draw current scene
            self.scene.draw()

            # update display
            pygame.display.update()


        raise NotImplementedError


# pylint: enable=too-few-public-methods
