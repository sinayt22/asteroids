import pygame


def create_triple_shot_icon():
    """Combine 3 arrow images into one pickup icon"""
    # Load the base arrow image
    arrow = pygame.image.load("laser_shot_1.png").convert_alpha()
    arrow = pygame.transform.scale(arrow, (150, 150))  # Size it appropriately
    arrow = pygame.transform.rotate(arrow, 90)
    
    # Create a surface to hold all 3 arrows
    icon_size = 100
    combined = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
    
    # Rotate and position each arrow
    # Center arrow (0 degrees)
    center_arrow = arrow.copy()
    rect = center_arrow.get_rect(center=(icon_size//2, icon_size//2))
    combined.blit(center_arrow, rect)
    
    # Left arrow (-45 degrees)
    left_arrow = pygame.transform.rotate(arrow, 45)
    rect = left_arrow.get_rect(center=(icon_size//2 - 15, icon_size//2 + 15))
    combined.blit(left_arrow, rect)
    
    # Right arrow (+45 degrees)
    right_arrow = pygame.transform.rotate(arrow, -45)
    rect = right_arrow.get_rect(center=(icon_size//2 + 15, icon_size//2 + 15))
    combined.blit(right_arrow, rect)
    
    return combined

def create_super_shot_icon():
    """Combine 3 arrow images into one pickup icon"""
    # Load the base arrow image
    arrow = pygame.image.load("laser_shot_2.png").convert_alpha()
    arrow = pygame.transform.scale(arrow, (150, 150))  # Size it appropriately
    arrow = pygame.transform.rotate(arrow, 90)
    
    icon_size = 150
    combined = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
    rect = combined.get_rect(center=(icon_size // 2, icon_size // 2))
    combined.blit(arrow, rect)
    
    return combined