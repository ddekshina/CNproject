import socket
import threading

def receive_messages(sock, protocol, addr=None):
    """Handles receiving messages from the other client."""
    while True:
        try:
            if protocol == "TCP":
                message = sock.recv(1024).decode()
            else:  # UDP
                message, addr = sock.recvfrom(1024)
                message = message.decode()
            
            if not message or message.lower() == "exit":
                print("\n[Connection Closed]")
                break

            print(f"\n[{addr if addr else 'Client'}]: {message}\nYou: ", end="")

        except:
            break

def start_host():
    ip = socket.gethostbyname(socket.gethostname())
    print(f"Your IP Address: {ip}")
    
    protocol = input("Choose protocol (TCP/UDP): ").strip().upper()

    if protocol == "TCP":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, 5000))
        server_socket.listen(1)
        print("[TCP] Waiting for connection...")

        conn, addr = server_socket.accept()
        print(f"[TCP] Connected to {addr}")

        # Start receiving messages in a separate thread
        threading.Thread(target=receive_messages, args=(conn, protocol)).start()

        while True:
            msg = input("You: ")
            if msg.lower() == "exit":
                conn.send(msg.encode())
                break
            conn.send(msg.encode())

        conn.close()
        server_socket.close()

    elif protocol == "UDP":
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((ip, 5001))
        print("[UDP] Waiting for messages...")

        threading.Thread(target=receive_messages, args=(udp_socket, protocol)).start()

        client_addr = None  # Store the address of the sender
        while True:
            msg = input("You: ")
            if client_addr:
                udp_socket.sendto(msg.encode(), client_addr)
            if msg.lower() == "exit":
                break

        udp_socket.close()

    else:
        print("Invalid protocol. Choose TCP or UDP.")

if __name__ == "__main__":
    start_host()
