from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, AudioSession
from typing import List
from .audio_manager import _AudioManager
from ..check_platform import is_linux


if not is_linux:
    from comtypes import CLSCTX_ALL, CoInitialize
    from ctypes import cast, POINTER




class AudioManager(_AudioManager):
    
    def __init__(self):
        
        super().__init__()


        CoInitialize()


    def _setPercent(self, percent):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))


            volume.SetMasterVolumeLevelScalar(percent / 100, None)


            return True, "Success"

        except Exception as ex:
            return False, str(ex)
        

    def _setSystemMute(self, is_mute: bool = True):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            volume.SetMute(1 if is_mute else 0, None)


            return True, "Success"

        except Exception as ex:
            print(ex)

            return False, str(ex)
        

    def _setMuteStateWithProcessName(self, process_name: str, is_mute: bool = False):
        try:
            sessions: List[AudioSession] = AudioUtilities.GetAllSessions()

            for session in sessions:
                interface = session.SimpleAudioVolume

                if session.Process and process_name in session.Process.name():
                    interface.SetMute(1 if is_mute else 0, None)


        except Exception as ex:
            print(ex)
            return False, str(ex)
        

    def _setPercenProcessName(self, process_name: str, percen: int):
        try:
            sessions: List[AudioSession] = AudioUtilities.GetAllSessions()

            for session in sessions:
                interface = session.SimpleAudioVolume



                if session.Process and process_name in session.Process.name():

                    # print(interface.GetMasterVolume())
                    interface.SetMasterVolume(percen / 100, None)


        except Exception as ex:
            print(ex)
            return False, str(ex)
        

    def _unMuteWithProcessName(self, process_name: str):
        return self._setMuteStateWithProcessName(process_name, False)

