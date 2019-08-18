import pygame
import numpy as np
pygame.init()


class Button:
    def __init__(self, pos, content, hover_over_content=None, center_pos=False):
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
        self.content = new_content
        self.size = self.content.get_size()
        if self.center_pos:
            self.pos[0] = self.mid_pos[0] - self.size[0] // 2
            self.pos[1] = self.mid_pos[1] - self.size[1] // 2

    def is_selected(self, pos):
        return self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and \
               self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]

    def update_selected(self, pos):
        self.selected = self.is_selected(pos)

    def render(self, screen, camera_pos=np.zeros(2)):
        if not self.selected or self.hover_over_content is None:
            position = (self.pos[0] - camera_pos[0].astype(np.int32), self.pos[1] - camera_pos[1].astype(np.int32))
            screen.blit(self.content, position)
        else:
            screen.blit(self.hover_over_content, self.pos - camera_pos.astype(np.int32))


class TextButton(Button):
    def __init__(self, pos, message, font, color_not_selected, color_selected=None, center_pos=False):
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
        new_content = self.font.render(new_text, True, self.color)
        self.message = new_text
        self.set_content(new_content)
        if self.color_selected is not None:
            self.hover_over_content = self.font.render(new_text, True, self.color_selected)


class ImageButton(Button):
    def __init__(self, pos, content, description):
        super(ImageButton, self).__init__(pos, content)
        self.description = description
