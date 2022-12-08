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

        self.loadFrames()

        self.ConnectFrame.pack(pady=40)



        # self.ConnectRememberChekbox.place(y=300, x=100)

    def loadFrames(self):

        self.ConnectFrame = tk.CTkFrame(self, width=400, height=500)
        self.ConnectIpInputState = tk.StringVar()
        self.ConnectIpInput = tk.CTkEntry(self.ConnectFrame, textvariable=self.ConnectIpInputState, width=250,
                                          height=40)
        self.ConnectIpInputLabel = tk.CTkLabel(self.ConnectFrame, text="Server ip")
        self.ConnectIpInputLabel.pack(pady=5)
        self.ConnectIpInput.pack(pady=5)
        self.ConnectPortInputState = tk.StringVar()
        self.ConnectPortInput = tk.CTkEntry(self.ConnectFrame, width=250, height=40,
                                            textvariable=self.ConnectPortInputState)
        self.ConnectPortInputLabel = tk.CTkLabel(self.ConnectFrame, text="Server port")
        self.ConnectPortInputLabel.pack(pady=5)
        self.ConnectPortInput.pack(pady=5)
        self.ConnectPasswordInputState = tk.StringVar()
        self.ConnectPasswordInput = tk.CTkEntry(self.ConnectFrame, width=250, height=40,
                                                textvariable=self.ConnectPasswordInputState)
        self.ConnectPasswordInputLabel = tk.CTkLabel(self.ConnectFrame, text="Password")
        self.ConnectPasswordInputLabel.pack(pady=5)
        self.ConnectPasswordInput.pack(pady=5)
        self.ConnectRememberChekbox = tk.CTkCheckBox(self.ConnectFrame, text="Remember", height=50, width=50)
        self.ConnectRememberChekbox.pack(pady=20, anchor="w")
        self.ConnectErrorsLabel = tk.CTkLabel(self.ConnectFrame, text="")
        self.ConnectErrorsLabel.pack()
        self.ConnectConnectButton = tk.CTkButton(self.ConnectFrame, height=35, width=150, text="Connect",
                                                 command=self.Connect)
        self.ConnectConnectButton.pack()



    def Connect(self):
        # print(self.ConnectPasswordInputState.get())
        # self.ConnectErrorsLabel.configure(text="has")
        password = self.ConnectPasswordInputState.get()
        ip = self.ConnectIpInputState.get()
        port = self.ConnectPortInputState.get()
        try:
            client.connectSocket(ip, port, password)
        except:
            self.ConnectErrorsLabel.configure(text="Uncorect ip or port. Chek if server controller is running")
            self.ConnectIpInputState.set("")
            self.ConnectPortInputState.set("")
        # time.sleep(1)
        result = client.send_v2(classes.HandShake(password.encode()))[0]
        print(result)
        if result == b"BAD":
            self.ConnectErrorsLabel.configure(text="Uncorrect password")
            self.ConnectPasswordInputState.set("")
        if result == b"GOOD":
            self.password=password
            self.ConnectFrame.forget()
            self.MainMenu()

    def MainMenu(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.geometry("700x300")
        self.title("Control panel")
        self.MainFrame = tk.CTkFrame(self, width=140, corner_radius=0)
        self.MainFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.MainFrame.grid_rowconfigure(4, weight=1)
        MainServerListFrame = tk.CTkFrame(self.MainFrame, height=300)
        MainServerListFrame.grid(row=0, column=0)
        lable = tk.CTkButton(MainServerListFrame, text="safsdgf")
        lable.place(y=10, x=10)

        MainServerInfoFrame = tk.CTkFrame(self.MainFrame, height=300, width=400)
        MainServerInfoFrame.grid(row=0, column=1, padx=40, pady=10)
        self.MainFrame.pack()


if __name__ == "__main__":
    interface = App()
    interface.mainloop()