import socket
import threading
import requests

# ------------------ CONFIG ------------------ #
common_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3",
    139: "NetBIOS", 143: "IMAP",
    443: "HTTPS", 445: "SMB"
}

# ------------------ NETWORK SCAN ------------------ #
def scan_device(ip):
    try:
        hostname = "Unknown"
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            pass

        open_ports = []

        for port in common_ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(f"{port}({common_ports[port]})")
                s.close()
            except:
                pass

        if open_ports:
            print("\n[+] Device Found")
            print("IP:", ip)
            print("Hostname:", hostname)
            print("Open Ports:", ", ".join(open_ports))
            print("-" * 40)

    except:
        pass


def network_scan():
    base_ip = input("Enter base IP (e.g. 192.168.205): ")
    
    threads = []
    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        t = threading.Thread(target=scan_device, args=(ip,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


# ------------------ LINK LOOKUP ------------------ #
def link_lookup():
    domain = input("Enter website (e.g. google.com): ")

    try:
        ip = socket.gethostbyname(domain)
        print("\n[+] Domain Info")
        print("Domain:", domain)
        print("IP:", ip)

        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()

        if data.get("status") == "success":
            print("\n[+] Location Info")
            print("Country:", data.get("country"))
            print("City:", data.get("city"))
            print("ISP:", data.get("isp"))
        else:
            print("Location not found")

    except Exception as e:
        print("Error:", e)


# ------------------ MY IP ------------------ #
def my_ip():
    try:
        ip = requests.get("https://api64.ipify.org", timeout=5).text
        print("Your Public IP:", ip)
    except:
        print("Error fetching IP")


# ------------------ MENU ------------------ #
def main():
    while True:
        print("\n==== FINAL TOOLKIT ====")
        print("1. Network Scan")
        print("2. Link Lookup (Domain → IP + Location)")
        print("3. My Public IP")
        print("4. Exit")

        ch = input("Choose: ")

        if ch == "1":
            network_scan()
        elif ch == "2":
            link_lookup()
        elif ch == "3":
            my_ip()
        elif ch == "4":
            print("Exit...")
            break
        else:
            print("Invalid option")

# ------------------ RUN ------------------ #
if __name__ == "__main__":
    main()
