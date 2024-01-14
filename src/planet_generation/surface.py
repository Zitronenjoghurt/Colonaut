from src.planet_generation.probability import Probability

class Surface():
    def __init__(self, texture: list[str], topography: list[str]) -> None:
        self.texture = texture
        self.topography = topography

    @staticmethod
    def from_dict(data: dict) -> 'Surface':
        texture = data.get("texture", [])
        topography = data.get("topography", [])

        return Surface(texture=texture, topography=topography)

    def to_dict(self) -> dict:
        data = {
            "texture": self.texture,
            "topography": self.topography
        }
        return data

class RandomSurface():
    def __init__(self, texture: Probability, topography: Probability) -> None:
        self.texture = texture
        self.topography = topography

    @staticmethod
    def create(data: dict) -> 'RandomSurface':
        texture = data.get("texture", [])
        topography = data.get("topography", [])
        
        random_surface = RandomSurface(
            texture=Probability.create(texture),
            topography=Probability.create(topography)
        )

        return random_surface

    def generate(self) -> Surface:
        texture = self.texture.generate()
        topography = self.topography.generate()
        return Surface(texture=texture, topography=topography)