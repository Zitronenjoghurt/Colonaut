# Style tags for displaying different styles of text in the ship console
class StyleTags:
    energy = {"family": "Stifly", "size": 22}
    lifesupport = {"family": "The Fruit Star", "size": 20}
    nexus = {"family": "ELNATH", "size": 22}
    you = {"family": "ELNATH", "size": 24}
    sensor = {"family": "Achron Regular", "size": 24}
    geist_mono = {"family": "Geist Mono", "size": 22}
    geist_mono_bold = {"family": "Geist Mono", "size": 22, "weight": 'bold'}

    TAGS = [
        {"tagName": "computer", "font": geist_mono},
        {"tagName": "energy", "foreground": "darkgreen", "font": energy},
        {"tagName": "lifesupport", "foreground": "#e864e8", "font": lifesupport},
        {"tagName": "nexus", "foreground": "lightgray", "font": nexus},
        {"tagName": "sensor", "foreground": "#a6684b", "font": sensor},
        {"tagName": "you", "foreground": "white", "font": you},
        {"tagName": "success", "foreground": "green", "font": geist_mono_bold},
        {"tagName": "failure", "foreground": "red", "font": geist_mono_bold},
        {"tagName": "warning", "foreground": "#ffcc00", "font": geist_mono_bold}
    ]