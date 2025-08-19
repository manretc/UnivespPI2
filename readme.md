# **Rede de Doações de Alimentos**

Este é o repositório do projeto "Rede de Doações de Alimentos", uma aplicação web desenvolvida em Python com o framework Flask. A plataforma visa conectar doadores de alimentos a instituições de caridade, facilitando o processo de doação e combatendo o desperdício.

## **Pré-requisitos**

Antes de começar, certifique-se de que tem o seguinte software instalado na sua máquina:

* **Python 3.8** ou superior  
* **Git**  
* **PostgreSQL** (versão 12 ou superior)

## **Guia de Instalação e Configuração**

Siga estes passos para configurar o ambiente de desenvolvimento local.

### **1\. Clonar o Repositório**

Abra o seu terminal e clone o projeto para a sua máquina:

git clone \<URL\_DO\_REPOSITORIO\>  
cd rede\_doacoes

### **2\. Configurar o Ambiente Virtual (Recomendado)**

É uma boa prática isolar as dependências do projeto num ambiente virtual.

\# Criar o ambiente virtual  
python \-m venv venv

\# Ativar o ambiente virtual (Windows)  
.\\venv\\Scripts\\activate

\# Para macOS/Linux, o comando seria:  
\# source venv/bin/activate

### **3\. Instalar as Dependências**

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias:

pip install \-r requirements.txt

### **4\. Configurar o Banco de Dados PostgreSQL**

1. Certifique-se de que o seu serviço do PostgreSQL está em execução.  
2. Abra uma ferramenta de gestão do PostgreSQL (como o psql ou o pgAdmin).  
3. Crie uma nova base de dados para o projeto:  
   CREATE DATABASE rede\_doacoes;

### **5\. Configurar as Variáveis de Ambiente**

A aplicação utiliza um ficheiro .env para gerir configurações sensíveis.

1. Na raiz do projeto, crie um ficheiro chamado .env.  
2. Copie o conteúdo abaixo para o seu ficheiro .env e preencha os valores corretos:  
   \# Chave secreta para a segurança da aplicação (pode gerar uma nova)  
   SECRET\_KEY='uma-chave-secreta-de-desenvolvimento-pode-ser-qualquer-coisa'

   \# URI de conexão com o banco de dados PostgreSQL  
   \# Substitua \<SUA\_SENHA\> pela senha do seu utilizador 'postgres'  
   DATABASE\_URL='postgresql://postgres:\<SUA\_SENHA\>@localhost:5432/rede\_doacoes'

   \# Chave da API do Google Cloud Platform  
   \# Certifique-se de que as APIs "Geocoding API" e "Maps Static API" estão ativas  
   GOOGLE\_MAPS\_API\_KEY='SUA\_CHAVE\_DA\_API\_DO\_GOOGLE\_AQUI'

### **6\. Executar as Migrações da Base de Dados**

Estes comandos irão criar as tabelas necessárias na sua base de dados rede\_doacoes.

\# Definir a aplicação Flask para o terminal (só precisa de o fazer uma vez por sessão)  
set FLASK\_APP=run.py

\# Inicializar o repositório de migrações (só precisa de o fazer uma vez na vida do projeto)  
flask db init

\# Gerar o script da primeira migração  
flask db migrate \-m "criacao inicial das tabelas"

\# Aplicar a migração à base de dados  
flask db upgrade

**Nota:** Sempre que houver uma alteração nos modelos (app/models.py), será necessário executar os comandos flask db migrate e flask db upgrade novamente.

## **Como Executar a Aplicação**

Com tudo configurado, inicie o servidor de desenvolvimento do Flask:

flask run

A aplicação estará disponível no seu navegador no seguinte endereço: [**http://127.0.0.1:5000**](https://www.google.com/search?q=http://127.0.0.1:5000)

## **Como Executar os Testes**

Para garantir que tudo está a funcionar como esperado, pode executar a suíte de testes automatizados:

pytest  
