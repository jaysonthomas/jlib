import sys, pygame
from colour import Colour

# TODO: Pass in background colour, width, height of window.
class AnimationManager:
  def __init__(self):
    self.colour = Colour
    pygame.init()
    
    # Create a pygame window of the specified height, width.
    self.width, self.height = 1200, 600
    self.screen = pygame.display.set_mode((self.width, self.height))
    
    # Fill the background with the speicifed colour.
    self.screen.fill(self.colour.gray)

  def drawRect(self, colour, topLeftX_m=0, topLeftY_m=0, width=10, height=10):
    x_pix = self.toPixels(topLeftX_m)
    y_pix = self.toPixels(topLeftY_m)
    x_pix, y_pix = self.toScreenPos(x_pix, y_pix)
    print(f"{x_pix}, {y_pix}")
    pygame.draw.rect(self.screen, colour, (x_pix, y_pix, width, height))

  def hasExitSignalBeenReceived(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        print("Exit signal received!!")
        sys.exit()

  def refresh(self):
    self.screen.fill(self.colour.gray)

  def toScreenPos(self, x_pix, y_pix):
    return x_pix + (self.width/2), y_pix + (self.height/2) 

  def toPixels(self, input_m: float):
    '''
    500 pixels represent 1 metre.
    '''
    return int(input_m * 500)
  
  def update(self):
    pygame.display.flip()
    