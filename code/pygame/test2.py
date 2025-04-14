import sys, pygame
from math import pi, sin, cos
from cartpole import Cart, Pole, DCMotor
from timeManager import TimeManager
from animationManager import AnimationManager
from colour import Colour

g = 9.81

# 0 is upwards. A clockwise rotation leads to +90 horizontally right.
# +270 is horizontally left.
startingPoleAngleInRad = 360 / 180 * pi
childPoles = Pole(
    0.2,
    5 / 180 * pi,
    0.15,
    0.005,
    Colour.blue,
    Pole(0.2, 15 / 180 * pi, 0.10, 0.005, Colour.purple, None),
)
childPoles = None

cart = Cart(
    0.5,
    0.05,
    0,
    -0.8,
    0.8,
    Colour.red,
    DCMotor(0.05, 0.5, 0.05, 0.01, 0.05, Colour.black),
    Pole(
        0.2,
        startingPoleAngleInRad,
        0.2,
        0.005,
        Colour.green,
        childPoles,
    ),
)

timeManager = TimeManager()
am = AnimationManager()
i = 0

font = pygame.font.Font("freesansbold.ttf", 20)

while True:
  if not timeManager.isItTimeToUpdatePlot():
    continue

  am.hasExitSignalBeenReceived()

  am.refresh()
  dt = 0.001
  cart.update(dt, 12 * cos(i * dt * 2), g)

  am.drawRect(cart.color, topLeftX_m=cart.x(), width=20)
  am.drawRect(cart.color, topLeftX_m=cart.max_x+(20/500))
  am.drawRect(cart.color, topLeftX_m=cart.min_x-(10/500))

  # motor_x0 = min_x - 100
  # motor_sin = si_to_pixels(sin(-cart.motor.angle()) * 0.05)
  # motor_cos = si_to_pixels(cos(-cart.motor.angle()) * 0.05)

  # pygame.draw.polygon(
  #     screen,
  #     cart.motor.color,
  #     [
  #         (motor_x0 + motor_sin, y0 + motor_cos),
  #         (motor_x0 + motor_cos, y0 - motor_sin),
  #         (motor_x0 - motor_sin, y0 - motor_cos),
  #         (motor_x0 - motor_cos, y0 + motor_sin),
  #     ],
  # )

  # x0 += 10
  # for pole in cart:
  #     x1 = x0 + si_to_pixels(pole.l * sin(pole.angle()))
  #     y1 = y0 + si_to_pixels(-pole.l * cos(pole.angle()))
  #     pygame.draw.line(screen, pole.color, (x0, y0), (x1, y1), 10)
  #     x0 = x1
  #     y0 = y1

  texts = [
      f"Time: {round(i*dt,2)} s",
      f"",
      f"Cart:",
      f"Position: {round(cart.x(),2)} m",
      f"Velocity: {round(cart.velocity(),2)} m/s",
      f"Acceleration: {round(cart.acceleration(),2)} m/s^2",
      f"",
      f"Motor:",
      f"Angle: {round(cart.motor.angle(),2)} rad",
      f"Angular velocity: {round(cart.motor.angular_velocity(),2)} rad/s",
  ]

  for k, text_k in enumerate(texts):
      text = font.render(text_k, True, Colour.black, Colour.gray)
      text_rect = text.get_rect()
      am.screen.blit(
          text, (0, (text_rect.height) * k, text_rect.width, text_rect.height)
      )



  am.update()
  i += 1
