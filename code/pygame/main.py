import sys, pygame
from math import pi, sin, cos
from cart import Cart
from pole import Pole
from dcMotor import DCMotor
from timeManager import TimeManager
from animationManager import AnimationManager
from colour import Colour
import numpy as np

g = 9.81

startingPoleAngleInRad = np.pi/2 + np.pi/4

cart = Cart(0.5, 0.05, 0, -0.8, 0.8,
            Colour.red, DCMotor(0.065, 0.5, 0.01, 0.001, 0.05, Colour.black),
            Pole(0.2, startingPoleAngleInRad, 0.2, 0.005, Colour.green))

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
  va = 0
  # va = 12 * cos(i * dt * 2)
  cart.update(dt, va, g)

  xCartPix = am.toPixels(cart.x())
  
  am.drawRect(cart.color, xTopLeftPix=xCartPix, width=20)
  am.drawRect(cart.color, xTopLeftPix=am.toPixels(cart.max_x)+20)
  am.drawRect(cart.color, xTopLeftPix=am.toPixels(cart.min_x)-10)

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

  x0Pole = xCartPix + 10
  y0Pole = 0
  pole = cart.pole
  x1Pole = x0Pole + am.toPixels((pole.l * sin(pole.angle())))
  y1Pole = y0Pole + am.toPixels((-pole.l * cos(pole.angle())))
  am.drawLine(pole.color, (x0Pole, y0Pole), (x1Pole, y1Pole))

  # print(f"({x0Pole}, {y0Pole}), ({x1Pole}, {y1Pole})")
  # print(f"{cart.pole.angle()}, {cart.pole.angular_velocity()}")

  # if (abs(cart.pole.angular_velocity()) > 1000):
  #   exit()
  # texts = [
  #     f"Time: {round(i*dt,2)} s",
  #     f"",
  #     f"Cart:",
  #     f"Position: {round(cart.x(),2)} m",
  #     f"Velocity: {round(cart.velocity(),2)} m/s",
  #     f"Acceleration: {round(cart.acceleration(),2)} m/s^2",
  #     f"",
  #     f"Motor:",
  #     f"Angle: {round(cart.motor.angle(),2)} rad",
  #     f"Angular velocity: {round(cart.motor.angular_velocity(),2)} rad/s",
  # ]

  # for k, text_k in enumerate(texts):
  #     text = font.render(text_k, True, Colour.black, Colour.gray)
  #     text_rect = text.get_rect()
  #     am.screen.blit(
  #         text, (0, (text_rect.height) * k, text_rect.width, text_rect.height)
  #     )

  am.update()
  # pygame.time.delay(50)
  i += 1
