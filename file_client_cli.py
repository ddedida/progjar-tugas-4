import os
import socket
import json
import base64
import logging
import struct

server_address = ('0.0.0.0', 8889)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        command_bytes = command_str.encode()
        command_length = struct.pack('!I', len(command_bytes))

        sock.sendall(command_length)
        sock.sendall(command_bytes)

        data_received = b""
        while True:
            data = sock.recv(4096)
            if data:
                data_received += data
                if b"\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received.decode())
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {str(e)}")
        return False
    finally:
        sock.close()

def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print("Daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb') as fp:
            fp.write(isifile)
        print(f"{namafile} berhasil diunduh.")
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    try:
        if filename == '':
            return None
        with open(filename, "rb") as fp:
            isifile = base64.b64encode(fp.read()).decode()

        command_str = f"UPLOAD {os.path.basename(filename)} {isifile}"
        hasil = send_command(command_str)
        if hasil["status"] == "OK":
            print(hasil["data"])
            return True
        else:
            print("Gagal")
            return False
    except Exception as e:
        logging.warning(f"Error during file upload: {str(e)}")
        return False
    
def remote_delete(filename=""):
    try:
        command_str = f"DELETE {filename}"
        hasil = send_command(command_str)
        if hasil["status"] == "OK":
            print(hasil["data"])
            return True
        else:
            print("Gagal")
            return False
    except Exception as e:
        logging.warning(f"Error during file upload: {str(e)}")
        return False

if __name__ == '__main__':
    server_address = ('0.0.0.0', 8889)
    # remote_upload('donalbebek.jpg')
    # remote_upload('rfc2616.pdf')
    # remote_list()
    # remote_get('donalbebek.jpg')
    # remote_get('rfc2616.pdf')
    # remote_delete('donalbebek.jpg')
    # remote_delete('rfc2616.pdf')