from resources import screen as sc

class ParticleGroup:
    def __init__(self, num_particles, particle_class):
        self.particles = [particle_class() for _ in range(num_particles)]

    def update(self, delta):
        for particle in self.particles:
            particle.update(delta)

    def draw(self, screen=sc):
        for particle in self.particles:
            particle.draw(screen)
