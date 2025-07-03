from audio_manager.linux import AudioManager as AudioManagerLinux
from audio_manager.win import AudioManager as AudioManagerWin
from check_platform import is_linux


audio_manager = (AudioManagerLinux if is_linux else AudioManagerWin)()



def setAudio(percent: int):
    audio_manager.setPercent(percent)


def setUnMute(process_name: str):
    audio_manager.unMuteWithProcessName(process_name)


def setPercenProcess(process_name: str, percen: int):
    audio_manager.setPercenProcessName(process_name, percen)


if __name__ == "__main__":
    pass
    # setAudio(20)

    audio_manager.setSystemMute(**{
        "is_mute": not False
    })

    # setUnMute("")

    # setPercenProcess("ffplay", 100)




