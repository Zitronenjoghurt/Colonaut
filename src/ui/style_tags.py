import customtkinter as ctk

# Style tags for displaying different styles of text in the ship console
class StyleTags:
    andale_mono = {"family": "Andale Mono", "size": 22}
    andale_mono_bold = {"family": "Andale Mono", "size": 22, "weight": 'bold'}

    TAGS = [
        {"tagName": "computer", "font": andale_mono},
        {"tagName": "energy", "foreground": "darkgreen", "font": andale_mono},
        {"tagName": "success", "foreground": "green", "font": andale_mono_bold},
        {"tagName": "failure", "foreground": "red", "font": andale_mono_bold}
    ]