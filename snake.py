import tkinter as tk
import random

ANCHO = 600
ALTO = 600
TAMANO_CELDA = 20
VELOCIDAD = 100

class JuegoSnake:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake - Juego de la Viborita")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="black")
        self.canvas.pack()
        
        self.label_puntuacion = tk.Label(root, text="Puntuación: 0", font=("Arial", 14), fg="white", bg="black")
        self.label_puntuacion.pack()
        
        self.reiniciar_juego()
        
        self.root.bind("<KeyPress>", self.cambiar_direccion)
        self.root.focus_set()
        
    def reiniciar_juego(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direccion = "Right"
        self.siguiente_direccion = "Right"
        self.comida = self.generar_comida()
        self.puntuacion = 0
        self.juego_terminado = False
        self.label_puntuacion.config(text=f"Puntuación: {self.puntuacion}")
        self.actualizar()
        
    def generar_comida(self):
        while True:
            x = random.randint(0, (ANCHO // TAMANO_CELDA) - 1) * TAMANO_CELDA
            y = random.randint(0, (ALTO // TAMANO_CELDA) - 1) * TAMANO_CELDA
            if (x, y) not in self.snake:
                return (x, y)
    
    def cambiar_direccion(self, event):
        teclas = {
            "Up": "Up", "Down": "Down", "Left": "Left", "Right": "Right",
            "w": "Up", "s": "Down", "a": "Left", "d": "Right",
            "W": "Up", "S": "Down", "A": "Left", "D": "Right"
        }
        if event.keysym in teclas:
            nueva = teclas[event.keysym]
            opuestos = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if nueva != opuestos.get(self.direccion):
                self.siguiente_direccion = nueva
    
    def mover(self):
        self.direccion = self.siguiente_direccion
        cabeza_x, cabeza_y = self.snake[0]
        
        if self.direccion == "Up":
            cabeza_y -= TAMANO_CELDA
        elif self.direccion == "Down":
            cabeza_y += TAMANO_CELDA
        elif self.direccion == "Left":
            cabeza_x -= TAMANO_CELDA
        elif self.direccion == "Right":
            cabeza_x += TAMANO_CELDA
            
        nueva_cabeza = (cabeza_x, cabeza_y)
        
        # Colisión con paredes
        if (cabeza_x < 0 or cabeza_x >= ANCHO or 
            cabeza_y < 0 or cabeza_y >= ALTO or 
            nueva_cabeza in self.snake):
            self.game_over()
            return
            
        self.snake.insert(0, nueva_cabeza)
        
        # Comer comida
        if nueva_cabeza == self.comida:
            self.puntuacion += 10
            self.label_puntuacion.config(text=f"Puntuación: {self.puntuacion}")
            self.comida = self.generar_comida()
        else:
            self.snake.pop()
    
    def game_over(self):
        self.juego_terminado = True
        self.canvas.create_text(ANCHO//2, ALTO//2, text="💀 GAME OVER 💀", 
                               fill="red", font=("Arial", 30, "bold"))
        self.canvas.create_text(ANCHO//2, ALTO//2 + 50, 
                               text=f"Puntuación final: {self.puntuacion}", 
                               fill="white", font=("Arial", 18))
        self.canvas.create_text(ANCHO//2, ALTO//2 + 100, 
                               text="Presiona ESPACIO para reiniciar", 
                               fill="yellow", font=("Arial", 14))
        self.root.bind("<space>", lambda e: self.reiniciar_juego())
    
    def dibujar(self):
        self.canvas.delete("all")
        
        # Dibujar serpiente
        for i, (x, y) in enumerate(self.snake):
            color = "lime" if i == 0 else "green"
            self.canvas.create_rectangle(x, y, x + TAMANO_CELDA, y + TAMANO_CELDA, 
                                       fill=color, outline="darkgreen")
            # Ojos en la cabeza
            if i == 0:
                ojo_x = x + 5 if self.direccion in ["Up", "Down"] else (x + 15 if self.direccion == "Right" else x + 5)
                ojo_y = y + 5 if self.direccion in ["Left", "Right"] else (y + 15 if self.direccion == "Down" else y + 5)
                self.canvas.create_oval(ojo_x, ojo_y, ojo_x + 4, ojo_y + 4, fill="black")
                ojo_x2 = x + 15 if self.direccion in ["Up", "Down"] else (x + 5 if self.direccion == "Right" else x + 15)
                ojo_y2 = y + 5 if self.direccion in ["Left", "Right"] else (y + 15 if self.direccion == "Down" else y + 5)
                self.canvas.create_oval(ojo_x2, ojo_y2, ojo_x2 + 4, ojo_y2 + 4, fill="black")
        
        # Dibujar comida
        cx, cy = self.comida
        self.canvas.create_oval(cx, cy, cx + TAMANO_CELDA, cy + TAMANO_CELDA, 
                               fill="red", outline="darkred")
        # Brillo en la comida
        self.canvas.create_oval(cx + 3, cy + 3, cx + 8, cy + 8, fill="orange", outline="")
    
    def actualizar(self):
        if not self.juego_terminado:
            self.mover()
            self.dibujar()
            self.root.after(VELOCIDAD, self.actualizar)
        else:
            self.dibujar()

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoSnake(root)
    root.mainloop()