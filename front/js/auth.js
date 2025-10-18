// URL base da sua API Flask
const API_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

/**
 * Lida com o submit do formulário de login
 */
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = ''; // Limpa erros antigos

    try {
        const response = await fetch(`${API_URL}/usuarios/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (response.ok) {
            // Login bem-sucedido
            console.log('Login com sucesso:', data.usuario);
            // Salva dados do usuário no localStorage
            localStorage.setItem('socialFitUser', JSON.stringify(data.usuario));
            // Redireciona para a página principal (feed)
            window.location.href = 'index.html';
        } else {
            // Exibe mensagem de erro
            errorMessage.textContent = data.erro || 'Erro ao fazer login.';
        }
    } catch (error) {
        console.error('Erro de rede:', error);
        errorMessage.textContent = 'Não foi possível conectar ao servidor.';
    }
}

/**
 * Lida com o submit do formulário de cadastro
 */
async function handleRegister(e) {
    e.preventDefault();
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const bio = document.getElementById('bio').value;
    
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');
    errorMessage.textContent = '';
    successMessage.textContent = '';

    try {
        const response = await fetch(`${API_URL}/usuarios`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, email, senha, bio, nivel_fitness: 'INICIANTE' })
        });

        const data = await response.json();

        if (response.status === 201) {
            // Cadastro bem-sucedido
            successMessage.textContent = 'Usuário criado! Redirecionando para login...';
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            // Exibe mensagem de erro
            errorMessage.textContent = data.erro || 'Erro ao cadastrar.';
        }
    } catch (error) {
        console.error('Erro de rede:', error);
        errorMessage.textContent = 'Não foi possível conectar ao servidor.';
    }
}