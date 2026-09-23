import socket
import time

SERVIDOR = "137.131.178.229"
PORTA    = 8080
GRUPO    = "grupo08"   

def criar_socket(timeout=5.0):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return cliente_socket

def ping(cliente_socket, servidor):
    # envia PING, mede RTT, retorna float em ms
    inicio = time.time()
    cliente_socket.sendto(b"PING", servidor)

    try:
        cliente_socket.settimeout(5.0)
        dados, endereco_servidor = cliente_socket.recvfrom(65507)
        dados = dados.decode()

        # print("dados:", dados) -> para testar 

        resposta, guardar_tempo_servidor = dados.split("|")

        if resposta == "PONG":
            rtt = (time.time() - inicio)*1000
            return rtt, guardar_tempo_servidor
        else:
            print("Resposta inesperada:", resposta)
            return None, None

    except socket.timeout:
        print("O tempo expirou")
        return None, None


def hello(sock, servidor, grupo):
    # envia HELLO, parseia OK, retorna dict com os campos
    ...

def requisitar_segmento(sock, servidor, seq=0):
    # envia REQ seq=0, recebe DATA, retorna bytes do payload
    ...

def main():
    cliente_socket = criar_socket()
    servidor = (SERVIDOR, PORTA)

    print("=== Tarefa 0 — RDT-UnB Explorer ===")
    print(f"Servidor: {SERVIDOR}:{PORTA}")
    print()

    # Passo 1 — PING
    rtt, tempo_servidor_anotado = ping(cliente_socket, servidor)

    #print(f"rtt:{rtt}, tempo:{tempo_servidor_anotado}") -> para testar

    # Passo 2 — HELLO
    ...

    # Passo 3 — REQ
    ...

if __name__ == "__main__":
    main()