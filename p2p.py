import socket
import threading
import time
from Crypto.Cipher import ARC2 as RC2
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA3_384

connections = {}
chaves ={}

#aceitar conexão emtre os nós e adicona as conexões feitas no dicionario connections
def aceppt_connection(user_socket,porta1,chave):
    if porta1 not in connections:
        connections[porta1]= {}     
    while True:
        sock, addr = user_socket.accept()
        porta_sock = int(sock.recv(1024).decode('utf-8'))
        connections[porta1][porta_sock] = sock
        t = threading.Thread(target=receive_message,args=(sock,addr,porta1,porta_sock,chave))
        t.start()
        
def encrypt_rc2(msg,key1):
    key = key1.encode('utf-8')
    teste = msg.encode('utf-8')
    #adiciona preenchimento
    padded_message = pad(teste, RC2.block_size)
    # Criptografar a mensagem usando RC2
    cipher = RC2.new(key, RC2.MODE_ECB)
    encrypted_message = cipher.encrypt(padded_message)
    return encrypted_message

def descrypt_rc2(encrypted_message,key1):
    key = key1.encode('utf-8')
    # Descriptografar a mensagem usando RC2
    decipher = RC2.new(key, RC2.MODE_ECB)
    decrypted_message = decipher.decrypt(encrypted_message)
    # Remover preenchimento da mensagem descriptografada
    unpadded_message = unpad(decrypted_message, RC2.block_size).decode()
    # Imprimir mensagem descriptografada
    return unpadded_message

def send_messages(porta1,porta2,msg,chave):
    cripto = encrypt_rc2(msg,chave)
    # signature = sign(cripto, porta1, dic_chaves[porta1]['private_key'])
    time.sleep(0.000001)
    connections[porta1][porta2].send(cripto)
    
def receive_message(user_socket,addr,porta1,porta2,chave):
    while True:
        try:
            msg = user_socket.recv(1024)
            descripto = descrypt_rc2(msg,chave)
            print(f"{porta2} -> {porta1}",descripto)
        except socket.error:
            print("Conexão encerrada")
            break

def start_connection(porta1,porta2,chave):
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock1.connect(("localhost",porta2))
    print(f"eu {porta1},me conectei com {porta2}")
    sock1.send(str(porta1).encode('utf-8'))
    if porta1 not in connections:
        connections[porta1]= {}
    connections[porta1][porta2] = sock1
    t = threading.Thread(target=receive_message,args=(sock1,("localhost",porta2),porta1,porta2,chave))
    t.start()

    return sock1   
    
    
#abaixo a tentativa de implementar o ECCp-251 e o Hash SH3_384
    #tentativa de implementação
def sign(msg_encry,porta,ecc_private_key):
    
    hash = SHA3_384.new(msg_encry)
    signer = DSS.new(ecc_private_key, 'fips-186-3')
    signature = signer.sign(hash)
    return signature

def verificacao_sign(signature,msg,porta):
    h = SHA3_384.new(msg)
    #tentativa de implementação, dicionário era um teste
    verifier = DSS.new(chaves[porta]['public_key'],'fips-186-3')
    try:
        verifier.verify(h, signature)
        print("A mensagem é autentica")
    except ValueError:
        print("A mensagem não é autentica")
        
#tentativa de implemetação
def compute_hash(message):
        if isinstance(message, str):
            message = message.encode('utf-8')
        h = SHA3_384.new()
        h.update(message)
        return h.digest()
#tentativa de implementação
def verify_hash(received_hash, encrypted_message):
        message = encrypted_message.decode('utf-8')
        computed_hash =compute_hash(message)
        if received_hash != computed_hash:
            raise ValueError("Hashes do not match. Message integrity compromised.")
        else:
            print("integridade ok")   



#para adicionar mais portas é só adicionar um número entre 1 e 50.0000
portas = [11191,23235,21276]
messages =["Obra na BR-101",
           "Obra na PE-015",
           "Acidente Avenida Norte",
           "Acidente Avenida Cruz Cabugá",
           "Trânsito Intenso na Avenida Boa viagem",
           "Trânsito Intenso na Governador Agamenon Magalhães"]

#chave simétrica que irá ser usada entre os nós
chave = str(input("digite uma chave em string: "))

#criar sockets e começar conexões
for porta in portas:
    user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user_socket.bind(('localhost',porta))
    user_socket.listen(3)
    t = threading.Thread(target=aceppt_connection, args=(user_socket,porta,chave))
    t.start()
    print(f"{porta},aguardando conexão...")

# se conectar
for i in range(len(portas)-1):
    porta1 = portas[i]
    for j in range(i+1, len(portas)):
        porta2 = portas[j]
        start_connection(porta1,porta2,chave)

#enviar messagens
for i in range(len(portas)):
        porta1 = portas[i]
        for j in range(len(portas)):
            if i == j:
                continue
            porta2 = portas[j]
            for message in messages[0:2]:
                send_messages(porta1,porta2,message,chave)
            
for i in range(len(portas)):
        porta1 = portas[i]
        for j in range(len(portas)):
            if i == j:
                continue
            porta2 = portas[j]
            for message in messages[0:4]:
                send_messages(porta1,porta2,message,chave)

for i in range(len(portas)):
        porta1 = portas[i]
        for j in range(len(portas)):
            if i == j:
                continue
            porta2 = portas[j]
            for message in messages:
                send_messages(porta1,porta2,message,chave)