import socket
import time

SERVIDOR = "137.131.178.229"
PORTA = 8080
GRUPO = "grupo08"


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

        resposta, guardar_tempo_servidor = dados.split("|")

        if resposta == "PONG":
            rtt = (time.time() - inicio) * 1000
            return rtt, guardar_tempo_servidor

        else:
            print("Resposta inesperada:", resposta)
            return None, None

    except socket.timeout:
        print("O tempo expirou")
        return None, None


def hello(sock, servidor, grupo):
    pacote = f"HELLO|grupo={grupo}|segment_size=512|file=small"

    print("Enviando:", pacote)

    sock.sendto(pacote.encode("utf-8"), servidor)

    try:
        sock.settimeout(5.0)

        dados, endereco_servidor = sock.recvfrom(65507)
        resposta = dados.decode("utf-8")

        print("Recebido:", resposta)

        campos = resposta.split("|")

        if campos[0] != "OK":
            print("Resposta inesperada:", resposta)
            return None

        resultado = {}

        for campo in campos[1:]:
            chave, valor = campo.split("=", 1)
            resultado[chave] = valor

        return resultado

    except socket.timeout:
        print("O tempo expirou")
        return None


def requisitar_segmento(sock, servidor, seq=0):
    pacote = f"REQ|seq={seq}"
    sock.sendto(pacote.encode("utf-8"), servidor)

    try:
        sock.settimeout(5.0)
        dados, endereco_servidor = sock.recvfrom(65507)

        separadores_encontrados = 0
        indice_corte = 0

        for i, byte in enumerate(dados):
            if byte == ord(b'|'):
                separadores_encontrados += 1
                if separadores_encontrados == 3:
                    indice_corte = i + 1
                    break

        payload = dados[indice_corte:]
        return payload

    except socket.timeout:
        print("o tempo expirou")
        return None

def main():
    cliente_socket = criar_socket()
    servidor = (SERVIDOR, PORTA)

    print("=== Tarefa 0 — RDT-UnB Explorer ===")
    print(f"Servidor: {SERVIDOR}:{PORTA}")
    print()

    # Passo 1 — PING
    print("[1] PING")

    rtt, tempo_servidor_anotado = ping(cliente_socket, servidor)

    if rtt is not None:
        print(f"    RTT: {rtt:.1f} ms")
        print(f"    Tempo servidor: {tempo_servidor_anotado}")
        print()

    # Passo 2 — HELLO
    print("[2] HELLO")

    info = hello(cliente_socket, servidor, GRUPO)

    if info is not None:
        file_size = int(info["file_size"])
        checksum = info["checksum"]
        total_segments = int(info["total_segments"])
        segment_size = int(info["segment_size"])

        print()
        print(f"    Arquivo:         small")
        print(f"    Tamanho arquivo: {file_size} bytes")
        print(f"    Checksum MD5:    {checksum}")
        print(f"    Total segmentos: {total_segments}")
        print(f"    Tamanho segmento: {segment_size} bytes")
        print()

    # Passo 3 — REQ
    print("[3] REQ seg=0")
    
    payload = requisitar_segmento(cliente_socket, servidor, seq=0)

    if payload is not None:
        tamanho_payload = len(payload)
        primeiros_8 = payload[:8]
        hex_str = " ".join(f"{b:02x}" for b in primeiros_8)

        print(f"    Payload recebido: {tamanho_payload} bytes")
        print(f"    Primeiros 8 bytes: {hex_str}")
    else:
        print("    Falha ao receber o payload.")


if __name__ == "__main__":
    main()