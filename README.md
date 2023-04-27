# Projeto Redes 

## Projeto 1: Segurança numa Arquitetura P2P:
### 🌐contextualização
Este projeto tem como objetivo fazer desenvolvimento de uma arquitetura P2P, que vai fazer a comunicação entre três usuários , utilizando sockets através dos conhecimentos que foram adquiridos durante a disciplina de é da disciplina IF975 - Redes de Computadores do CIN-UFPE.
### 🔐Algoritmos que garantem os pilares da segurança
Na questão que envolve confidenciabilidade foi passado a chave simétrica RC2, sobre o pilar da integridade , foi passado o hahs SH3_384 e para autencidade , a chave assimétrica ECCp-251 que foi requisistada.
### 💻 IDE utilizada:
Visual Studio Code (VSCode) para o desenvolvimento e teste deste projeto.
### 📖Biblioteca utilizada
Lembre de fazer a instalação da biblioteca em sua máquina, basta digitar no terminal da máquina ou no da IDE, o comando __*"pip install pycyptodome"*__ e com isso irá obter a versão que foi utilizada no projeto.

[pycyptodome](https://pypi.org/project/pycryptodome/)

### 😃Dicas de uso
Na implementação do nosso código, criamos uma lista a qual tem o número da porta que vão representar os nós do P2P, em caso de erro, devido ao endereço já está em uso, basta alterar os números, da lista portas e irá funcionar normalmente.
