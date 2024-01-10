import random
from customtkinter import CTkImage
from typing import Optional
from PIL import Image
from src.utils.file_operations import construct_path, file_to_dict

PLANET_IMAGE_INDEX = construct_path("src/data/planet_image_index.json")
PLANET_IMAGE_SOURCE = construct_path("src/assets/planets/{name}.gif")

class PlanetImage():
    def __init__(self, name: str, tags: list[str], path: str, height: int, width: int, frame_count: int) -> None:
        self.name = name
        self.tags = tags
        self.path = path
        self.height = height
        self.width = width
        self.frame_count = frame_count

    def get_image(self) -> Image.Image:
        random_frame = random.randint(0, self.frame_count - 1)
        random_angle = random.randint(0, 360)
        with Image.open(self.path) as gif:
            gif.seek(random_frame)
            if gif.mode == 'P':
                gif = gif.convert('RGB')
            gif = gif.rotate(random_angle)
            return gif.copy()
        
    def get_ctk_image(self, height: Optional[int] = None, width: Optional[int] = None) -> CTkImage:
        if height is None:
            height = self.height
        if width is None:
            width = self.width
        image = self.get_image()
        return CTkImage(image, size=(width, height))

class PlanetImageLibrary():
    _instance = None
    
    def __init__(self) -> None:
        if PlanetImageLibrary._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of PlanetImageLibrary.")
        self.image_index = file_to_dict(PLANET_IMAGE_INDEX)
        self.library: dict[str, PlanetImage] = {}
        
        for name, data in self.image_index.items():
            tags = data.get("tags", [])
            self.library[name] = self._load_image(name=name, tags=tags)

    def _load_image(self, name: str, tags: list[str]) -> PlanetImage:
        path = PLANET_IMAGE_SOURCE.format(name=name)
        gif = Image.open(path)

        frame_count = 0
        while True:
            try:
                gif.seek(frame_count)
                frame_count += 1
            except EOFError:
                break
        
        return PlanetImage(name=name, tags=tags, path=path, height=gif.height, width=gif.width, frame_count=frame_count)

    @staticmethod
    def get_instance() -> 'PlanetImageLibrary':
        if PlanetImageLibrary._instance is None:
            PlanetImageLibrary._instance = PlanetImageLibrary()
        return PlanetImageLibrary._instance