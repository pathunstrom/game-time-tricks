"""
A ppb game exploring time manipulation mechanics.
"""
from random import randint, uniform

import ppb
from ppb import gomlib

from timetricks import shared
from timetricks.sprites import Player, Ball, TrueTimeBall
from timetricks.systems import Controller


class TimeManipulation(gomlib.GameObject):
    time_levels = [0.25, 0.5, 1, 2, 4]
    current_level = 2
    total_run_time = 0
    current_count = 0

    def on_update(self, event: ppb.events.Update, signal):
        real_time_delta = event.time_delta
        modified_time_delta = real_time_delta * self.time_levels[self.current_level]
        self.current_count += modified_time_delta
        self.total_run_time += modified_time_delta

        while self.current_count >= real_time_delta:
            self.current_count -= real_time_delta
            signal(shared.AdvanceSim(time_delta=real_time_delta))

    def on_slow_time(self, event: shared.SlowTime, signal):
        self.current_level = max(self.current_level - 1, 0)

    def on_accelerate_time(self, event: shared.AccelerateTime, signal):
        self.current_level = min(self.current_level + 1, len(self.time_levels) - 1)


class TimeTricks(ppb.Scene):
    background_color = (0, 0, 0)

    def __init__(self, **props):
        super().__init__(**props)
        self.add(TimeManipulation())
        self.add(Player())
        self.add(Ball(velocity=ppb.Vector(1, 5).scale_to(6)))
        self.add(TrueTimeBall(velocity=ppb.Vector(3, 7).scale_to(8)))

    def on_scene_started(self, event: ppb.events.SceneStarted, signal):
        camera = self.main_camera
        left_limit = int(camera.left) + 1
        right_limit = int(camera.right) - 1
        top_limit = int(camera.top) - 1
        bottom_limit = int(camera.bottom) + 1
        for _ in range(randint(2, 6)):
            vector = ppb.Vector(
                    uniform(-1, 1), uniform(-1, 1)
                )
            if vector:
                vector = vector.scale_to(randint(1, 10))
            self.add(Ball(
                velocity=vector,
                position=ppb.Vector(randint(left_limit, right_limit),
                                    randint(bottom_limit, top_limit))
            ))

        for _ in range(1, 3):
            vector = ppb.Vector(
                uniform(-1, 1), uniform(-1, 1)
            )
            if vector:
                vector = vector.scale_to(randint(1, 10))
            self.add(TrueTimeBall(
                velocity=vector,
                position=ppb.Vector(randint(left_limit, right_limit),
                                    randint(bottom_limit, top_limit))
            ))


def main():
    ppb.run(
        starting_scene=TimeTricks,
        title='Time Tricks',
        systems=[Controller]
    )
