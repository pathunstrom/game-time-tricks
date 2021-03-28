from ppb import Sprite, Square, Vector, Circle, directions, events

from timetricks.shared import AdvanceSim


class Player(Sprite):
    image = Square(180, 50, 140)
    speed = 3

    def on_advance_sim(self, event: AdvanceSim, signal):
        self.position += event.controls.movement * self.speed * event.time_delta


class BaseBall(Sprite):
    velocity: Vector = Vector(1, 2).scale_to(5)
    image = Circle(255, 255, 255)

    def advance_sim(self, event):
        camera = event.scene.main_camera
        if camera.left >= self.position.x - (0.5 * self.size):
            self.velocity = self.velocity.reflect(directions.Right)
        elif camera.right <= self.position.x + (0.5 * self.size):
            self.velocity = self.velocity.reflect(directions.Left)

        if camera.top <= self.position.y + (0.5 * self.size):
            self.velocity = self.velocity.reflect(directions.Down)
        elif camera.bottom >= self.position.y - (0.5 * self.size):
            self.velocity = self.velocity.reflect(directions.Up)

        for ball in event.scene.get(kind=BaseBall):
            if (self.position - ball.position).length <= self.size:
                from_other = self.position - ball.position
                new_velocities = (self.velocity.length + ball.velocity.length) / 2
                if from_other:
                    self.velocity = self.velocity.reflect(from_other.normalize())
                    self.velocity.scale_to(new_velocities)
                to_other = ball.position - self.position
                if to_other:
                    ball.velocity = ball.velocity.reflect(to_other.normalize())
                    self.velocity.scale_to(new_velocities)

        self.position += self.velocity * event.time_delta


class Ball(BaseBall):

    def on_advance_sim(self, event: AdvanceSim, signal):
        self.advance_sim(event)


class TrueTimeBall(BaseBall):
    image = Circle(50, 200, 50)

    def on_update(self, event: events.Update, signal):
        self.advance_sim(event)
