import threading
import time

import customtkinter as tk
import client
import classes

tk.set_appearance_mode("Dark")


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.title("Connect menu")

        self.password=None
        self.host=None
        self.port=None
        self.Connect()
        # self.MainMenu()
        # self.loadFrames()
        # self.test()
        # self.ConnectFrame.pack(pady=40)


    def Connect(self):
        self.ConnectFrame = tk.CTkFrame(self, width=400, height=500)
        self.ConnectFrame.pack(pady=40)
        self.ConnectIpInputState = tk.StringVar()
        ConnectIpInput = tk.CTkEntry(self.ConnectFrame, textvariable=self.ConnectIpInputState, width=250,
                                     height=40)
        ConnectIpInputLabel = tk.CTkLabel(self.ConnectFrame, text="Server ip")
        ConnectIpInputLabel.pack(pady=5)
        ConnectIpInput.pack(pady=5)
        self.ConnectPortInputState = tk.StringVar()
        ConnectPortInput = tk.CTkEntry(self.ConnectFrame, width=250, height=40,
                                       textvariable=self.ConnectPortInputState)
        ConnectPortInputLabel = tk.CTkLabel(self.ConnectFrame, text="Server port")
        ConnectPortInputLabel.pack(pady=5)
        ConnectPortInput.pack(pady=5)
        self.ConnectPasswordInputState = tk.StringVar()
        ConnectPasswordInput = tk.CTkEntry(self.ConnectFrame, width=250, height=40,
                                           textvariable=self.ConnectPasswordInputState)
        ConnectPasswordInputLabel = tk.CTkLabel(self.ConnectFrame, text="Password")
        ConnectPasswordInputLabel.pack(pady=5)
        ConnectPasswordInput.pack(pady=5)
        ConnectRememberChekbox = tk.CTkCheckBox(self.ConnectFrame, text="Remember", height=50, width=50)
        ConnectRememberChekbox.pack(pady=20, anchor="w")
        self.ConnectErrorsLabel = tk.CTkLabel(self.ConnectFrame, text="")
        self.ConnectErrorsLabel.pack()
        ConnectConnectButton = tk.CTkButton(self.ConnectFrame, height=35, width=150, text="Connect",
                                            command=self.ConnectResponce)
        ConnectConnectButton.pack()

    def ConnectResponce(self):
        password = self.ConnectPasswordInputState.get()
        ip = self.ConnectIpInputState.get()
        port = self.ConnectPortInputState.get()
        try:
            client.connectSocket(ip, port)
        except:
            self.ConnectErrorsLabel.configure(text="Uncorect ip or port. Chek if server controller is running")
            self.ConnectIpInputState.set("")
            self.ConnectPortInputState.set("")
        result = client.send_v2(classes.HandShake(password.encode()))[0]
        print(result)
        time.sleep(1)
        if result == b"BAD":
            self.ConnectErrorsLabel.configure(text="Uncorrect password")
            self.ConnectPasswordInputState.set("")
        if result == b"GOOD":
            self.password=password

            self.serversCount = client.send_v2(classes.GetServers(0, password))
            self.ConnectFrame.forget()
            self.MainMenu()

    def ShowInfo(self, id):
        pass
    def MainMenu(self):

        self.geometry("570x320")
        self.title("Control panel")
        self.MainFrame = tk.CTkFrame(self, width=570, height=320, corner_radius=0)

        self.MainFrame.pack()

        MainServerListFrame = tk.CTkFrame(self.MainFrame, height=300, width=150)
        MainServerListFrame.grid(row=0, column=0, padx=10)
        reload = tk.CTkButton(MainServerListFrame, text="reload", command=lambda: threading.Thread(target=asyncReload).start())
        reload.pack(pady=10, padx=10)
        btn1 = tk.CTkButton(MainServerListFrame, text="1", command=lambda: editPage(0))
        btn1.pack(pady=10, padx=10)
        btn2 = tk.CTkButton(MainServerListFrame, text="2", command=lambda: editPage(1))
        btn2.pack(pady=10, padx=10)
        self.servers = client.getServers(self.host)#[:self.serversCount]
        self.corid=0
        def asyncReload():
            self.servers = client.getServers(self.host)
            editPage(self.corid)

        def editPage(id):
            self.curid=id
            print(self.curid)
            for i in self.prewPage:
                i.destroy()
            pages = []
            for i in self.servers:
                if i[1].online:
                    status = "Active"
                else:
                    status = "Offline"
                page = tk.CTkFrame(self.MainFrame)
                state = tk.CTkLabel(page, text=f"Server status: {status}")
                state.pack(anchor="n", padx=10, pady=10)
                if i[1].online:
                    btn = tk.CTkButton(page, text="Start", command= lambda: print("hui"))
                else: btn = tk.CTkButton(page, text="Stop", command= lambda: print("dwa huja"))
                btn.pack()
                players= tk.CTkLabel(page, text=f"Online players: {i[1].current_players}")
                players.pack(padx=10, pady=10)
                motd = tk.CTkLabel(page, text=f"Motd: {i[1].stripped_motd}")
                motd.pack(padx=10, pady=10)
                pages.append(page)
            self.prewPage = pages

            pages[id].grid(row=0, column=1, padx=10, pady=10)




        # lable = tk.CTkButton(MainServerListFrame, text="safsdgf")
        # lable.pack(pady=10, padx=10)
        # lable1 = tk.CTkButton(MainServerListFrame, text="safsdgf1")
        # lable1.pack(pady=10)

        MainServerInfoFrame = tk.CTkFrame(self.MainFrame, height=300, width=400)
        self.prewPage = [MainServerInfoFrame]
        MainServerInfoFrame.grid(row=0, column=1, padx=10, pady=10)
        # self.MainFrame.grid()
    def update(self):
        self.MainFrame.destroy()
        self.MainMenu()



if __name__ == "__main__":
    interface = App()
    interface.mainloop()