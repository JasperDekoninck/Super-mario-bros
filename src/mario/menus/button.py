import pygame
import numpy as np
pygame.init()


class Button:
    class Button:
        def __init__(self, pos, content, hover_over_content=None, center_pos=False):
            """
            Initializes a Button object.

            Args:
                pos (tuple): The position of the button (x, y).
                content (pygame.Surface): The content to be displayed on the button.
                hover_over_content (pygame.Surface, optional): The content to be displayed when the button is hovered over. Defaults to None.
                center_pos (bool, optional): Whether to center the button position. Defaults to False.
            """
            self.pos = pos
            self.mid_pos = None
            self.content = content
            self.hover_over_content = hover_over_content
            self.center_pos = center_pos
            self.size = self.content.get_size()

            if center_pos:
                self.pos = list(pos)
                self.mid_pos = pos[:]
                self.pos[0] = self.pos[0] - self.size[0] // 2
                self.pos[1] = self.pos[1] - self.size[1] // 2

            self.selected = False

    def set_content(self, new_content):
        """
        Sets the content of the button.

        Parameters:
        - new_content: The new content to be set.

        Returns:
        None
        """
        self.content = new_content
        self.size = self.content.get_size()
        if self.center_pos:
            self.pos[0] = self.mid_pos[0] - self.size[0] // 2
            self.pos[1] = self.mid_pos[1] - self.size[1] // 2

    def is_selected(self, pos):
        """
        Check if the button is selected based on the given position.

        Args:
            pos (tuple): The position to check against.

        Returns:
            bool: True if the button is selected, False otherwise.
        """
        return self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and \
               self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]

    def update_selected(self, pos):
        """
        Updates the selected state of the button based on the given position.

        Args:
            pos (tuple): The position (x, y) to check for selection.

        Returns:
            None
        """
        self.selected = self.is_selected(pos)

    def render(self, screen, camera_pos=np.zeros(2)):
        """
        Renders the button on the screen.

        Args:
            screen: The surface to render the button on.
            camera_pos: The position of the camera in the game world.

        Returns:
            None
        """
        if not self.selected or self.hover_over_content is None:
            position = (self.pos[0] - camera_pos[0].astype(np.int32), self.pos[1] - camera_pos[1].astype(np.int32))
            screen.blit(self.content, position)
        else:
            screen.blit(self.hover_over_content, self.pos - camera_pos.astype(np.int32))


class TextButton(Button):
    def __init__(self, pos, message, font, color_not_selected, color_selected=None, center_pos=False):
        """
        Initializes a TextButton object.

        Args:
            pos (tuple): The position of the button (x, y).
            message (str): The text to be displayed on the button.
            font (pygame.font.Font): The font used for rendering the text.
            color_not_selected (tuple): The color of the text when the button is not selected (r, g, b).
            color_selected (tuple, optional): The color of the text when the button is selected (r, g, b). Defaults to None.
            center_pos (bool, optional): Whether to center the button position. Defaults to False.
        """
        content = font.render(message, True, color_not_selected)
        hover_content = None
        if color_selected is not None:
            hover_content = font.render(message, True, color_selected)

        self.font = font
        self.message = message
        self.color = color_not_selected
        self.color_selected = color_selected
        super(TextButton, self).__init__(pos, content, hover_content, center_pos=center_pos)

    def set_text(self, new_text):
        """
        Set the text of the button.

        Parameters:
        - new_text (str): The new text to be displayed on the button.

        Returns:
        None
        """
        new_content = self.font.render(new_text, True, self.color)
        self.message = new_text
        self.set_content(new_content)
        if self.color_selected is not None:
            self.hover_over_content = self.font.render(new_text, True, self.color_selected)


class ImageButton(Button):
    def __init__(self, pos, content, description):
        """
        Initialize an ImageButton object.

        Args:
            pos (tuple): The position of the button on the screen.
            content (str): The content of the button.
            description (str): The description of the button.

        Returns:
            None
        """
        super(ImageButton, self).__init__(pos, content)
        self.description = description
