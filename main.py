# Andrea Diamantini
# UDP async CHAT

import argparse
import sys
import asyncio

# local import
import udp_peer
import udp_server
import udp_client

# peer 1
peer1_address = ("127.0.0.1", 10001)

# peer 2
peer2_address = ("127.0.0.1", 10002)

# server
server_address = ("127.0.0.1", 20000)

# ---------------------------------------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--peer", help="peer number. Can be 1 or 2", type=int)

    parser.add_argument("--server", help="run in server mode", action="store_true")

    parser.add_argument("--client", help="run in client mode", action="store_true")

    parser.add_argument("--gui", help="run in GUI client mode", action="store_true")

    args = parser.parse_args()

    try:
        if args.peer:
            print("[INFO] peer mode")
            peerNumber = args.peer
            if peerNumber == 1:
                asyncio.run(udp_peer.runPeer(peer1_address, peer2_address))
            elif peerNumber == 2:
                asyncio.run(udp_peer.runPeer(peer2_address, peer1_address))
            else:
                print(
                    f"peer number can be 1 for {peer1_address} or 2 for {peer2_address}"
                )
                sys.exit(1)

        if args.server:
            print("[INFO] server mode")
            asyncio.run(udp_server.runServer(server_address))
            sys.exit(0)

        import random

        clientPort = random.randint(20001, 50000)
        client_address = ("127.0.0.1", clientPort)

        if args.client:
            print("[INFO] client mode")
            asyncio.run(udp_client.runClient(client_address, server_address))
            sys.exit(0)

        if args.gui:
            print("[INFO] GUI client mode")
            # included here cause of the OPTIONAL wx deps
            import udp_gui_client

            asyncio.run(udp_gui_client.runGuiClient(client_address, server_address))
            sys.exit(0)

    except KeyboardInterrupt:
        print("[INFO] chiudo tutto!!!")


# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
