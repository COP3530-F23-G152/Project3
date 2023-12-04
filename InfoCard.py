import pygame

def draw_info_card(screen, font, pos, right, bottom, zone_name, zone_percent):
    zone_name_surface = font.render(zone_name, True, (255, 255, 255))
    zone_percent_surface = font.render("Incoming Percent: {:.2f}%".format(zone_percent), True, (255, 255, 255))
    width = max(zone_name_surface.get_size()[0], zone_percent_surface.get_size()[0]) + 20
    height = zone_name_surface.get_size()[1] + 10 + zone_percent_surface.get_size()[1] + 20

    offest_pos = (pos[0] if right else pos[0] - width, pos[1] if bottom else pos[1] - height)

    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surf, (50, 50, 50, 200), pygame.Rect((0, 0), (width, height)), border_radius=5)
    surf.blit(zone_name_surface, (10, 10))
    surf.blit(zone_percent_surface, (10, 10 + zone_name_surface.get_size()[1] + 10))
    screen.blit(surf, offest_pos)
