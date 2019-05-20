import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class PongBall(Widget):
    vx = NumericProperty(0)
    vy = NumericProperty(0)
    v = ReferenceListProperty(vx, vy)

    def move(self):
        self.pos = Vector(*self.v) + self.pos


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.v
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            speedup = 1.1
            v = bounced * speedup
            ball.v = v.x, v.y + offset


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, v=(4, 0)):
        self.ball.center = self.center
        self.ball.v = v


    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.vy *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(v=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(v=(-4, 0))


    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    PongApp().run()

