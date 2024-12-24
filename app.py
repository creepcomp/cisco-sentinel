import tkinter as tk
import time
import asyncio
from pysnmp.hlapi.asyncio import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from async_tkinter_loop import async_handler, async_mainloop

class CiscoSentinel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cisco Sentinel (Developed by Parsa Rostamzadeh)")
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

        # Previous data for calculating traffic rates
        self.prev_data = {
            'traffic_in': 0.0,
            'traffic_out': 0.0,
            'time': time.time()
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

    async def snmp_get(self, oid):
        try:
            iterator = await get_cmd(
                SnmpEngine(),
                CommunityData("public", mpModel=0),
                await UdpTransportTarget.create((self.snmp_host.get(), 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
            )

            errorIndication, _, _, varBinds = iterator

            if errorIndication:
                return f"Error: {errorIndication}"
            return varBinds[0][1]
        except Exception as e:
            return f"Exception: {str(e)}"

    async def fetch_data(self):
        cpu_usage = await self.snmp_get("1.3.6.1.4.1.9.9.109.1.1.1.1.8.1")
        self.data['cpu'].append(float(cpu_usage))

        memory_used = float(await self.snmp_get("1.3.6.1.4.1.9.9.48.1.1.1.5.1"))
        memory_free = float(await self.snmp_get("1.3.6.1.4.1.9.9.48.1.1.1.6.1"))
        memory_percent = int((memory_used * 100) / (memory_used + memory_free))
        self.data['memory'].append(memory_percent)

        traffic_in = await self.snmp_get("1.3.6.1.2.1.2.2.1.10.1")
        traffic_out = await self.snmp_get("1.3.6.1.2.1.2.2.1.16.1")
        
        current_time = time.time()
        elapsed_time = current_time - self.prev_data['time']

        self.data['traffic_in'].append(float((float(traffic_in) - self.prev_data['traffic_in']) * 8 / elapsed_time) / 1000)
        self.data['traffic_out'].append(float((float(traffic_out) - self.prev_data['traffic_out']) * 8 / elapsed_time) / 1000)

        self.prev_data.update({
            'traffic_in': traffic_in,
            'traffic_out': traffic_out,
            'time': current_time
        })

        self.data['time'].append(current_time)
        self.update_graphs()

    def update_graphs(self):
        self.plot_data(self.ax_cpu, self.data['cpu'], "CPU Usage")
        self.plot_data(self.ax_memory, self.data['memory'], "Memory Usage")
        self.plot_data(self.ax_traffic_in, self.data['traffic_in'], "Traffic In")
        self.plot_data(self.ax_traffic_out, self.data['traffic_out'], "Traffic Out")

        self.canvas.draw()

    def plot_data(self, ax, data, label):
        ax.clear()
        ax.plot(self.data['time'], data, label=label)
        ax.set_title(f"{label} ({data[-1]:.2f})")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel(label)
        ax.legend()

    def connect(self):
        if self.snmp_host.get():
            self.connection_status.set("Connected")
            self.status_label.config(fg="green")
            self.start_monitoring()
        else:
            self.connection_status.set("Disconnected")
            self.status_label.config(fg="red")

    @async_handler
    async def start_monitoring(self):
        while True:
            await self.fetch_data()
            await asyncio.sleep(1)

if __name__ == "__main__":
    app = CiscoSentinel()
    async_mainloop(app)
