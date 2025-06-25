
# Galaga!

In this exercise, we shall write a [Galaga](https://en.wikipedia.org/wiki/Galaga) style game. Galaga was first released in 1981 as a sequel to Galaxian. It is a fixed shooter with the player's character at the bottom of the screen facing off against a grid of non-player enemies which fire at the player and dive at the enemy. Galaga is one of the most memorable games from the golden age of arcade video games.

The game play occurs on a single screen or scene. The screen is oriented in a portrait orientation which is traditional for an arcade video game. The player's character, a space craft, is at the bottom of the screen and the player may move to the left or to the right. The player's character faces off against an armada of alien space craft.

Galaga is famous for enemies' dramatic entrance. The enemies swoop in from off screen along paths that curve and circle on screen then disappear off screen. The aliens return on screen and create a grid-like pattern at the top of the screen facing off against the player. Regularly, groups of enemies dive towards the player and shoot.

The goal of the game is to score the highest score possible before losing all three lives. If the player defeats all the enemies in a given scene, then the scene is completed and a new scene begins with new enemies.

If you have never played Pong before, please visit the [Internet Aracade](https://archive.org/details/internetarcade)  at the [Internet Archive](https://archive.org/) and try [Galaga '88](https://archive.org/details/arcade_galaga88) or the original Galaga in [Namco Classic Collection Vol. 1](https://archive.org/details/arcade_ncv1).

(To insert _coins_, press _5_. To start a game after inserting a _coin_, press _1_. To shoot, press _left_control_. The _tab_ key will get you into a setup  menu which will show you what keys are mapped to which controls. The _esc_ key goes back when in the setup menu.)

Playing the game will give you an appreciation for what the game mechanics are and how you can take the Galaga concept and make it your own.

Additionally, you may find watching a video capture of gameplay informative. Slow down the video playback so you can analyze how the enemies move and behave.

Remember, this assignment is an individual assignment where you are creating your own Galaga game clone. _Please do not follow an online tutorial or duplicate an existing Galaga project._

Our Galaga game shall have the following rules or requirements:

* The game must be written in Python using Pygame.

* The game must use object oriented design using the same principles from previous programming assignments. Projects which disregard this requirement will not be graded.

* The game must be graphical (not a text-based or text console game).

* The game must at least be a one player game versus an armada of enemy characters controlled by an AI.

* Each game-play scene must have a soundtrack. You are urged to have a soundtrack throughout the entire game.

* Each game-play scene must contain a minimum of 20 enemies and no more than 80 enemies. A game-play scene is considered a single level. Killing all the enemies in a level transitions the player to another level which is more challenging. The challenges that confront the player are left to your discretion. Enemies may be of any size and have any behavior.

* The game may be controlled from the keyboard, mouse, or joystick. If joystick or mouse controls exist, then there must be an option to fallback to a keyboard.

* The player moves along a line at the bottom of the screen. This is the player's baseline of movement. The player character may not go off screen.

* The player is given three _lives_. A life is lost when the player's character is shot or collides with an enemy. A player gains an additional life every 10,000 points. When a player's life is lost, a sound effect is played and the game pauses for no less than 1 second before spawning the next player. The player may be respawned anywhere along the player's baseline of movement. Although not a requirement, playing an animation where the player's character perishes may take the place of the game pause required above.

* The player's character shoots upwards towards the aliens. Whenever a shot is fired, a sound effect is played as an auditory cue that a shot was fired. When a bullet from the player's character intersects with an alien an alien perishes. The bullet perishes along with the alien, meaning a bullet may only strike one target. A sound effect is played when the alien perishes. When an alien perishes, it is not required but you are strongly urged to animate the demise of the alien.

* Each level begins with the aliens parading into the scene. During the parade, the player may fire upon the aliens and the aliens may fire upon the player. Once the parade completes, the aliens take up a position in a grid-like formation at the top of the display. Groups or individual aliens attack the player by diving towards the player's position. The diving aliens may also fire while diving.

* When the aliens shoot at the player, there is a sound effect that is played. The sound effect for a shot fired from a stationary position is different than the sound effect fired while the alien is parading or diving.

* The objective of the game is to score as many points by completing as many levels as possible. Successfully shooting an enemy while stationary is 50 points. Successfully shooting an enemy while it is flying is 100-200 points, at your discretion.

* The game's leaderboard shall contain the top 3 scores of all time. The scores must be stored in a file that can be loaded anytime during game play. You are urged to use a Python Pickle.

* Galaga has many sophisticated game mechanics. You do not need to include them all. The key mechanics to include are spawning a new life when the player's character perishes, having the aliens parade on to the screen, the aliens form a grid after the parade, the aliens periodically attack the player, the completion of one game-level leads swiftly into another game-level which is more challenging.

* The program begins by presenting a title scene. The scene shows the title of the game and explains the controls of the game. To advance to the next scene, any key may be pressed. The next scene is the level 1 of the game. When a level is completed, the game moves on to the next level. Should a player loose all their lives, a game over scene is shown. If the player's score is a high score, then the player can either enter their name/handle/initials or the game can generate an identifier (the date and time) to use in the leaderboard. Pressing a key from the game over scene transitions to a leaderboard display. Pressing any key again transitions back to the title screen.

* The player's score shall be shown along the top edge. 

* If the player has lives, the game continues until all lives are lost. There is no maximum number of levels.

* Additional scenes may be added at your discretion.

* All code related to the Galaga game must be in a Python module named `videogame`.

* The main function must be called from the file named `galaga.py`. The file `galaga.py` is not in the `videogame` module.

* You must conform to [PEP-8](https://www.python.org/dev/peps/pep-0008/). Use [pylint](https://www.pylint.org/) and [pycodestyle](https://pypi.org/project/pycodestyle/) to conform to [PEP-8](https://www.python.org/dev/peps/pep-0008/).

Start from scratch. Make your own game. Make something you'll be proud to share with family and friends.

# Rubric

* Functionality (24 points): Your submission shall be assessed for the appropriate constructs and strategies to address the exercise. A program the passes the instructor's tests completely receives full marks. A program that partially passes the instructors tests receives partial-marks. A program that fails the majority or all the tests receives no marks.

* Format & Readability (16 point): Your submission shall be assessed by checking whether your code passess the style and format check, as well as how well it follows the proper naming conventions, and internal documentation guidelines. Git log messages are an integral part of how readable your project is.
