# import re
#
# text = "[spark-worker-pool-1-thread-1/INFO]: [⚡] Starting process (process) \n [spark-worker-pool-1-thread-1/INFO]: [⚡] Sing process (process)"
#
# text = """[22:39:59] [spark-worker-pool-1-thread-1/INFO]: [⚡] TPS from last 5s, 10s, 1m, 5m, 15m:
# [22:39:59] [spark-worker-pool-1-thread-1/INFO]: [⚡]  *20.0, *20.0, *20.0, *20.0, *20.0
# [22:39:59] [spark-worker-pool-1-thread-1/INFO]: [⚡]
# [22:39:59] [spark-worker-pool-1-thread-1/INFO]: [⚡] Tick durations (min/med/95%ile/max ms) from last 10s, 1m:
# [22:39:59] [spark-worker-pool-1-thread-1/INFO]: [⚡]  5.6/11.7/17.1/42.6;  5.1/11.8/31.3/70.6
# [22:39:59] [spark-worker-pool-1-thread-1/INFO]: [⚡]
# [22:39:59] [spark-worker-pool-1-thread-1/INFO]: [⚡] CPU usage from last 10s, 1m, 15m:
# [22:39:59] [spark-worker-pool-1-thread-1/INFO]: [⚡]  20%, 16%, 20%  (system)
# [22:39:59] [spark-worker-pool-1-thread-1/INFO]: [⚡]  6%, 12%, 17%  (process)"""
#
# pattern = r"\[spark-worker-pool-1-thread-1/INFO\]: \[⚡\] (.*) \(process\)"
#
# match = re.findall(pattern, text, re.DOTALL)
#
# if match:
#     extracted_text = match[-1]
#     print(extracted_text)
# from mcipc.query import Client
# from mcipc.rcon.je import Client
#
# # with Client('127.0.0.1', 25565) as stat:
# #     print(dict(stat.stats(full=True)))
#
# with Client("127.0.0.1", 25575, passwd='1234') as cl:
#     s=dict(cl.co)
#     print(s)

# import tkinter as tk
# import mcipc.rcon.je
#
# # Connect to the Minecraft server
# # rcon = mcipc.rcon.Client("localhost", 25565, passwd='1234')
#
# # Create the main window
# root = tk.Tk()
# root.title("Minecraft Command Sender")
#
# # Create a text box for entering commands
# entry = tk.Entry(root)
# entry.pack()
#
# # Create a function for sending commands to the server
# def send_command():
#     command = entry.get()
#     with mcipc.rcon.Client("localhost", 25575, passwd='1234') as rcon:
#         response = rcon.run(command)
#         print(response)
#
# # Create a button for triggering the command sending
# button = tk.Button(root, text="Send", command=send_command)
# button.pack()
#
# # Start the main loop
# root.mainloop()
#
import tkinter as tk
from tkinter import ttk
from mcipc.rcon.je import Client

#Create the window
window = tk.Tk()
window.title("Minecraft Server Console")
window.geometry("600x400")
window.configure(background="black")

#Create the labels
ip_label = ttk.Label(window, text="IP Address:", font=("Verdana", 16), foreground="white", background="black")
ip_label.grid(row=0, column=0, padx=10, pady=10)

port_label = ttk.Label(window, text="Port:", font=("Verdana", 16), foreground="white", background="black")
port_label.grid(row=1, column=0, padx=10, pady=10)

command_label = ttk.Label(window, text="Command:", font=("Verdana", 16), foreground="white", background="black")
command_label.grid(row=2, column=0, padx=10, pady=10)

#Create the entry boxes
ip_entry = ttk.Entry(window, width=30)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

port_entry = ttk.Entry(window, width=30)
port_entry.grid(row=1, column=1, padx=10, pady=10)

command_entry = ttk.Entry(window, width=30)
command_entry.grid(row=2, column=1, padx=10, pady=10)

#Create the submit button
submit_button = ttk.Button(window, text="Submit", command=lambda: submit_command(ip_entry.get(), port_entry.get(), command_entry.get()))
submit_button.grid(row=3, column=1, padx=10, pady=10)

#Create the output box
output_box = tk.Text(window, width=50, height=20, font=("Verdana", 12), foreground="white", background="black")
output_box.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

#Function to submit the command
def submit_command(ip, port, command):
    with Client(ip, int(port), passwd='1234') as client:
        output_box.insert(tk.END, client.run(command))

#Run the window
window.mainloop()
