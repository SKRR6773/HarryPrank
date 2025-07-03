import platform


is_linux = "linux" in platform.platform().lower()


print("IS: " + "linux" if is_linux else "windows")