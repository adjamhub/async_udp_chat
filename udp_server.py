# Andrea Diamantini
# async UDP server

import asyncio
import socket


async def udpServer(serverAddress):
    """Funzione che implementa un chat server UDP in grado di ricevere msg e reinviarli a tutti"""

    clientList = {}

    loop = asyncio.get_running_loop()

    # Crea il socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(serverAddress)
    udp_socket.setblocking(False)

    print("UDP server up and listening")

    # Listen for incoming datagrams
    while True:
        data, address = await loop.sock_recvfrom(udp_socket, 1024)
        messaggio = data.decode()

        # procedura di connessione
        if messaggio.startswith("CONNECT"):
            wordList = messaggio.split()
            name = wordList[1]
            clientList[address] = name
            continue

        sender = clientList.get(address, "boh")
        msg = f"[{sender}] {messaggio}"
        print(msg)
        for addr in clientList:
            if addr != address:
                udp_socket.sendto(msg.encode(), addr)
                print(f"sending to {addr}")

    udp_socket.close()


async def runServer(serverAddress):

    # Esegue entrambe le funzioni contemporaneamente
    await asyncio.gather(
        udpServer(serverAddress),
    )


if __name__ == "__main__":

    # server address
    localAddress = ("127.0.0.1", 20001)

    try:
        # serve per eseguire il processo in maniera asincrona
        asyncio.run(runServer(localAddress))

    # serve per chiudere CORRETTAMENTE cliccando CTRL + C
    except KeyboardInterrupt:
        print("[INFO] Peer terminato")
