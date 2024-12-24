# Cisco Sentinel

**Cisco Sentinel** is a monitoring application for Cisco network devices that visualizes key performance metrics like CPU usage, memory usage, and traffic statistics using SNMP (Simple Network Management Protocol). This application provides real-time graphical insights into device performance and is developed with Python using `tkinter`, `matplotlib`, `asyncio`, and `pysnmp`.

## Features
- **Real-time monitoring**: Continuously tracks device CPU, memory, and network traffic (in and out) data.
- **Graphical interface**: Displays real-time graphs of system statistics.
- **SNMP support**: Fetches data from Cisco devices using SNMP for monitoring.
- **Dynamic updates**: The interface and graphs are updated every second with new data from the connected device.
- **Device connectivity**: Connects to devices via IP address to retrieve system stats.

## Requirements
- Python 3.6+
- Required Python libraries:
  - `tkinter` (for the GUI)
  - `asyncio` (for asynchronous operations)
  - `matplotlib` (for graph plotting)
  - `pysnmp` (for SNMP communication)
  - `async_tkinter_loop` (for asynchronous integration with tkinter)

You can install the required libraries with the following command:

```bash
pip install matplotlib pysnmp async_tkinter_loop
```

## Installation
1. Clone or download the repository to your local machine.
2. Install the necessary Python packages (as mentioned above).
3. Run the `CiscoSentinel` application:

```bash
python cisco_sentinel.py
```

## Usage
- Launch the application and enter the IP address of your Cisco device in the input field.
- Press "Connect" to initiate the SNMP connection to the device.
- The application will display graphs of the device's CPU usage, memory usage, and traffic in and out over time.
- The data is refreshed every second and the graphs are updated accordingly.

## Interface Overview
- **IP Address Input**: Allows the user to enter the IP address of the Cisco device to connect to.
- **Connect Button**: Establishes the SNMP connection to the device and starts the monitoring process.
- **Connection Status**: Displays the current connection status (Connected or Disconnected) in green or red.
- **Graphs**: Real-time graphs displaying:
  - CPU Usage (%)
  - Memory Usage (%)
  - Traffic In (kbps)
  - Traffic Out (kbps)

## How it Works
1. The app fetches data from the Cisco device using SNMP OIDs (Object Identifiers):
   - CPU Usage: `1.3.6.1.4.1.9.9.109.1.1.1.1.8.1`
   - Memory Usage: `1.3.6.1.4.1.9.9.48.1.1.1.5.1` (used) and `1.3.6.1.4.1.9.9.48.1.1.1.6.1` (free)
   - Traffic In/Out: `1.3.6.1.2.1.2.2.1.10.1` (in) and `1.3.6.1.2.1.2.2.1.16.1` (out)
   
2. Every second, the application fetches the data, calculates traffic rates (kbps), and updates the graphs accordingly.

3. The data is displayed on a GUI with dynamic plotting using `matplotlib`.

## Customization
- You can modify the SNMP OIDs to match those of other devices or add new metrics.
- The appearance of the graphs can be customized using `matplotlib` configurations.

## Troubleshooting
- **Connection Issues**: Make sure the device IP is correct and reachable from the machine running Cisco Sentinel.
- **SNMP Configuration**: Ensure that SNMP is enabled on the Cisco device and is accessible using the "public" community string.
  
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Developed by Parsa Rostamzadeh**