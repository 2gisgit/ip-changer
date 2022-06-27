import wmi
import tkinter as tk
from tkinter import messagebox
import socket as s
import getmac
import os
import subprocess

if os.name != "nt":
    messagebox.showwarning("Error", message="Your OS is not window.Sorry.")

else:
    output = subprocess.check_output("ipconfig")
    fw = open("ipconfig_log.txt","w")
    fr = open("ipconfig_log.txt","r")
    read = fr.readlines()
    if read == None:
        fw.write(output)
    def DhcpIpChanger():
        nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)

        # First network adaptor
        nic = nic_configs[0]

        # Enable DHCP
        nic.EnableDHCP()
        return True

    def StaticIpChanger():
        nic_configs = wmi.WMI('').Win32_NetworkAdapterConfiguration(IPEnabled=True)

        nic = nic_configs[0]

        ip = entryIP.get()
        subnetmask = entrySubnet.get()
        gateway = entryGateway.get()
        dns1, dns2 = entryDNS.get().split(" - ")
        
        a = nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
        b = nic.SetGateways(DefaultIPGateway=[gateway])
        c = nic.SetDNSServerSearchOrder([dns1, dns2])
        d = nic.SetDynamicDNSRegistration(FullDNSRegistrationEnabled=1)
        row_ip = s.gethostbyname(s.gethostname())
        rd = ["Wi-Fi","로컬 영역 연결","Loopback Pseudo-Interface 1"]
        for i in rd:
            try:
                cmd = f'netsh interface ip add neighbors "{i}" {row_ip} a0-b1-c2-d3-e4-f5'
                os.system(cmd)
            except Exception as e:
                print(e)
                continue

        e = getmac.get_mac_address()

        print(a)
        print(b)
        print(c)
        print(d)
        print(e)
        
        if [a[0], b[0], c[0], d[0], e[0]] == [0, 0, 0, 0, 0]:
    ##        messagebox.showinfo("Done", message="IP Succesfully Change")
            return True
        else:
            errorMessage = """Return error codes are:
    %s
    %s
    %s
    %s
    %s
    Detail information;
    You must give the administrator permission to run the program.
    https://docs.microsoft.com/windows/desktop/CIMWin32Prov/setdynamicdnsregistration-method-in-class-win32-networkadapterconfiguration
    """%(a[0],b[0],c[0],d[0],e[0])
            with open("./ErrorLog.txt","w") as f:
                f.write(errorMessage)
            messagebox.showwarning("Error", message="Error description in 'ipchanger.txt'.But,check yourt IP plz.")
            return False

    def IpChanger():
        if varRadio.get() == "dhcp":
            if DhcpIpChanger():
                messagebox.showinfo("Done", message="IP Succesfully Change")
        else:
            if StaticIpChanger():
                messagebox.showinfo("Done", message="IP Succesfully Change")

    def TrackRadioButton():
        if varRadio.get() == "dhcp":
            entryIP["state"] = "disable"
            entrySubnet["state"] = "disable"
            entryGateway["state"] = "disable"
            entryDNS["state"] = "disable"
            entryMacGateway["state"] = "disable"
        else:
            entryIP["state"] = "normal"
            entrySubnet["state"] = "normal"
            entryGateway["state"] = "normal"
            entryDNS["state"] = "normal"
            entryMacGateway['state'] = "normal"
            

    # main part
    top = tk.Tk()
    top.geometry("250x450+100+100")
    top.title("IP Changer")
    top.resizable(False, False)

    # radio buttons
    varRadio = tk.StringVar()
    radio1 = tk.Radiobutton(top, text="DHCP", variable=varRadio,
                                 value="dhcp", command=TrackRadioButton)
    radio1.pack()
    tk.Label(text="_"*44, fg="#888888").pack(pady=5)

    radio2 = tk.Radiobutton(top, text="Static", variable=varRadio,
                                 value="static", command=TrackRadioButton)
    radio2.pack()
    varRadio.set("dhcp")

    # IP entry
    tk.Label(text="IP").pack()
    entryIP = tk.Entry(top)
    entryIP.pack()
    c = wmi.WMI()
    for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
        for ip_address in interface.IPAddress:
            entryIP.insert(0, ip_address) if len(ip_address)<15 else entryIP.insert(0, "")

    # subnetmask entry
    tk.Label(text="\nSubnetmask").pack()
    entrySubnet = tk.Entry(top)
    entrySubnet.pack()
    entrySubnet.insert(0, "255.255.255.0")

    # gateway entry
    tk.Label(text="\nGateway").pack()
    entryGateway = tk.Entry(top)
    entryGateway.pack()
    entryGateway.insert(0, "172.30.1.254")

    # dns entry
    tk.Label(text="\nDNS").pack()
    entryDNS = tk.Entry(top)
    entryDNS.pack()
    entryDNS.insert(0, "168.126.63.1 - 168.126.63.2")

    #mac entry
    tk.Label(text="\nArpGateway").pack()
    entryMacGateway = tk.Entry(top)
    entryMacGateway.pack()
    entryMacGateway.insert(0, "a1-b2-c3-d4-e5-f6")

    tk.Label(text=" ").pack()

    btnOK = tk.Button(top, text="Change", command=IpChanger)
    btnOK.pack()

    tk.Label(text=" ").pack()

    TrackRadioButton()

    messagebox.showwarning("Warning", message="After change your IP, check 'ipconfig_log.txt' to recover your Internet connection.")
    
    top.mainloop()
