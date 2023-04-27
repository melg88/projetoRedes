import socket  # Biblioteca para implementar sockets
import os  # Biblioteca para navegar em pastas
import base64  # É necessário que os binários sejam modificados para base64

# Configurações do cliente
HOST = 'localhost'  # Endereço IP do servidor
PORT = 8080  # Porta do servidor
BUFFER_SIZE = 1024  # Tamanho do buffer de leitura
REQUEST = {
    'Docs': "/Docs",
    'ProjetoRedes': '/Docs/ProjetoRedes.pdf',
    'Photos': '/Photos',
    'all': '/Photos/all.jpg',
    'ob': '/Photos/obito.jpg',
    'fem': '/Photos/sakura.jpg',
    'Photos': '/Photos/reuniao.jpg',
    'secret doc': '/secret_doc',
    'secret user': '/secret_doc/user',
    'secret photo': '/secret_photo',
    'secret gow': '/secret_photo/gow.png',
    'http10': '505',
    'Docs': "/Docs/naruto.mp3",
    'Docs': "/Docs/naruto.mp4",
    'Docs': "/Docs/naotemnobrasil.jpg",
    'badRequest': "/Photos/all.jpg"
}

# envia request normal


def request(client_socket, file_path):
    # Requisição HTTP/1.1 com conexão persistente
    request = f'GET {file_path} HTML\Server HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\n\r\n'
    client_socket.send(request.encode())

# envia request para teste 505


def request505(client_socket):
    # Requisição HTTP/1.1 com conexão persistente
    request = f'GET / HTML\Server HTTP/1.0\r\nHost: localhost\r\nConnection: keep-alive\r\n\r\n'
    client_socket.send(request.encode())

# Função para decodificar os dados em base64


def request400(client_socket):
    # Requisição HTTP/1.1 com conexão persistente
    request = f'POST / HTML\Server HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\n\r\n'
    client_socket.send(request.encode())


def decode_base64(dados_base64):
    while len(dados_base64) % 4 != 0:
        # Adicionar caracteres de padding '=' até que seja múltiplo de 4
        dados_base64 += b'='
    dados_binarios = base64.b64decode(dados_base64)
    return dados_binarios


def run_client():
    # Cria o socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.settimeout(5)
    print(f'Conectado ao servidor {HOST}:{PORT}')

    for dir in REQUEST:

        print(REQUEST.get(dir))
        if dir != 'http10' and dir != 'badRequest':
            request(client_socket, REQUEST.get(dir))
        elif dir == 'http10':
            request505(client_socket)
        else:
            request400(client_socket)
        # Receber a resposta do servidor
        response = client_socket.recv(BUFFER_SIZE).decode()

        if not response:
            break  # Sai do loop se não houver mais dados

        if "Transfer-Encoding: chunked" in response:
            # Tamanho total do arquivo em bytes
            total_size = int(response.split(
                'Content-Length: ')[1].split('\r\n')[0])
            file_path = response.split('File-Path: ')[1].split('\r\n')[0]
            downloaded_size = 0  # Tamanho baixado até o momento em bytes
            file_name = os.path.basename(file_path)
            with open(file_name, 'wb') as file:
                while True:

                    try:
                        # Receber o próximo chunk de dados
                        chunk = client_socket.recv(1024)
                        chunk64 = decode_base64(chunk)
                        file.write(chunk64)
                        downloaded_size += len(chunk64)

                        # Calcula o progresso do download
                        progress = (downloaded_size / total_size) * 100
                        print(
                            f'Downloaded: {downloaded_size} bytes / Total: {total_size} bytes ({progress:.2f}%)')
                    # Verificar se chegou ao final do arquivo
                    except TimeoutError:
                        break
            print('Download completo.')
        else:
            print(response)

    # Fechar a conexão com o servidor
    client_socket.close()


if __name__ == '__main__':
    run_client()
