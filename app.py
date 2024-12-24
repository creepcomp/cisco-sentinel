import tkinter as tk

class CiscoSentinel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Network Device Health Monitor")
        self.geometry("1200x800")

        self.snmp_host = tk.StringVar(value="192.168.10.100")
        self.connection_status = tk.StringVar(value="Disconnected")

        self.create_ui()

    def create_ui(self):
        # Frame for IP and status
        frame = tk.Frame(self)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Device IP Address:").pack(side="left", padx=5)
        tk.Entry(frame, textvariable=self.snmp_host).pack(side="left", padx=5)
        tk.Button(frame, text="Connect", command=self.connect).pack(side="left", padx=5)
        tk.Label(frame, text="Status:").pack(side="left", padx=5)

        self.status_label = tk.Label(frame, textvariable=self.connection_status, fg="red")
        self.status_label.pack(side="left", padx=5)

    def connect(self):
        if self.snmp_host.get():
            self.connection_status.set("Connected")
            self.status_label.config(fg="green")
        else:
            self.connection_status.set("Disconnected")
            self.status_label.config(fg="red")

if __name__ == "__main__":
    app = CiscoSentinel()
    app.mainloop()
