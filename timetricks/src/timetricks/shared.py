from dataclasses import dataclass

from ppb import Vector, Scene


@dataclass
class Controls:
    movement: Vector = Vector(0, 0)


@dataclass
class SlowTime:
    pass


@dataclass
class AccelerateTime:
    pass


@dataclass
class AdvanceSim:
    time_delta: float
    scene: Scene = None
    controls: Controls = None
