# Andrea Diamantini
# UDP GUI Client


import wx
import wxasync

import asyncio
import socket
import sys


class Esempio(wx.Frame):

    def __init__(self, name, clientAddress, serverAddress):
        super().__init__(None, title="Async UDP Client Chat")

        # member variables
        self.name = name
        self.clientAddress = clientAddress
        self.serverAddress = serverAddress

        # The NETWORK SOCKET async part --------
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(clientAddress)
        self.udp_socket.setblocking(False)

        self.loop = asyncio.get_running_loop()

        self.udp_socket.sendto(("CONNECT " + self.name).encode(), self.serverAddress)

        # The GUI part -------------------------
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.msgList = wx.ListBox(panel)
        hbox1.Add(self.msgList, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox1, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc1 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        sendButton = wx.Button(panel, label="SEND")

        # AsyncBind (instead of usual Bind)
        wxasync.AsyncBind(wx.EVT_TEXT_ENTER, self.sendMessage, self.tc1)
        wxasync.AsyncBind(wx.EVT_BUTTON, self.sendMessage, sendButton)

        hbox2.Add(self.tc1, proportion=1, flag=wx.ALL, border=5)
        hbox2.Add(sendButton, proportion=0, flag=wx.ALL, border=5)
        vbox.Add(hbox2, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)

        self.SetMinSize((200, 300))
        panel.SetSizer(vbox)
        self.Centre()

        # Adesso inizia la ricezione!
        wxasync.StartCoroutine(self.recvMessage, self)

    async def sendMessage(self, evt):
        messaggio = self.tc1.Value.strip()

        if messaggio:
            # Invia il messaggio
            self.udp_socket.sendto(messaggio.encode(), self.serverAddress)
            self.msgList.Append(f"[IO] {messaggio}")

        self.tc1.Clear()
        return

    async def recvMessage(self):

        while True:
            data = await self.loop.sock_recv(self.udp_socket, 1024)
            messaggio = data.decode()
            self.msgList.Append(messaggio)

        return


# ---------------------------------------------------------------------------------


async def runGuiClient(clientAddress, serverAddress):

    print(f"Ciaone da {clientAddress} che invia a {serverAddress}")

    # THE App...
    app = wxasync.WxAsyncApp()

    diag = wx.TextEntryDialog(None, "Inserisci nome")
    if diag.ShowModal() != wx.ID_OK:
        sys.exit(0)

    name = diag.GetValue()

    window = Esempio(name, clientAddress, serverAddress)
    window.Show()

    app.SetTopWindow(window)
    await app.MainLoop()


# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    import random

    clientPort = random.randint(20001, 50000)
    clientAddress = ("127.0.0.1", clientPort)

    serverAddress = ("127.0.0.1", 20000)

    try:
        asyncio.run(runGuiClient(clientAddress, serverAddress))

    # serve per chiudere CORRETTAMENTE cliccando CTRL + C
    except KeyboardInterrupt:
        print("[INFO] Chiusura GUI client")
