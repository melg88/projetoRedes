🐾🌐 Testando o Projeto 2 - Redes e Computadores 🖥️🐈 

💻 IDE utilizada:
Visual Studio Code (VSCode) para o desenvolvimento e teste deste projeto.

📂 Pastas:
O projeto está dividido em duas pastas: Client e Server.

Tudo sobre a pasta Server:
Na pasta Server/Docs ou Server/Photos 📁 é onde você deve inserir as fotos ou documentos/arquivos pesados conforme desejar.
Na pasta Server/error 📁 é onde ficarão os arquivos HTML com os status http (400, 403, 404, 505).
As pastas Server/secret_doc 📁 e Server/secret_error 📁 são pastas secretas que, ao tentar serem acessadas, retornarão o status HTTP 403.
Dentro da pasta Server será criado o arquivo index.html que permite a navegação no servidor, similar ao Apache. 🐱‍👤

Tudo sobre a pasta Client:
Após executar o Server/Server.py é necessário executar o Client/Client.py.
Na variável request já existem exemplos de requisições para alguns arquivos que já existem no servidor. O formato da requisição deve seguir o seguinte padrão:

'[qualquerNomeQueDesejar': '/[PastaQueOArquivoEstaLocalizado]/[arquivoRequisitado]',


Lembrando que para obter sucesso, o status HTTP 200 OK deve ser retornado e o arquivo deve estar salvo em uma das pastas do Server e ser chamado corretamente na variável Request.

🐱 Conclusão
Com essas dicas você poderá testar o projeto corretamente.
