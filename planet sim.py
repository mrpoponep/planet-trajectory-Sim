import pygame as py
import math

WIDTH, HEIGHT = 800, 1000
WHITE=(255,255,255)
BLACK=(0,0,0)
YELLOW=(255,255,100)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FPS = 60

WIN=py.display.set_mode((WIDTH,HEIGHT))
py.init()
py.display.set_caption("Planet Simulation")

class planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day
    def __init__(self,x,y,radius,color,mass):
        self.x =x
        self.y =y
        self.radius=radius
        self.color=color
        self.mass=mass
        self.orbit=[]
        self.vel_x = 0
        self.vel_y = 0
    def draw(self):
        x=self.x *self.SCALE+400
        y=self.y *self.SCALE+400
        py.draw.circle(WIN,self.color,(x,y),self.radius)
        for i in self.orbit:
            py.draw.line(WIN,self.color,i,i)
    def attraction(self, other):
        other_x , other_y = other.x,other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y **2)
        force = self.G * ( other.mass * self.mass ) / distance**2
        omega = math.atan2(distance_y,distance_x)
        force_x = force * math.cos(omega)
        force_y = force * math.sin(omega)
        return force_x,force_y,distance
    
    def move(self,planets):
        total_fx= total_fy = 0
        for p in planets:
            if self == p:
                continue
            fx,fy,d = self.attraction(p)
            total_fx+=fx
            total_fy+=fy
        
        self.vel_x += total_fx / self.mass * self.TIMESTEP
        self.vel_y += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.vel_x * self.TIMESTEP
        self.y += self.vel_y * self.TIMESTEP
        self.orbit.append((self.x*self.SCALE+400,self.y*self.SCALE+400))
    
    def stat(self,name,x,y):
        distance=round(math.sqrt(self.x**2+self.y**2))
        title_font = py.font.SysFont("comicsans", 25)
        orbit= title_font.render(f"{name}: {distance}",1, WHITE)
        WIN.blit(orbit,(x,y))
def main():
    sun=planet(0,0,30,YELLOW,1.98892 * 10**30)
    earth = planet(1 * planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.vel_y=29.783 * 1000
    mars = planet(1.524 * planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.vel_y = 24.077 * 1000
    mercury = planet(0.387 * planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.vel_y = 47.4 * 1000
    venus = planet(0.723 * planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.vel_y = 35.02 * 1000
    
    planets=[sun,earth,mars,mercury,venus]

    running=True
    clock=py.time.Clock()
    while running:
        clock.tick(FPS)
        WIN.fill(BLACK)
        for p in planets:
            p.draw()
            p.move(planets)
        
        for event in py.event.get():
            if event.type == py.QUIT:
                running=False

        mercury.stat('Mercury',50,825)
        venus.stat('Venus',50,900)
        earth.stat('Earth',450,825)
        mars.stat('Mars',450,900)

        py.display.flip()
    py.quit()

main()