# animations.py - Анимации (БЕЗ ОШИБОК)

import tkinter as tk
import random

class AnimationManager:
    def __init__(self, root):
        self.root = root
        self.animations = []
        self.particles = []
        
    def show_click_effect(self, x, y, text, color='#FFD700'):
        """Показать эффект клика в указанной позиции"""
        label = tk.Label(self.root, text=text, font=('Arial', 16, 'bold'),
                         fg=color, bg='#1a1a2e')
        label.place(x=x, y=y)
        
        # Анимация: поднимаем и исчезаем
        self._animate_label(label, y, 60, 0.8)
    
    def _animate_label(self, label, start_y, distance, duration):
        """Внутренняя анимация подъёма и исчезновения"""
        steps = 25
        delta_y = distance / steps
        
        def step(current_step=0):
            if current_step < steps:
                new_y = start_y - (current_step * delta_y)
                label.place(y=new_y)
                
                self.root.after(int(duration * 1000 / steps), 
                               lambda s=current_step + 1: step(s))
            else:
                label.destroy()
        
        step(0)
    
    def show_build_effect(self, x, y, text):
        """Эффект постройки здания"""
        colors = ['#FFD700', '#FF6F00', '#FFAB00', '#FFC107', '#FFE082']
        for i in range(15):
            self.root.after(i * 50, lambda i=i: self._sparkle(
                x + random.randint(-40, 40),
                y + random.randint(-40, 40),
                random.choice(colors)
            ))
        
        label = tk.Label(self.root, text=text, font=('Arial', 14, 'bold'),
                         fg='#4CAF50', bg='#1a1a2e')
        label.place(x=x-80, y=y-20)
        self.root.after(2000, label.destroy)
    
    def _sparkle(self, x, y, color):
        """Одна искра"""
        size = random.randint(4, 8)
        label = tk.Label(self.root, text='✦', font=('Arial', size, 'bold'),
                         fg=color, bg='#1a1a2e')
        label.place(x=x, y=y)
        self.root.after(500, label.destroy)
    
    def show_particles(self, canvas, x, y, count=8):
        """Показать частицы в указанной позиции"""
        colors = ['#FFD700', '#FF6F00', '#4CAF50', '#E53935', '#1565C0', '#FFAB00']
        for _ in range(count):
            color = random.choice(colors)
            size = random.randint(3, 8)
            particle = Particle(canvas, x + random.randint(-10, 10), 
                               y + random.randint(-10, 10), 
                               color, size)
            self.particles.append(particle)
        
        self._update_particles(canvas)
    
    def _update_particles(self, canvas):
        """Обновление частиц"""
        if not self.particles:
            return
        
        for p in self.particles[:]:
            if not p.update():
                self.particles.remove(p)
        
        if self.particles:
            self.root.after(50, lambda: self._update_particles(canvas))

class Particle:
    def __init__(self, canvas, x, y, color, size=6):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.vx = random.randint(-4, 4)
        self.vy = random.randint(-8, -2)
        self.life = 1.0
        self.id = canvas.create_oval(x, y, x+size, y+size, fill=color, outline='')
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15
        self.life -= 0.02
        self.size *= 0.97
        
        if self.life <= 0 or self.size < 1:
            self.canvas.delete(self.id)
            return False
        
        self.canvas.coords(self.id, self.x, self.y, 
                          self.x + self.size, self.y + self.size)
        return True
