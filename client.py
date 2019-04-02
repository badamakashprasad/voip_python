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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = input("Enter the Server IP Address")
    PORT = 54321
    sock.connect((HOST, PORT))
    p = pyaudio.PyAudio()
    stream_recv = p.open(format=FORMAT, channels=CHANNEL, rate=RATE, output=True, frames_per_buffer=CHUNK)
    stream_send = p.open(format=FORMAT, channels=CHANNEL, rate=RATE, input=True, frames_per_buffer=CHUNK)
    recv = Process(target=recv_data, args=(sock,))
    send = Process(target=send_data, args=(sock,))
    recv.start()
    send.start()
    recv.join()
    send.join()
