# Andrea Diamantini
# UDP async CHAT

import argparse
import asyncio
import sys

# local import
import async_udp_chat.udp_client
import async_udp_chat.udp_server

# server
server_port = 22222

# ---------------------------------------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="run in server mode", action="store_true")

    parser.add_argument("--client", help="run in client mode", action="store_true")

    parser.add_argument("--gui", help="run in GUI client mode", action="store_true")

    args = parser.parse_args()

    try:
        if args.server:
            print("[INFO] server mode")
            asyncio.run(udp_server.runServer(server_port))
            sys.exit(0)

        if args.client:
            print("[INFO] client mode")
            asyncio.run(udp_client.runClient(server_port))
            sys.exit(0)

        if args.gui:
            print("[INFO] GUI client mode")
            # included here cause of the OPTIONAL wx deps
            import async_udp_chat.udp_gui_client

            asyncio.run(udp_gui_client.runGuiClient(server_port))
            sys.exit(0)

    except KeyboardInterrupt:
        print("[INFO] Closing!!!")


# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
