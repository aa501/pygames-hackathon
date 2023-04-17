import pygame


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        button_hover = self.rect.collidepoint(pos)

        # button border
        border_color = (255, 255, 255)
        border_thickness = 2
        pygame.draw.rect(surface, border_color, self.rect, border_thickness)

        # button background
        bg_color = (200, 200, 200)
        if button_hover:
            bg_color = (180, 180, 180)
        if self.clicked:
            bg_color = (150, 150, 150)
        pygame.draw.rect(surface, bg_color, self.rect)

        # button image
        image_offset = 10  # offset from the left and top edges of the button
        surface.blit(self.image, (self.rect.x + image_offset, self.rect.y + image_offset))

        # button click action
        if button_hover:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
