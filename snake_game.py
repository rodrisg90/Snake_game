import turtle
import time
import random


class SnakeGame:
    def __init__(self, width=600, height=600, color="green"):
        """Inicializa los componentes del juego."""
        self._width = width
        self._height = height
        # Inicializa el lienzo de la pantalla
        self.screen = turtle.Screen()
        self.screen.title("Snake game")
        self.screen.bgcolor(color)
        self.screen.setup(width=width, height=height)
        self.screen.tracer(0)
        # Inicializa la serpiente
        self.snake = turtle.Turtle()
        self.snake.speed(0)
        self.snake.shape("square")
        self.snake.color("orange")
        self.snake.penup()
        self.snake.goto(0, 0)
        # Inicializa el texto que se muestra en la pantalla
        self.text = turtle.Turtle()
        self.text.speed(0)
        self.text.shape("square")
        self.text.color("white")
        self.text.penup()
        self.text.hideturtle()
        self.text.goto(0, (height / 2) - 40)
        # Inicialización de la comida de la serpiente
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0, 100)
        # Atributos de la clase
        self._direction = None
        self._delay = 0.1
        self._score = 0
        self._high_score = 0
        self.snake_body = []
        # Asociación de los movimientos y las teclas
        self.screen.listen()
        self.screen.onkeypress(self.up, "w")
        self.screen.onkeypress(self.down, "s")
        self.screen.onkeypress(self.left, "a")
        self.screen.onkeypress(self.right, "d")
        # Imprimimos marcador
        self._print_score()

    def up(self):
        """Este método define el movimiento hacia arriba de la serpiente"""
        if self._direction != "down":
            self._direction = "up"

    def down(self):
        if self._direction != "up":
            self._direction = "down"

    def left(self):
        if self._direction != "right":
            self._direction = "left"

    def right(self):
        if self._direction != "left":
            self._direction = "right"

    def move(self):
        # Obtenemos las coordenadas de la cabeza de la serpiente
        hx, hy = self.snake.xcor(), self.snake.ycor()

        # Movemos el cuerpo de la serpiente
        for i in range(len(self.snake_body) - 1, 0, -1):
            x = self.snake_body[i - 1].xcor()
            y = self.snake_body[i - 1].ycor()
            self.snake_body[i].goto(x, y)

        # Movemos el nuevo cuadrado más cercano a la cabeza
        if len(self.snake_body) > 0:
            self.snake_body[0].goto(hx, hy)

        if self._direction == "up":
            self.snake.sety(hy + 20)
        elif self._direction == "down":
            self.snake.sety(hy - 20)
        elif self._direction == "left":
            self.snake.setx(hx - 20)
        elif self._direction == "right":
            self.snake.setx(hx + 20)

    def play(self):

        while True:
            self.screen.update()
            self.borders()
            self.eating_food()
            self.body_crash()
            time.sleep(self._delay)
            self.move()
        self.screen.mainloop()

    def borders(self):
        bxcor = (self._width // 2) - 10
        bycor = (self._height // 2) - 10

        if self.snake.xcor() > bxcor or self.snake.xcor() < -bxcor or self.snake.ycor() > bycor or self.snake.ycor() < -bycor:
            self._reset()

    def body_crash(self):
        for s in self.snake_body:
            if s.distance(self.snake) < 20:
                self._reset()

    def eating_food(self):
        if self.snake.distance(self.food) < 20:
            # Mover la comida de lugar
            bxcor = (self._width // 2) - 10
            bycor = (self._height // 2) - 10
            x = random.randint(-bxcor, bxcor)
            y = random.randint(-bycor, bycor)
            self.food.goto(x, y)
            # Aumentar el cuerpo de la serpiente
            self.increase_body()
            # Reducir el delay
            self._delay -= 0.001
            # Aumentar el score
            self._score += 10
            self._print_score()

    def increase_body(self):
        new_square = turtle.Turtle()
        new_square.speed(0)
        new_square.shape("square")
        new_square.color("orange")
        new_square.penup()
        self.snake_body.append(new_square)

    def _print_score(self):
        self.text.clear()
        self.text.write("Puntos: {} Record: {}".format(self._score, self._high_score), align="center",
                        font=("Century Gothic", 24, "normal"))

    def _reset(self):
        time.sleep(1)
        self.snake.goto(0, 0)
        self._direction = None
        # Reiniciamos el cuerpo de la serpiente
        for s in self.snake_body:
            s.ht()  # Oculta el segmento
        # Limpiar cuadrados de la serpiente
        self.snake_body.clear()
        # Reiniciar el delay
        self._delay = 0.1
        # Reiniciar el score
        if self._score > self._high_score:
            self._high_score = self._score
        self._score = 0
        self._print_score()

snake_game = SnakeGame()

snake_game.play()