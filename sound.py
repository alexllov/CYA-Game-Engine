# Windows ONLY, will need to rework eventually
import winsound

class Sound():
    """
    Note instances of [sound.play file] can only take a single sound file.
    To add multiple sound effects to one trigger,
    use multiple [sound.play] tags.
    """
    def __init__(self):
        ...
    
    def play(self, filepath):
        """
        Plays a given .wav sound file.
        """
        winsound.PlaySound(filepath, winsound.SND_FILENAME)

    def mod_txt(self, x, y):
        return ""
    
    def check_req(self, text, reqs):
        return (True, "")

    def process(self, type, items):
        for sound in items:
            self.play(sound)

if __name__ == "__main__":
    s = Sound()
    s.play("./Occult/sounds/battle/swing3.wav")