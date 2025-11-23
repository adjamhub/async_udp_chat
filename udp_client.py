# Andrea Diamantini
# UDP Client

import socket
import asyncio


async def sendMessage(udp_socket, serverAddress):
    """Funzione per inviare messaggi al server"""

    loop = asyncio.get_running_loop()

    print(f"[INFO] Invierò messaggi a {serverAddress}")
    print("[INFO] Scrivi un messaggio e premi INVIO (o /quit per uscire)")
    print("-" * 50)

    while True:
        # Legge input in modo asincrono
        messaggio = await loop.run_in_executor(None, input)
        messaggio = messaggio.strip()

        if messaggio.lower() == "/quit":
            print("[INFO] Chiusura peer... Adesso premi CTRL + C")
            break

        if messaggio:
            # Invia il messaggio
            udp_socket.sendto(messaggio.encode(), serverAddress)
            print(f"[IO] {messaggio}")

    udp_socket.close()


async def recvMessage(udp_socket):
    """Funzione per ricevere i messaggi inviati dal server"""

    loop = asyncio.get_running_loop()

    print(f"[INFO] In ascolto su {udp_socket.getsockname()}")

    while True:
        data = await loop.sock_recv(udp_socket, 1024)
        messaggio = data.decode()
        print(messaggio)

    udp_socket.close()


async def runClient(clientAddress, serverAddress):

    name = input("Nome: ")

    # Crea il socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(clientAddress)
    udp_socket.setblocking(False)

    udp_socket.sendto(("CONNECT " + name).encode(), serverAddress)

    # Esegue entrambe le funzioni contemporaneamente
    await asyncio.gather(
        sendMessage(udp_socket, serverAddress), 
        recvMessage(udp_socket),
    )


if __name__ == "__main__":

    import random

    clientPort = random.randint(20001, 50000)
    clientAddress = ("127.0.0.1", clientPort)

    serverAddress = ("127.0.0.1", 20000)

    try:
        # serve per eseguire il processo in maniera asincrona
        asyncio.run(runClient(clientAddress, serverAddress))

    # serve per chiudere CORRETTAMENTE cliccando CTRL + C
    except KeyboardInterrupt:
        print("[INFO] Chiusura client")
