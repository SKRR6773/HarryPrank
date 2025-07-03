from .audio_manager import _AudioManager
import subprocess



class AudioManager(_AudioManager):
    def __init__(self):
        super().__init__()

    def _setPercent(self, percent):
        if not (percent >= 0 and percent <= 100):
            raise Exception("percent can 0 - 100")
        
        
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{percent}%"])


    def _setSystemMute(self, is_mute: bool):
        print("Result: ", is_mute)
