# Andrea Diamantini
# async UDP peer

import asyncio
import socket


async def ricevi_messaggi(localAddress):
    """Funzione che riceve e visualizza i messaggi UDP in arrivo"""
    loop = asyncio.get_running_loop()

    # Crea il socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(localAddress)
    udp_socket.setblocking(False)

    print(f"[INFO] In ascolto su {localAddress}")

    while True:
        data = await loop.sock_recv(udp_socket, 1024)
        messaggio = data.decode()
        print(f"\n[L'ALTRO] {messaggio}")


async def invia_messaggi(remoteAddress):
    """Funzione che legge l'input dell'utente e invia messaggi UDP"""
    loop = asyncio.get_running_loop()

    # Crea il socket UDP per l'invio
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"[INFO] Invierò messaggi a {remoteAddress}")
    print("[INFO] Scrivi un messaggio e premi INVIO (o /quit per uscire)")
    print("-" * 50)

    while True:
        # Legge input in modo asincrono
        messaggio = await loop.run_in_executor(None, input)
        messaggio = messaggio.strip()

        if messaggio:
            # Invia il messaggio
            udp_socket.sendto(messaggio.encode(), remoteAddress)
            print(f"[IO] {messaggio}")

    udp_socket.close()


async def runPeer(localAddress, remoteAddress):

    # Esegue entrambe le funzioni contemporaneamente
    await asyncio.gather(
        ricevi_messaggi(localAddress),
        invia_messaggi(remoteAddress)
    )


if __name__ == "__main__":

    # peer 1
    localAddress = ("127.0.0.1", 20001)

    # peer 2
    remoteAddress = ("127.0.0.1", 20002)

    try:
        # serve per eseguire il processo in maniera asincrona
        asyncio.run(runPeer(localAddress, remoteAddress))

    # serve per chiudere CORRETTAMENTE cliccando CTRL + C
    except KeyboardInterrupt:
        print("\n[INFO] Peer terminato")
