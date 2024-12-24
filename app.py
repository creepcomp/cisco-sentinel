import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CiscoSentinel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Network Device Health Monitor")
        self.geometry("1200x800")

        self.snmp_host = tk.StringVar(value="192.168.10.100")
        self.connection_status = tk.StringVar(value="Disconnected")

        # Data for monitoring
        self.data = {
            'cpu': [],
            'memory': [],
            'traffic_in': [],
            'traffic_out': [],
            'time': []
        }

        self.create_ui()

    def create_ui(self):
        # Create plots
        self.fig, axs = plt.subplots(2, 2)
        self.ax_cpu, self.ax_memory, self.ax_traffic_in, self.ax_traffic_out = axs.flatten()

        # Plot configurations
        self.configure_plot(self.ax_cpu, "CPU Usage (%)", "CPU Usage (%)", (0, 100))
        self.configure_plot(self.ax_memory, "Memory Usage (%)", "Memory Usage (%)", (0, 100))
        self.configure_plot(self.ax_traffic_in, "Traffic In (kbps)", "Traffic In (kbps)", None)
        self.configure_plot(self.ax_traffic_out, "Traffic Out (kbps)", "Traffic Out (kbps)", None)

        self.fig.subplots_adjust(hspace=0.4, wspace=0.3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Frame for IP and status
        frame = tk.Frame(self)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Device IP Address:").pack(side="left", padx=5)
        tk.Entry(frame, textvariable=self.snmp_host).pack(side="left", padx=5)
        tk.Button(frame, text="Connect", command=self.connect).pack(side="left", padx=5)
        tk.Label(frame, text="Status:").pack(side="left", padx=5)

        self.status_label = tk.Label(frame, textvariable=self.connection_status, fg="red")
        self.status_label.pack(side="left", padx=5)

    def configure_plot(self, ax, title, ylabel, ylim):
        ax.set_title(title)
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel(ylabel)
        if ylim:
            ax.set_ylim(ylim)

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
