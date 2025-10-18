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

## Estrutura do Projeto