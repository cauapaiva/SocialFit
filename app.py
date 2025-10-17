from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_fit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
CORS(app)

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Modelos
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    foto = db.Column(db.String(200), default='default_avatar.png')
    bio = db.Column(db.String(300), default='')
    nivel_fitness = db.Column(db.String(50), default='INICIANTE')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', backref='autor', lazy=True, cascade='all, delete-orphan')
    seguidores = db.relationship('Seguidor', foreign_keys='Seguidor.seguido_id', backref='seguido', lazy=True)
    seguindo = db.relationship('Seguidor', foreign_keys='Seguidor.seguidor_id', backref='seguidor', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(500), nullable=False)
    tipo_exercicio = db.Column(db.String(100))
    duracao = db.Column(db.Integer)
    calorias = db.Column(db.Integer)
    imagem = db.Column(db.String(200))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    curtidas = db.relationship('Curtida', backref='post', lazy=True, cascade='all, delete-orphan')
    comentarios = db.relationship('Comentario', backref='post', lazy=True, cascade='all, delete-orphan')

class Seguidor(db.Model):
    __tablename__ = 'seguidores'
    
    id = db.Column(db.Integer, primary_key=True)
    seguidor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seguido_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('seguidor_id', 'seguido_id', name='unique_seguimento'),)

class Curtida(db.Model):
    __tablename__ = 'curtidas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('usuario_id', 'post_id', name='unique_curtida'),)

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(300), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

# Criar banco de dados
with app.app_context():
    db.drop_all()  # Limpa o banco antigo
    db.create_all()  # Cria novas tabelas
    
    # Dados de exemplo
    if not User.query.first():
        print("📝 Adicionando dados de exemplo...")
        
        usuario1 = User(
            nome="João Silva", 
            email="joao@email.com", 
            bio="Amo correr e malhar! 🏃‍♂️💪",
            nivel_fitness="INTERMEDIARIO"
        )
        usuario1.set_senha("123")
        
        usuario2 = User(
            nome="Maria Santos", 
            email="maria@email.com", 
            bio="Foco na musculação e alimentação saudável! 🏋️‍♀️🥗",
            nivel_fitness="AVANCADO"
        )
        usuario2.set_senha("123")

        usuario3 = User(
            nome="Carlos Oliveira",
            email="carlos@email.com",
            bio="Yoga e meditação para uma vida equilibrada 🧘‍♂️",
            nivel_fitness="INICIANTE"
        )
        usuario3.set_senha("123")
        
        db.session.add_all([usuario1, usuario2, usuario3])
        db.session.commit()
        
        # Posts de exemplo
        posts = [
            Post(
                conteudo="Hoje completei 5km de corrida no parque! 🏃‍♂️ Foi incrível sentir o vento no rosto.",
                tipo_exercicio="CORRIDA",
                duracao=30,
                calorias=300,
                autor_id=1
            ),
            Post(
                conteudo="Treino de peito incrível hoje! 💪 3 séries de supino e finalizei com crucifixo.",
                tipo_exercicio="MUSCULACAO",
                duracao=60,
                calorias=400,
                autor_id=2
            ),
            Post(
                conteudo="Primeira aula de yoga hoje! 🧘‍♂️ Ainda tenho muita flexibilidade para conquistar.",
                tipo_exercicio="YOGA",
                duracao=45,
                calorias=150,
                autor_id=3
            ),
            Post(
                conteudo="Meta atingida: 10km em 55 minutos! 🎉 A evolução é constante!",
                tipo_exercicio="CORRIDA",
                duracao=55,
                calorias=600,
                autor_id=1
            )
        ]
        
        db.session.add_all(posts)
        db.session.commit()
        
        # Seguidores de exemplo
        seguidores = [
            Seguidor(seguidor_id=1, seguido_id=2),
            Seguidor(seguidor_id=1, seguido_id=3),
            Seguidor(seguidor_id=2, seguido_id=1),
            Seguidor(seguidor_id=3, seguido_id=1),
        ]
        
        db.session.add_all(seguidores)
        db.session.commit()
        
        print("✅ Dados de exemplo criados!")
        print(f"👤 Usuários: {User.query.count()}")
        print(f"📝 Posts: {Post.query.count()}")
        print(f"🔗 Seguidores: {Seguidor.query.count()}")

