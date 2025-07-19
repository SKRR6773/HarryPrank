import keyboard



keyboard.on_press(lambda e: print(e.to_json()))
keyboard.wait()


