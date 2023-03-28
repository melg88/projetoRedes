# Projeto Redes 

## Projeto 1: Segurança numa Arquitetura P2P:
  a. Cada Equipe (Preencher Tabela) receberá um algoritmo criptográfico
simétrico (AES, DES e RC4) e assimétrico (ECC, RSA, ECDH);
  b. Esses algoritmos devem ser utilizados para garantir os pilares de
segurança em redes numa aplicação do tipo P2P entre três usuários
distintos que estão se comunicando entre si;

  i. Cada usuário deve enviar 2, 4 e 6 pacotes para os outros dois
usuários.
  ii. As mensagens que devem ser enviadas são:
  1. Obra na BR-101;
  2. Obra na PE-015;
  3. Acidente Avenida Norte;
  4. Acidente Avenida Cruz Cabugá;
  5. Trânsito Intenso na Avenida Boa viagem;
  6. Trânsito Intenso na Governador Agamenon Magalhães;

  c. Os pilares que devem ser implementados são:
  i. Confidencialidade;
  ii. Autenticidade;
  iii. Integridade.
  d. Deverá ser realizada uma análise de desempenho dos algoritmos para
cada cenário de envio de pacotes (2, 4 e 6), tais como:
  i. Tamanho do pacote;
  ii. Tempo de transmissão;
  iii. Tempo de criptografia e descriptografia;
  iv. Tempo total Gasto.
  
## Projeto 2: Servidor Web (implemente o protocolo padronizado HTTP/1.1)
- TCP
  a. Deverá ser desenvolvido um servidor WEB;
  i. Deverá implementar o protocolo HTTP/1.1, apenas o método
  GET;

  b. O servidor terá que ser capaz de retornar diversos tipos de arquivos (por
  ex: html, htm, css, js, png, jpg, svg...);
  i. Ou seja, deverá conseguir manipular tanto arquivos de texto,
quanto arquivos binários;

  c. O servidor deverá ser capaz de transmitir arquivos de tamanho muito
grande;
  d. Os requisitos mínimos (devem ser implementados obrigatoriamente) são
o desenvolvimento das respostas com os códigos de resposta a seguir:
  i. 200 OK:
  1. Requisição bem-sucedida, objeto requisitado será enviado
  ii. 400 Bad Request:
  1. Mensagem de requisição não entendida pelo servidor,
nesse caso o cliente escreveu a mensagem de requisição
com algum erro de sintaxe;

  iii. 403 Forbidden:

  1. O cliente não tem direitos de acesso ao conteúdo, portanto
o servidor está rejeitando dar a resposta.

  iv. 404 Not Found

  1. Documento requisitado não localizado no servidor;
v. 505 Version Not Supported
  1. A versão do HTTP utilizada não é suportada neste
servidor.

  e. Com exceção do código 200, o servidor deverá enviar obrigatoriamente
um arquivo html personalizado informando o respectivo erro;
  f. Se a pasta requisitada não contiver um arquivo index.html ou index.htm,
o servidor deverá criar uma página html para navegar pelas pastas,
semelhante ao que apache faz (que navega nas pastas de forma
semelhante ao windows explorer, nautilus e afins...);
  g. O uso de sockets TCP é obrigatório:
  i. Não é permitido o uso de frameworks ou bibliotecas que
implementem o HTTP e substituam o uso de sockets;
  ii. Reforçando, não é permitido o uso de APIs que dispensem a
implementação de um servidor HTTP. (A ideia é realmente
implementar um servidor seguindo um protocolo bem definido
pela comunidade de redes).
  
  
