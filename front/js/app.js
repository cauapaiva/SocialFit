// URL base da sua API Flask
const API_URL = 'http://localhost:5000/api';

// 1. Verifica se o usuário está logado
const user = JSON.parse(localStorage.getItem('socialFitUser'));
if (!user) {
    // Se não estiver logado, redireciona para a página de login
    window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', () => {
    // 2. Personaliza a página com dados do usuário
    document.getElementById('user-name').textContent = `Olá, ${user.nome}!`;

    // 3. Carrega o feed
    loadFeed();

    // 4. Configura botão de Logout
    document.getElementById('logout-btn').addEventListener('click', () => {
        localStorage.removeItem('socialFitUser');
        window.location.href = 'login.html';
    });

    // 5. Configura formulário de novo post
    document.getElementById('post-form').addEventListener('submit', handleCreatePost);
    
    // 6. Configura cliques de "Curtir" (usando delegação de eventos)
    document.getElementById('feed-container').addEventListener('click', handleLikeClick);
});

/**
 * Busca o feed do usuário na API e o renderiza na tela
 */
async function loadFeed() {
    const feedContainer = document.getElementById('feed-container');
    feedContainer.innerHTML = 'Carregando feed...'; // Feedback de loading

    try {
        const response = await fetch(`${API_URL}/feed/${user.id}`);
        if (!response.ok) {
            throw new Error('Falha ao carregar o feed');
        }
        
        const posts = await response.json();

        if (posts.length === 0) {
            feedContainer.innerHTML = '<p>Seu feed está vazio. Siga alguém ou crie seu primeiro post!</p>';
            return;
        }

        // Limpa o container e renderiza os posts
        feedContainer.innerHTML = '';
        posts.forEach(post => {
            feedContainer.appendChild(createPostElement(post));
        });

    } catch (error) {
        console.error('Erro ao carregar feed:', error);
        feedContainer.innerHTML = '<p class="error">Não foi possível carregar o feed.</p>';
    }
}

/**
 * Cria o elemento HTML para um único post
 * @param {object} post - O objeto do post vindo da API
 * @returns {HTMLElement} O elemento <div> do post
 */
function createPostElement(post) {
    const postCard = document.createElement('div');
    postCard.className = 'post-card';
    postCard.dataset.postId = post.id; // Armazena o ID do post no elemento

    const postDate = new Date(post.data_criacao).toLocaleString('pt-BR');

    // Adiciona classe 'liked' se o usuário já curtiu
    const likedClass = post.curtido_por_mim ? 'liked' : '';

    postCard.innerHTML = `
        <div class="post-header">
            <img src="https://ui-avatars.com/api/?name=${post.autor.nome}&background=random" alt="Avatar" class="post-avatar">
            <div class="post-author-info">
                <span class="name">${post.autor.nome}</span>
                <span class="date">${postDate}</span>
            </div>
        </div>
        <div class="post-content">
            <p>${post.conteudo}</p>
        </div>
        <div class="post-stats">
            ${post.tipo_exercicio ? `<span>💪 ${post.tipo_exercicio}</span>` : ''}
            ${post.duracao ? `<span>⏱️ ${post.duracao} min</span>` : ''}
            ${post.calorias ? `<span>🔥 ${post.calorias} kcal</span>` : ''}
        </div>
        <div class="post-meta">
            <span id="likes-count-${post.id}">${post.qtd_curtidas} curtidas</span>
        </div>
        <div class="post-actions">
            <button class="action-btn like-btn ${likedClass}" data-post-id="${post.id}">
                ${post.curtido_por_mim ? 'Descurtir' : 'Curtir'}
            </button>
            <button class="action-btn comment-btn">Comentar</button>
        </div>
    `;
    return postCard;
}

/**
 * Lida com o submit do formulário de novo post
 */
async function handleCreatePost(e) {
    e.preventDefault();

    const conteudo = document.getElementById('post-conteudo').value;
    const tipo_exercicio = document.getElementById('post-tipo').value;
    const duracao = document.getElementById('post-duracao').value;
    const calorias = document.getElementById('post-calorias').value;

    const postData = {
        conteudo,
        autor_id: user.id, // Adiciona o ID do usuário logado
        tipo_exercicio: tipo_exercicio || null,
        duracao: duracao ? parseInt(duracao) : null,
        calorias: calorias ? parseInt(calorias) : null,
    };

    try {
        const response = await fetch(`${API_URL}/posts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(postData)
        });

        if (response.status === 201) {
            // Sucesso! Limpa o formulário e recarrega o feed
            document.getElementById('post-form').reset();
            loadFeed(); // Recarrega o feed para mostrar o novo post
        } else {
            const errorData = await response.json();
            alert(`Erro ao criar post: ${errorData.erro}`);
        }
    } catch (error) {
        console.error('Erro de rede:', error);
        alert('Não foi possível conectar ao servidor para postar.');
    }
}

/**
 * Lida com cliques no botão "Curtir/Descurtir"
 */
async function handleLikeClick(e) {
    // Verifica se o clique foi em um botão de curtir
    if (!e.target.classList.contains('like-btn')) {
        return;
    }

    const likeButton = e.target;
    const postId = likeButton.dataset.postId;
    const isLiked = likeButton.classList.contains('liked');

    if (isLiked) {
        // --- Lógica para DESCURTIR ---
        try {
            const response = await fetch(`${API_URL}/curtir/${user.id}/${postId}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            
            if (response.ok) {
                // Atualiza o botão e a contagem
                likeButton.classList.remove('liked');
                likeButton.textContent = 'Curtir';
                document.getElementById(`likes-count-${postId}`).textContent = `${data.total_curtidas} curtidas`;
            } else {
                alert(`Erro ao descurtir: ${data.erro}`);
            }
        } catch (error) {
            console.error('Erro de rede ao descurtir:', error);
        }

    } else {
        // --- Lógica para CURTIR ---
        try {
            const response = await fetch(`${API_URL}/curtir`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ usuario_id: user.id, post_id: parseInt(postId) })
            });
            const data = await response.json();
            
            if (response.ok) {
                // Atualiza o botão e a contagem
                likeButton.classList.add('liked');
                likeButton.textContent = 'Descurtir';
                 document.getElementById(`likes-count-${postId}`).textContent = `${data.total_curtidas} curtidas`;
            } else {
                 alert(`Erro ao curtir: ${data.erro}`);
            }
        } catch (error) {
            console.error('Erro de rede ao curtir:', error);
        }
    }
}