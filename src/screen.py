"""
Render
"""
from tkinter import Tk, Canvas, PhotoImage
from raycasting import RayCasting


class Screen:
    def __init__(self, width, height, level, player):
        self.level = level
        self.width = width
        self.height = height
        self.player = player
        self.raycasting = RayCasting(width, height, level, player)
        self.image = None

    def render(self):
        self.tk = Tk()
        self.canvas = Canvas(self.tk, width=self.width, height=self.height)
        self.canvas.pack()
        self.image = PhotoImage(width=self.width, height=self.height)
        self.canvas.create_image(
            0,
            0,
            image=self.image,
            anchor="nw",
            state="normal"
        )
        self.tk.after(100, self.update)
        self.tk.mainloop()

    def update(self):
        self.raycasting.raycasting()
        pixels = self.raycasting.get_pixels()
        self._update_image(pixels)
        self.canvas.update()
        self.player.angle += 2
        self.tk.after(100, self.update)

    def _update_image(self, pixels):
        for y in range(self.height):
            for x in range(self.width):
                data = pixels[y * self.width + x]
                self.image.put(data, (x, y))
