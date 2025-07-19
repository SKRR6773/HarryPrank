import client.shared as shared



def closeProcess():
    shared.is_running = False

    if shared.hand_shake:
        shared.hand_shake.close()


    if shared.client:
        shared.client.close()

