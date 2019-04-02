import socket
import pyaudio
from multiprocessing import Process

CHUNK = 1024
CHANNEL = 2
FORMAT = pyaudio.paInt16
RATE = 44100
p = pyaudio.PyAudio()
stream_recv = p.open(format=FORMAT, channels=CHANNEL, rate=RATE, output=True, frames_per_buffer=CHUNK)
stream_send = p.open(format=FORMAT, channels=CHANNEL, rate=RATE, input=True, frames_per_buffer=CHUNK)


def recv_data(conn):
    while True:
        data = conn.recv(CHUNK * 4)
        print("Received data {}".format(len(data)))
        stream_recv.write(data)


def send_data(conn):
    while True:
        data = stream_send.read(CHUNK)
        print("Sent data {}".format(len(data)))
        conn.sendall(data)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    HOST = s.getsockname()[0]
    PORT = 54321
    s.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    sock.bind((HOST, PORT))
    sock.listen()
    conn, addr = sock.accept()
    print('Connected to {}:{}'.format(addr[0], addr[1]))
    recv = Process(target=recv_data, args=(conn,))
    send = Process(target=send_data, args=(conn,))
    recv.start()
    send.start()
    recv.join()
    send.join()
