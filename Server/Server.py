import socket  # Biblioteca para implementar sockets
import os  # Biblioteca para navegar em pastas
import mimetypes  # Biblioteca para descobrir o mime type
import base64  # É necessário que os binários sejam modificados para base64


# Configurações do servidor
HOST = 'localhost'
PORT = 8080
BUFFER_SIZE = 1024
ERROR_FILES_DIR = './error/'
# Mapeamento dos códigos de resposta e suas mensagens correspondentes
RESPONSES = {
    200: 'HTTP/1.1 200 OK\r\n',
    400: 'HTTP/1.1 400 Bad Request\r\n',
    403: 'HTTP/1.1 403 Forbidden\r\n',
    404: 'HTTP/1.1 404 Not Found\r\n',
    505: 'HTTP/1.1 505 Version Not Supported\r\n'
}


# Mapeamento dos diretorios e arquivos que nao podem ser acessados
RESTRICT = ['secret_doc', 'secret_photo', 'Server.py', 'Client.py', 'error']


def check_IsRestrict(file_path):

    # Obtém o nome da pasta do caminho fornecido
    file = os.path.basename(file_path)

    # Verifica se o nome da pasta está presente na lista Restrito
    if file in RESTRICT:
        return True  # Retorna True se o nome da pasta estiver presente na lista Restrito
    return False  # Retorna False se o nome da pasta não estiver presente na lista Restrito


# Função para gerar a resposta do servidor (precisa de melhoria)
def generate_response(client_socket, code):

    # Se não for 200, cria a pagina de erro, se ela nao existir no server e depois a envia para o cliente.
    if code != 200:
        check_error_page(code)
        send_file(client_socket, ERROR_FILES_DIR + str(code) + '.html', code)


def check_error_page(code):
    file = ERROR_FILES_DIR + str(code) + '.html'
    if not os.path.isfile(file):
        create_error_html(code)

# cria um index para o diretório


def create_error_html(code):
    # Criar arquivo index.html e escreve o conteúdo
    html_content = f'<html><body><h1>Error {code}</h1><p>{RESPONSES[code]}</p><a href="https://httpcats.com/{code}.jpg" target="_blank"><button>Clique aqui</button></a></body></html>'
    File = ERROR_FILES_DIR + str(code) + '.html'
    with open(File, 'w') as arquivo:
        arquivo.write(html_content)

    print(f"Arquivo {str(code)}.html criado com sucesso!")

# Função para codificar os dados binários em base64


def encode_base64(dados_binarios):
    dados_byte = dados_binarios.encode()
    dados_base64 = base64.b64encode(dados_byte)
    return dados_base64.decode('utf-8')

# Função para envio de arquivo em partes (streaming)


def send_file(client_socket, file_path, code=200):

    mime_type, encoding = mimetypes.guess_type(file_path)

    # Abrir o arquivo para leitura em modo de binário
    with open(file_path, 'rb') as file:
        # Configurar o tamanho total do arquivo para monitoramento de progresso
        file_size = os.path.getsize(file_path)
        fulladdres = os.path.abspath(file_path)
        get_response = RESPONSES.get(code)
        response_header = f'{get_response}Content-type: {mime_type}\r\nContent-Encoding: {encoding}\r\nContent-Length: {file_size}\r\nTransfer-Encoding: chunked\r\nConnection: keep-alive\r\nFile-Path: {fulladdres}\r\n\r\n'
        client_socket.send(response_header.encode())

        bytes_sent = 0

        # Ler e enviar o arquivo em partes (streaming)
        while True:
            # Ler o próximo pedaço do arquivo
            chunk = file.read(1024 * 1024)  # Ler 1MB por vez

            # Verificar se chegou ao final do arquivo
            if not chunk:
                break

            chunk_base64 = base64.b64encode(chunk)
            # Enviar o chunk como parte da resposta
            client_socket.send(chunk_base64)
            # client_socket.send(b'\r\n')

            # Atualizar o progresso
            bytes_sent += len(chunk_base64)
            progress = int(bytes_sent * 100 / file_size)
            print(f'Progresso: {progress}%')

    print('Envio completo')

# Função para gerar a listagem de diretório


def generate_directory_listing(directory):

    content = create_page_head(directory)
    files = os.listdir(directory)
    content += f'''
    <body>
        <h1>{'Home' if directory == '.' else 'Índice de Pasta - ' + directory}</h1>
        <ul>'''
    for file in files:

        # Não se deve listar pastas restritas
        if not check_IsRestrict(file) and file != 'index.html':
            content += f'<li><a href="{file}">{file}</a></li>'
    content += '''
        </ul>
    </body>
    </html>'''
    return content

# criação do header index.HTML


def create_page_head(directory):
    if directory == '.':
        directory = 'Home'
    header = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Index - {directory}</title>
        <style>
            /* Estilos CSS para a página de index */
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                margin-bottom: 10px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 5px;
            }}
            a {{
                text-decoration: none;
                color: #007bff;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    '''
    return header

# cria um index para o diretório


def create_index_html(directory):

    # Criar arquivo index.html e escrever conteúdo
    html_content = generate_directory_listing(directory)

    with open(directory+'/index.html', 'w') as arquivo:
        arquivo.write(html_content)

    print("Arquivo index.html criado com sucesso!")

# possui a strin do index no file_path e não existe como file? Cria a index


def check_index(file_path):
    is_index = 'index.html' in file_path
    not_exists = not os.path.isfile('.'+file_path)

    if is_index and not_exists:
        create_index_html(
            '.' if file_path == '/index.html' else file_path.replace('/index.html', ''))

# Função para tratar a requisição GET


def handle_get_request(client_socket, request):

    file_path = request.split()[1]

    # request padrão com / deve ser tratado como index da home page
    if file_path == '/':
        file_path = '/index.html'

    # possui a strin do index e não existe como file? Cria a index
    check_index(file_path)

    file_path = '.' + file_path

    # é o endereço de um arquivo?
    if os.path.isfile(file_path):
        directory = os.path.dirname(file_path)

        # checa se o path é restrito
        if not check_IsRestrict(directory):
            send_file(client_socket, file_path)

        else:
            response = generate_response(client_socket, 403)
    # É o endereço de um diretório (Pasta)?
    elif os.path.isdir(file_path):
        # checa se o path é restrito
        if not check_IsRestrict(file_path):
            file_path = file_path + '/index.html'
            check_index(file_path)
            send_file(client_socket, file_path)

        else:
            response = generate_response(client_socket, 403)

    else:
        response = generate_response(client_socket, 404)

# Função principal do servidor


def run_server():
    # Criação do socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f'Server is running on http://{HOST}:{PORT}')

    while True:
        # Aceita conexão do cliente
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address}')

        client_socket.settimeout(100)  # timeout para o client

        while True:
            try:
                request = client_socket.recv(BUFFER_SIZE).decode()

                if not request:
                    # Se não houver dados, o cliente fechou a conexão
                    print('Cliente fechou a conexão')
                    break

                # verifica se é a versão correta do protocolo
                if 'HTTP/1.1' in request:
                    # Verifica se é uma requisição GET
                    if 'GET' in request:
                        handle_get_request(client_socket, request)
                    else:
                        response = generate_response(client_socket, 400)

                else:
                    response = generate_response(client_socket, 505)
            except socket.timeout:
                # Se ocorrer timeout, fecha a conexão do cliente
                print('Timeout do cliente')
                break
        # Fecha a conexão com o cliente
        client_socket.close()
        print(f'Connection from {client_address} was closed')


# Inicia o servidor
if __name__ == '__main__':
    run_server()
