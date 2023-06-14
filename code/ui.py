import pygame

from settings import *
from player import Player

class UI:
    def __init__(self) -> None:
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current_amount: int, max_amount: int, bg_rect: pygame.Rect, color: str):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel 
        ratio: float = current_amount / max_amount
        current_width = int(bg_rect.width * ratio)
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp: int):
        text_surf = self.font.render(str(exp), False, TEXT_COLOR)
        text_rect = text_surf.get_rect()
        text_rect.bottomright = (WIDTH - 20, HEIGTH - 20)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def display(self, player: Player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect,
                      HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect,
                      ENERGY_COLOR)

        self.show_exp(player.exp)
