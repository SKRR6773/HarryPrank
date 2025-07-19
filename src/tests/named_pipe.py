# ไม่มีผลอะไร
import win32file


pipe_name = r'\\.\pipe\53b96bfe-1.101.2-main-sock'


handle = win32file.CreateFile(
    pipe_name, 
    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
    0,
    None,
    win32file.OPEN_EXISTING,
    0,
    None
)

print(win32file.ReadFile(handle, 4096))


handle.close()