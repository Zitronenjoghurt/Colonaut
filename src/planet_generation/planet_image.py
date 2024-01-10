import random
from customtkinter import CTkImage
from typing import Optional
from PIL import Image
from src.utils.file_operations import construct_path, file_to_dict

PLANET_IMAGE_INDEX = construct_path("src/data/planet_image_index.json")
PLANET_IMAGE_SOURCE = construct_path("src/assets/planets/{name}.gif")

class PlanetImage():
    def __init__(
            self, 
            name: str, 
            tags: list[str], 
            path: str, 
            height: int, 
            width: int, 
            frame_count: int, 
            frame: Optional[int] = None, 
            angle: Optional[int] = None,
            flip_h: Optional[bool] = None,
            flip_v: Optional[bool] = None) -> None:
        self.name = name
        self.tags = tags
        self.path = path
        self.height = height
        self.width = width
        self.frame_count = frame_count
        self.frame = frame
        self.angle = angle
        self.flip_h = flip_h
        self.flip_v = flip_v

    def random_frame(self) -> int:
        return random.randint(0, self.frame_count - 1)
    
    def random_angle(self) -> int:
        return random.randint(0, 360)
    
    def copy_random_self(self) -> 'PlanetImage':
        random_frame = self.random_frame()
        random_angle = self.random_angle()
        flip_h = random.choice([True, False])
        flip_v = random.choice([True, False])

        self_copy = PlanetImage(
            name=self.name,
            tags=self.tags,
            path=self.path,
            height=self.height,
            width=self.width,
            frame_count=self.frame_count,
            frame=random_frame,
            angle=random_angle,
            flip_h=flip_h,
            flip_v=flip_v
        )

        return self_copy

    def get_image(self) -> Image.Image:
        random_frame = self.frame if self.frame else self.random_frame()
        random_angle = self.angle if self.angle else self.random_angle()
        flip_h = self.flip_h if self.flip_h else random.choice([True, False])
        flip_v = self.flip_v if self.flip_v else random.choice([True, False])

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
    EXISTING_TAGS = []
    COUNTS_PER_TAG = {}
    
    def __init__(self) -> None:
        if PlanetImageLibrary._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of PlanetImageLibrary.")
        self.image_index = file_to_dict(PLANET_IMAGE_INDEX)
        self.library: dict[str, PlanetImage] = {}
        
        for name, data in self.image_index.items():
            tags = data.get("tags", [])
            for tag in tags:
                self._handle_tag(tag=tag)
            self.library[name] = self._load_image(name=name, tags=tags)

    @staticmethod
    def _handle_tag(tag: str) -> None:
        if tag not in PlanetImageLibrary.EXISTING_TAGS:
            PlanetImageLibrary.EXISTING_TAGS.append(tag)
        if tag not in PlanetImageLibrary.COUNTS_PER_TAG:
            PlanetImageLibrary.COUNTS_PER_TAG[tag] = 0
        PlanetImageLibrary.COUNTS_PER_TAG[tag] += 1

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
    
    def get_by_tags(self, tags: list[str]) -> Optional[PlanetImage]:
        result = {name: image for name, image in self.library.items() if sorted(image.tags) == sorted(tags)}
        if result:
            image = random.choice(list(result.values()))
            return image.copy_random_self()
        return None