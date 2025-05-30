# Windows ONLY, will need to rework eventually
import winsound

class Sound():
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
        return True

    def process(self, type, items):
        for sound in items:
            self.play(sound)

if __name__ == "__main__":
    s = Sound()
    s.play("./Occult/sounds/battle/swing3.wav")