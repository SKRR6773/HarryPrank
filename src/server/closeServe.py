import server.shared as shared



def closeServ():
    
    if shared.server:
        shared.server.close()


    if shared.hello_client:
        shared.hello_client.close()