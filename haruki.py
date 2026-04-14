import os
import socket
import threading
import time
import sys
from datetime import datetime

# ------------------ AUTO INSTALL ------------------ #
def install(pkg):
    os.system(f"pip install {pkg} > /dev/null 2>&1")

try:
    import requests
except:
    install("requests")
    import requests

try:
    from colorama import Fore, init
except:
    install("colorama")
    from colorama import Fore, init

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress
except:
    install("rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress

init(autoreset=True)
console = Console()

# ------------------ SYSTEM ------------------ #
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ------------------ ANIMATION ------------------ #
def animated_title():
    text = "⚡ HARUKI NET TOOLKIT ⚡"
    for i in range(len(text)+1):
        print(Fore.GREEN + text[:i], end="\r")
        time.sleep(0.02)
    print(Fore.GREEN + text)

def glow_text(text):
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN]
    for i in range(4):
        print(colors[i] + text, end="\r")
        time.sleep(0.08)
    print(Fore.GREEN + text)

# ------------------ BANNER ------------------ #
def banner():
    clear()

    animated_title()

    print(Fore.GREEN + """
██╗  ██╗ █████╗ ██████╗ ██╗   ██╗██╗  ██╗██╗
██║  ██║██╔══██╗██╔══██╗██║   ██║██║ ██╔╝██║
███████║███████║██████╔╝██║   ██║█████╔╝ ██║
██╔══██║██╔══██║██╔══██╗██║   ██║██╔═██╗ ██║
██║  ██║██║  ██║██║  ██║╚██████╔╝██║  ██╗██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝
""")

    console.print(Panel.fit(
        "[bold green]HARUKI CONTROL PANEL[/bold green]\n"
        "[cyan]Instagram: @haru_ki_1[/cyan]",
        border_style="green"
    ))

# ------------------ CONFIG ------------------ #
common_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet",
    25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB"
}

# ------------------ LOG ------------------ #
def save_log(data):
    with open("haruki_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {data}\n")

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
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(str(port))
            s.close()

        if open_ports:
            console.print(f"[green][+] Device Found[/green]")
            console.print(f"[cyan]IP:[/cyan] {ip}")
            console.print(f"[magenta]Hostname:[/magenta] {hostname}")
            console.print(f"[yellow]Ports:[/yellow] {', '.join(open_ports)}")
            console.print("-" * 40)

            save_log(f"{ip} | {hostname} | {open_ports}")

    except:
        pass


def network_scan():
    base_ip = input(Fore.CYAN + "Enter base IP: ")
    threads = []

    try:
        with Progress() as progress:
            task = progress.add_task("[green]Scanning...", total=254)

            for i in range(1, 255):
                ip = f"{base_ip}.{i}"
                t = threading.Thread(target=scan_device, args=(ip,))
                threads.append(t)
                t.start()
                progress.update(task, advance=1)

            for t in threads:
                t.join()

        console.print("[green]✔ Scan Completed![/green]")

    except KeyboardInterrupt:
        console.print("[red]Scan Interrupted[/red]")

# ------------------ PORT SCAN ------------------ #
def port_scan():
    target = input(Fore.CYAN + "Enter IP or domain: ")
    console.print("[yellow]Scanning ports...[/yellow]")

    try:
        for port in common_ports:
            s = socket.socket()
            s.settimeout(0.5)
            if s.connect_ex((target, port)) == 0:
                console.print(f"[green][OPEN][/green] {port} ({common_ports[port]})")
            s.close()

    except KeyboardInterrupt:
        console.print("[red]Stopped[/red]")

# ------------------ LINK LOOKUP ------------------ #
def link_lookup():
    domain = input(Fore.CYAN + "Enter website: ")

    try:
        ip = socket.gethostbyname(domain)

        console.print(f"[cyan]Domain:[/cyan] {domain}")
        console.print(f"[yellow]IP:[/yellow] {ip}")

        data = requests.get(f"http://ip-api.com/json/{ip}").json()

        console.print(f"[magenta]Country:[/magenta] {data.get('country')}")
        console.print(f"[magenta]City:[/magenta] {data.get('city')}")
        console.print(f"[magenta]ISP:[/magenta] {data.get('isp')}")

    except:
        console.print("[red]Error[/red]")

# ------------------ MY IP ------------------ #
def my_ip():
    try:
        ip = requests.get("https://api64.ipify.org").text
        console.print(f"[green]Your IP:[/green] {ip}")
    except:
        console.print("[red]Error[/red]")

# ------------------ MATRIX MODE ------------------ #
def matrix_mode():
    clear()
    console.print("[green]Press CTRL+C to exit[/green]\n")

    chars = "01▓▒░#@$%&"

    try:
        while True:
            line = "".join([chars[ord(os.urandom(1)) % len(chars)] for _ in range(100)])
            console.print(f"[green]{line}[/green]")
            time.sleep(0.02)
    except KeyboardInterrupt:
        pass

# ------------------ MENU ------------------ #
def main():
    banner()

    try:
        while True:
            glow_text("==== HARUKI MENU ====")

            console.print(Panel(
                "[1] Network Scan\n"
                "[2] Port Scan\n"
                "[3] Link Lookup\n"
                "[4] My IP\n"
                "[5] Matrix Mode 😈\n"
                "[6] Refresh UI 🔄\n"
                "[7] Exit",
                title="HARUKI CONTROL PANEL",
                border_style="cyan"
            ))

            ch = input("➤ Choose: ")

            if ch == "1":
                network_scan()
            elif ch == "2":
                port_scan()
            elif ch == "3":
                link_lookup()
            elif ch == "4":
                my_ip()
            elif ch == "5":
                matrix_mode()
            elif ch == "6":
                banner()
            elif ch == "7":
                break
            else:
                console.print("[red]Invalid[/red]")

    except KeyboardInterrupt:
        console.print("\n[red]Exit[/red]")
        sys.exit()

# ------------------ RUN ------------------ #
if __name__ == "__main__":
    main()
