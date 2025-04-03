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

            print(f"\n[{addr if addr else 'Host'}]: {message}\nYou: ", end="")

        except:
            break

def start_guest():
    host_ip = input("Enter host IP: ").strip()
    protocol = input("Choose protocol (TCP/UDP): ").strip().upper()

    if protocol == "TCP":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host_ip, 5000))
        print(f"[TCP] Connected to {host_ip}")

        # Start receiving messages in a separate thread
        threading.Thread(target=receive_messages, args=(client_socket, protocol)).start()

        while True:
            msg = input("You: ")
            if msg.lower() == "exit":
                client_socket.send(msg.encode())
                break
            client_socket.send(msg.encode())

        client_socket.close()

    elif protocol == "UDP":
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"[UDP] Ready to send messages to {host_ip}")

        threading.Thread(target=receive_messages, args=(udp_socket, protocol, (host_ip, 5001))).start()

        while True:
            msg = input("You: ")
            udp_socket.sendto(msg.encode(), (host_ip, 5001))
            if msg.lower() == "exit":
                break

        udp_socket.close()

    else:
        print("Invalid protocol. Choose TCP or UDP.")

if __name__ == "__main__":
    start_guest()
