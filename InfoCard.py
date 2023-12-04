import pygame

def draw_info_card(screen, font, pos, right, bottom, text):
    if len(text) == 0:
        return

    text_surfaces = list(map(lambda t: font.render(t, True, (255, 255, 255)), text))
    width = max(surf.get_size()[0] for surf in text_surfaces) + 20
    height = sum(surf.get_size()[1] for surf in text_surfaces) + 20 + (len(text)-1)*10

    offest_pos = (pos[0] if right else pos[0] - width, pos[1] if bottom else pos[1] - height)

    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surf, (50, 50, 50, 200), pygame.Rect((0, 0), (width, height)), border_radius=5)
    
    text_pos = (10, 10)
    for text_surf in text_surfaces: 
        surf.blit(text_surf, text_pos)
        text_pos = (text_pos[0], text_pos[1] + text_surf.get_size()[1] + 10)

    screen.blit(surf, offest_pos)
