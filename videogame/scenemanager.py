"""A class to manage transitions from one scene to another."""


class SceneManager:
    """A scene manager that works like a list. Poor quality."""

    def __init__(self, scenes_list=None):
        """Initialize a scene manager with a given list of scenes."""
        self._scenes = scenes_list

    def __iter__(self):
        """Return an iterator to move through the scenes."""
        return iter(self._scenes)

    def add(self, scene):
        """Add an additional scene to the scene list."""
        self._scenes.append(scene)
