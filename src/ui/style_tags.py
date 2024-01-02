import customtkinter as ctk

# Style tags for displaying different styles of text in the ship console
class StyleTags:
    energy = {"family": "Futura", "size": 22}
    lifesupport = {"family": "Charm", "size": 20}
    nexus = {"family": "Chakra Petch", "size": 22}
    sensor = {"family": "BM Hannah Air", "size": 21}
    andale_mono = {"family": "Andale Mono", "size": 22}
    andale_mono_bold = {"family": "Andale Mono", "size": 22, "weight": 'bold'}

    TAGS = [
        {"tagName": "computer", "font": andale_mono},
        {"tagName": "energy", "foreground": "darkgreen", "font": energy},
        {"tagName": "lifesupport", "foreground": "#e864e8", "font": lifesupport},
        {"tagName": "nexus", "foreground": "lightgray", "font": nexus},
        {"tagName": "sensor", "foreground": "#a6684b", "font": sensor},
        {"tagName": "you", "foreground": "white", "font": nexus},
        {"tagName": "success", "foreground": "green", "font": andale_mono_bold},
        {"tagName": "failure", "foreground": "red", "font": andale_mono_bold}
    ]