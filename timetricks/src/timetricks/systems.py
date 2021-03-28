import ppb
from ppb import Vector, keycodes
from ppb.engine import GameEngine
from ppb.systemslib import System

from timetricks import shared


class Controller(System):
    movement: Vector = Vector(0, 0)

    def __init__(self, engine: GameEngine, **kwargs):
        super().__init__(engine=engine, **kwargs)
        engine.register(shared.AdvanceSim, self.extend)

    def extend(self, update_event):
        movement = self.movement
        if movement:
            movement = movement.normalize()
        update_event.controls = shared.Controls(movement)

    def on_key_pressed(self, event: ppb.events.KeyPressed, signal):
        if event.key is keycodes.W:
            self.movement += ppb.directions.Up
        elif event.key is keycodes.S:
            self.movement += ppb.directions.Down
        elif event.key is keycodes.D:
            self.movement += ppb.directions.Right
        elif event.key is keycodes.A:
            self.movement += ppb.directions.Left
        elif event.key is keycodes.Q:
            signal(shared.SlowTime())
        elif event.key is keycodes.E:
            signal(shared.AccelerateTime())

    def on_key_released(self, event: ppb.events.KeyReleased, signal):
        if event.key is keycodes.W:
            self.movement -= ppb.directions.Up
        elif event.key is keycodes.S:
            self.movement -= ppb.directions.Down
        elif event.key is keycodes.D:
            self.movement -= ppb.directions.Right
        elif event.key is keycodes.A:
            self.movement -= ppb.directions.Left