# Rota raiz para verificar API
@app.route('/')
def index():
    return jsonify({
        "mensagem": "🚀 Social Fit API está rodando!",
        "status": "online",
        "endpoints": {
            "usuarios": "/api/usuarios",
            "posts": "/api/posts", 
            "feed": "/api/feed/<user_id>",
            "estatisticas": "/api/estatisticas/<user_id>"
        }
    })

# API Routes - Usuários
@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = User.query.all()
        resultado = []
        for user in usuarios:
            resultado.append({
                "id": user.id,
                "nome": user.nome,
                "email": user.email,
                "foto": user.foto,
                "bio": user.bio,
                "nivel_fitness": user.nivel_fitness,
                "data_criacao": user.data_criacao.isoformat(),
                "qtd_seguidores": Seguidor.query.filter_by(seguido_id=user.id).count(),
                "qtd_seguindo": Seguidor.query.filter_by(seguidor_id=user.id).count()
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/usuarios/<int:user_id>', methods=['GET'])
def buscar_usuario(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        return jsonify({
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "foto": user.foto,
            "bio": user.bio,
            "nivel_fitness": user.nivel_fitness,
            "data_criacao": user.data_criacao.isoformat(),
            "qtd_seguidores": Seguidor.query.filter_by(seguido_id=user.id).count(),
            "qtd_seguindo": Seguidor.query.filter_by(seguidor_id=user.id).count()
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/usuarios', methods=['POST'])
def criar_usuario():
    try:
        data = request.json
        
        if not data.get('nome') or not data.get('email') or not data.get('senha'):
            return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400
            
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"erro": "Email já cadastrado"}), 400
            
        novo_user = User(
            nome=data['nome'],
            email=data['email'],
            bio=data.get('bio', ''),
            nivel_fitness=data.get('nivel_fitness', 'INICIANTE'),
            foto=data.get('foto', 'default_avatar.png')
        )
        novo_user.set_senha(data['senha'])
        
        db.session.add(novo_user)
        db.session.commit()
        
        return jsonify({
            "mensagem": "Usuário criado com sucesso!", 
            "id": novo_user.id,
            "usuario": {
                "id": novo_user.id,
                "nome": novo_user.nome,
                "email": novo_user.email,
                "bio": novo_user.bio,
                "nivel_fitness": novo_user.nivel_fitness,
                "foto": novo_user.foto
            }
        }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route('/api/usuarios/login', methods=['POST'])
def login():
    try:
        data = request.json
        
        if not data.get('email') or not data.get('senha'):
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400
            
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_senha(data['senha']):
            return jsonify({
                "mensagem": "Login realizado com sucesso!",
                "usuario": {
                    "id": user.id,
                    "nome": user.nome,
                    "email": user.email,
                    "foto": user.foto,
                    "nivel_fitness": user.nivel_fitness,
                    "bio": user.bio
                }
            })
        return jsonify({"erro": "Email ou senha incorretos"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

# API Routes - Posts
@app.route('/api/posts', methods=['GET'])
def listar_posts():
    try:
        posts = Post.query.order_by(Post.data_criacao.desc()).all()
        resultado = []
        for post in posts:
            autor = User.query.get(post.autor_id)
            resultado.append({
                "id": post.id,
                "conteudo": post.conteudo,
                "tipo_exercicio": post.tipo_exercicio,
                "duracao": post.duracao,
                "calorias": post.calorias,
                "imagem": post.imagem,
                "data_criacao": post.data_criacao.isoformat(),
                "autor": {
                    "id": autor.id,
                    "nome": autor.nome,
                    "foto": autor.foto,
                    "nivel_fitness": autor.nivel_fitness
                },
                "qtd_curtidas": Curtida.query.filter_by(post_id=post.id).count(),
                "qtd_comentarios": Comentario.query.filter_by(post_id=post.id).count()
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/posts/usuario/<int:user_id>', methods=['GET'])
def posts_usuario(user_id):
    try:
        posts = Post.query.filter_by(autor_id=user_id).order_by(Post.data_criacao.desc()).all()
        resultado = []
        for post in posts:
            resultado.append({
                "id": post.id,
                "conteudo": post.conteudo,
                "tipo_exercicio": post.tipo_exercicio,
                "duracao": post.duracao,
                "calorias": post.calorias,
                "imagem": post.imagem,
                "data_criacao": post.data_criacao.isoformat(),
                "qtd_curtidas": Curtida.query.filter_by(post_id=post.id).count(),
                "qtd_comentarios": Comentario.query.filter_by(post_id=post.id).count()
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/posts', methods=['POST'])
def criar_post():
    try:
        data = request.json
        
        if not data.get('conteudo') or not data.get('autor_id'):
            return jsonify({"erro": "Conteúdo e autor_id são obrigatórios"}), 400
            
        autor = User.query.get(data['autor_id'])
        if not autor:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        post = Post(
            conteudo=data['conteudo'],
            tipo_exercicio=data.get('tipo_exercicio'),
            duracao=data.get('duracao'),
            calorias=data.get('calorias'),
            imagem=data.get('imagem'),
            autor_id=data['autor_id']
        )
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            "mensagem": "Post criado com sucesso!", 
            "id": post.id,
            "post": {
                "id": post.id,
                "conteudo": post.conteudo,
                "tipo_exercicio": post.tipo_exercicio,
                "data_criacao": post.data_criacao.isoformat()
            }
        }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

# API Routes - Seguidores
@app.route('/api/seguir', methods=['POST'])
def seguir_usuario():
    try:
        data = request.json
        
        if not data.get('seguidor_id') or not data.get('seguido_id'):
            return jsonify({"erro": "seguidor_id e seguido_id são obrigatórios"}), 400
            
        seguidor_id = data['seguidor_id']
        seguido_id = data['seguido_id']
        
        seguidor = User.query.get(seguidor_id)
        seguido = User.query.get(seguido_id)
        
        if not seguidor or not seguido:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        if Seguidor.query.filter_by(seguidor_id=seguidor_id, seguido_id=seguido_id).first():
            return jsonify({"erro": "Você já segue este usuário"}), 400
        
        if seguidor_id == seguido_id:
            return jsonify({"erro": "Não é possível seguir a si mesmo"}), 400
            
        novo_seguimento = Seguidor(seguidor_id=seguidor_id, seguido_id=seguido_id)
        db.session.add(novo_seguimento)
        db.session.commit()
        
        return jsonify({
            "mensagem": f"Agora você está seguindo {seguido.nome}!",
            "seguindo": True
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route('/api/seguir/<int:seguidor_id>/<int:seguido_id>', methods=['DELETE'])
def deixar_seguir(seguidor_id, seguido_id):
    try:
        seguimento = Seguidor.query.filter_by(seguidor_id=seguidor_id, seguido_id=seguido_id).first()
        if seguimento:
            db.session.delete(seguimento)
            db.session.commit()
            return jsonify({"mensagem": "Deixou de seguir o usuário"})
        return jsonify({"erro": "Relação de seguimento não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

# API Routes - Curtidas
@app.route('/api/curtir', methods=['POST'])
def curtir_post():
    try:
        data = request.json
        
        if not data.get('usuario_id') or not data.get('post_id'):
            return jsonify({"erro": "usuario_id e post_id são obrigatórios"}), 400
            
        usuario_id = data['usuario_id']
        post_id = data['post_id']
        
        usuario = User.query.get(usuario_id)
        post = Post.query.get(post_id)
        
        if not usuario or not post:
            return jsonify({"erro": "Usuário ou post não encontrado"}), 404
        
        if Curtida.query.filter_by(usuario_id=usuario_id, post_id=post_id).first():
            return jsonify({"erro": "Você já curtiu este post"}), 400
        
        curtida = Curtida(usuario_id=usuario_id, post_id=post_id)
        db.session.add(curtida)
        db.session.commit()
        
        return jsonify({
            "mensagem": "Post curtido!",
            "curtido": True,
            "total_curtidas": Curtida.query.filter_by(post_id=post_id).count()
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route('/api/curtir/<int:usuario_id>/<int:post_id>', methods=['DELETE'])
def descurtir_post(usuario_id, post_id):
    try:
        curtida = Curtida.query.filter_by(usuario_id=usuario_id, post_id=post_id).first()
        if curtida:
            db.session.delete(curtida)
            db.session.commit()
            return jsonify({
                "mensagem": "Curtida removida",
                "curtido": False,
                "total_curtidas": Curtida.query.filter_by(post_id=post_id).count()
            })
        return jsonify({"erro": "Curtida não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

# API Routes - Comentários
@app.route('/api/comentarios', methods=['POST'])
def criar_comentario():
    try:
        data = request.json
        
        if not data.get('conteudo') or not data.get('usuario_id') or not data.get('post_id'):
            return jsonify({"erro": "Conteúdo, usuario_id e post_id são obrigatórios"}), 400
            
        usuario = User.query.get(data['usuario_id'])
        post = Post.query.get(data['post_id'])
        
        if not usuario or not post:
            return jsonify({"erro": "Usuário ou post não encontrado"}), 404
            
        comentario = Comentario(
            conteudo=data['conteudo'],
            usuario_id=data['usuario_id'],
            post_id=data['post_id']
        )
        db.session.add(comentario)
        db.session.commit()
        
        return jsonify({
            "mensagem": "Comentário adicionado!", 
            "id": comentario.id,
            "comentario": {
                "id": comentario.id,
                "conteudo": comentario.conteudo,
                "data_criacao": comentario.data_criacao.isoformat(),
                "usuario": {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "foto": usuario.foto
                }
            }
        }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route('/api/comentarios/post/<int:post_id>', methods=['GET'])
def listar_comentarios(post_id):
    try:
        comentarios = Comentario.query.filter_by(post_id=post_id).order_by(Comentario.data_criacao.asc()).all()
        resultado = []
        for comentario in comentarios:
            usuario = User.query.get(comentario.usuario_id)
            resultado.append({
                "id": comentario.id,
                "conteudo": comentario.conteudo,
                "data_criacao": comentario.data_criacao.isoformat(),
                "usuario": {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "foto": usuario.foto
                }
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# API Routes - Feed e Estatísticas
@app.route('/api/feed/<int:user_id>', methods=['GET'])
def feed_usuario(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        seguindo = Seguidor.query.filter_by(seguidor_id=user_id).all()
        ids_seguindo = [s.seguido_id for s in seguindo]
        ids_seguindo.append(user_id)
        
        posts = Post.query.filter(Post.autor_id.in_(ids_seguindo)).order_by(Post.data_criacao.desc()).all()
        
        resultado = []
        for post in posts:
            autor = User.query.get(post.autor_id)
            resultado.append({
                "id": post.id,
                "conteudo": post.conteudo,
                "tipo_exercicio": post.tipo_exercicio,
                "duracao": post.duracao,
                "calorias": post.calorias,
                "imagem": post.imagem,
                "data_criacao": post.data_criacao.isoformat(),
                "autor": {
                    "id": autor.id,
                    "nome": autor.nome,
                    "foto": autor.foto,
                    "nivel_fitness": autor.nivel_fitness
                },
                "qtd_curtidas": Curtida.query.filter_by(post_id=post.id).count(),
                "qtd_comentarios": Comentario.query.filter_by(post_id=post.id).count(),
                "curtido_por_mim": bool(Curtida.query.filter_by(usuario_id=user_id, post_id=post.id).first())
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/estatisticas/<int:user_id>', methods=['GET'])
def estatisticas_usuario(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
            
        total_posts = Post.query.filter_by(autor_id=user_id).count()
        total_seguidores = Seguidor.query.filter_by(seguido_id=user_id).count()
        total_seguindo = Seguidor.query.filter_by(seguidor_id=user_id).count()
        total_curtidas = db.session.query(Curtida).join(Post).filter(Post.autor_id == user_id).count()
        
        # Estatísticas de exercícios
        posts_usuario = Post.query.filter_by(autor_id=user_id).all()
        total_minutos = sum(post.duracao or 0 for post in posts_usuario)
        total_calorias = sum(post.calorias or 0 for post in posts_usuario)
        
        return jsonify({
            "total_posts": total_posts,
            "total_seguidores": total_seguidores,
            "total_seguindo": total_seguindo,
            "total_curtidas": total_curtidas,
            "total_minutos": total_minutos,
            "total_calorias": total_calorias
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/verificar-seguimento/<int:seguidor_id>/<int:seguido_id>', methods=['GET'])
def verificar_seguimento(seguidor_id, seguido_id):
    try:
        seguimento = Seguidor.query.filter_by(seguidor_id=seguidor_id, seguido_id=seguido_id).first()
        return jsonify({"seguindo": bool(seguimento)})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Social Fit Backend...")
    print("📊 Banco de dados: social_fit.db")
    print("🌐 Servidor rodando em: http://localhost:5000")
    print("🔑 Teste o login: POST /api/usuarios/login")
    print("📝 Teste os posts: GET /api/posts")
    print("👥 Teste o feed: GET /api/feed/1")
    app.run(debug=True, host='0.0.0.0', port=5000)