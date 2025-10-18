# Social Fit 🏋️‍♂️

`Social Fit` é um projeto full-stack de uma rede social voltada para o fitness. Permite que usuários se cadastrem, façam login, postem suas atividades físicas e interajam com os posts de outros usuários.

Este projeto foi criado como um exercício acadêmico, demonstrando a integração entre um backend Python (Flask) e um frontend em HTML/CSS/JS puro que consome a API.

## Funcionalidades

* **Autenticação de Usuários:** Cadastro e Login com validação de formulário e senhas armazenadas com hash.
* **Feed Dinâmico:** Página principal protegida que exibe os posts do usuário e das pessoas que ele segue.
* **Criação de Posts:** Formulário para registrar atividades (descrição, tipo de exercício, duração, calorias).
* **Interação Social:** Sistema de Curtir/Descurtir posts em tempo real.
* **API RESTful:** Backend robusto que gerencia usuários, posts, curtidas e seguidores.

## Tecnologias Utilizadas

### Backend

* **Python 3**
* **Flask:** Micro-framework web para criação da API.
* **Flask-SQLAlchemy:** ORM para interação com o banco de dados.
* **Flask-CORS:** Para permitir a comunicação entre o frontend e o backend.
* **SQLite:** Banco de dados relacional leve.

### Frontend

* **HTML5:** Estrutura das páginas.
* **CSS3:** Estilização (tema dark/vermelho).
* **JavaScript (Vanilla JS):** Manipulação do DOM, validação de formulários e consumo da API.
* **`fetch` API:** Para realizar requisições HTTP ao backend.
* **`localStorage`:** Para armazenar a sessão do usuário no navegador.

## Como Rodar o Projeto

Para rodar a aplicação completa, você precisará de **dois terminais** abertos simultaneamente: um para o backend (API) e outro para o frontend (o site).

### Pré-requisitos

* Ter o [Python 3](https://www.python.org/downloads/) instalado.
* Ter o `pip` (gerenciador de pacotes do Python) atualizado.

### 1. Preparando o Ambiente (Setup)

Antes de rodar pela primeira vez, você precisa instalar as dependências do backend.

1.  Abra um terminal na pasta raiz do projeto (`C:\Faculdade\SocialFit`).
2.  (Opcional, mas recomendado) Crie um ambiente virtual:
    ```bash
    python -m venv venv
    ```
3.  Ative o ambiente virtual:
    * **Windows:** `.\venv\Scripts\activate`
    * **MacOS/Linux:** `source venv/bin/activate`
4.  Instale as bibliotecas Python necessárias:
    ```bash
    pip install Flask Flask-SQLAlchemy Flask-CORS
    ```

### 2. Rodando o Backend (Terminal 1)

1.  No seu primeiro terminal (já na pasta `C:\Faculdade\SocialFit` e com o ambiente virtual ativado).
2.  Execute o servidor Flask:
    ```bash
    python app.py
    ```
3.  Você verá uma saída indicando que o servidor está rodando na porta 5000.
    ```
    * Servidor rodando em: http://localhost:5000
    ```
4.  **Mantenha este terminal aberto.** Ele é a sua API.

### 3. Rodando o Frontend (Terminal 2)

1.  Abra um **novo terminal**.
2.  Navegue para **dentro** da pasta `front`:
    ```bash
    cd C:\Faculdade\SocialFit\front
    ```
3.  Inicie um servidor web simples do Python na porta `8080`:
    ```bash
    python -m http.server 8080
    ```
4.  Você verá uma saída indicando que o servidor está servindo os arquivos.
    ```
    Serving HTTP on 0.0.0.0 port 8080 ([http://0.0.0.0:8080/](http://0.0.0.0:8080/)) ...
    ```
5.  **Mantenha este segundo terminal aberto.** Ele é o seu "servidor de arquivos" do site.

### 4. Acessando a Aplicação

Agora que os dois servidores estão rodando:

1.  Abra seu navegador (Chrome, Firefox, etc.).
2.  Acesse o endereço do **frontend**: **`http://localhost:8080/login.html`**

Você verá a tela de login. Você pode usar os dados de exemplo do `app.py` (`joao@email.com` / `123`) ou criar uma nova conta.

## Principais Endpoints da API (Backend)

* `POST /api/usuarios`: Cria um novo usuário.
* `POST /api/usuarios/login`: Autentica um usuário.
* `GET /api/feed/<user_id>`: Retorna o feed de posts para um usuário.
* `POST /api/posts`: Cria um novo post.
* `GET /api/posts/usuario/<user_id>`: Lista todos os posts de um usuário específico.
* `POST /api/curtir`: Adiciona uma curtida a um post.
* `DELETE /api/curtir/<user_id>/<post_id>`: Remove uma curtida.
* `POST /api/seguir`: Faz um usuário seguir outro.
* `DELETE /api/seguir/<seguidor_id>/<seguido_id>`: Faz um usuário deixar de seguir outro.
