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

        self.ConnectFrame = tk.CTkFrame(self, width=400, height=500)
        self.ConnectFrame.pack(pady=40)
        self.ConnectIpInputState=tk.StringVar()
        self.ConnectIpInput = tk.CTkEntry(self.ConnectFrame, textvariable=self.ConnectIpInputState, width=250, height=40)
        self.ConnectIpInputLabel = tk.CTkLabel(self.ConnectFrame, text="Server ip")
        self.ConnectIpInputLabel.pack(pady=5)
        self.ConnectIpInput.pack(pady=5)
        self.ConnectPortInputState=tk.StringVar()
        self.ConnectPortInput = tk.CTkEntry(self.ConnectFrame, width=250, height=40, textvariable=self.ConnectPortInputState)
        self.ConnectPortInputLabel = tk.CTkLabel(self.ConnectFrame, text="Server port")
        self.ConnectPortInputLabel.pack(pady=5)
        self.ConnectPortInput.pack(pady=5)
        self.ConnectPasswordInputState=tk.StringVar()
        self.ConnectPasswordInput = tk.CTkEntry(self.ConnectFrame, width=250, height=40, textvariable=self.ConnectPasswordInputState)
        self.ConnectPasswordInputLabel = tk.CTkLabel(self.ConnectFrame, text="Password")
        self.ConnectPasswordInputLabel.pack(pady=5)
        self.ConnectPasswordInput.pack(pady=5)
        self.ConnectRememberChekbox = tk.CTkCheckBox(self.ConnectFrame, text="Remember", height=50, width=50)
        self.ConnectRememberChekbox.pack(pady=20, anchor="w")
        self.ConnectErrorsLabel= tk.CTkLabel(self.ConnectFrame, text="")
        self.ConnectErrorsLabel.pack()
        self.ConnectConnectButton = tk.CTkButton(self.ConnectFrame, height=35, width=150, text="Connect", command=self.Connect)
        self.ConnectConnectButton.pack()

        # self.ConnectRememberChekbox.place(y=300, x=100)

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
        time.sleep(1)
        result = client.send_v2(classes.HandShake(password.encode()))[0]
        print(result)
        if result == b"BAD":
            self.ConnectErrorsLabel.configure(text="Uncorrect password")
            self.ConnectPasswordInputState.set("")
        if result == b"GOOD":
            pass


if __name__ == "__main__":
    interface = App()
    interface.mainloop()