import pygame

# Draws an info containing a line for every piece of text in text
def draw_info_card(screen, font, pos, right, bottom, text):
    # If there is no text do nothing
    if len(text) == 0:
        return

    # Convert all the text to surfaces using the passed font
    text_surfaces = list(map(lambda t: font.render(t, True, (255, 255, 255)), text))

    # Compute the width and height of the card
    width = max(surf.get_size()[0] for surf in text_surfaces) + 20
    height = sum(surf.get_size()[1] for surf in text_surfaces) + 20 + (len(text)-1)*10

    # Compute the position of the card
    offest_pos = (pos[0] if right else pos[0] - width, pos[1] if bottom else pos[1] - height)

    # Create a new surface for drawing the card on
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surf, (50, 50, 50, 200), pygame.Rect((0, 0), (width, height)), border_radius=5)
   
    # Draw all the text to the card
    text_pos = (10, 10)
    for text_surf in text_surfaces: 
        surf.blit(text_surf, text_pos)
        text_pos = (text_pos[0], text_pos[1] + text_surf.get_size()[1] + 10)

    # Blit the card to the screen 
    screen.blit(surf, offest_pos)
