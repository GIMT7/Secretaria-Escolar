# Sistema de Secretaria Escolar

Este projeto é uma aplicação web feita com Django, simulando uma secretaria escolar digital. O sistema permite gerenciar cadastros, edições e informações de alunos, professores, notas e contratos, promovendo organização e segurança dos dados escolares, com foco em usabilidade e boas práticas.

---

## 🚀 Primeiros Passos

Siga as orientações abaixo para rodar o sistema localmente para desenvolvimento e testes.

> 📅 **Prazo de entrega:** 18/06  
> 🧾 **Como entregar:** Envie o link do repositório no GitHub

---

## 📋 Requisitos Necessários

Antes de começar, instale:

- Python 3.10 ou superior
- Git
- Virtualenv (opcional, mas recomendado)
- SQLite (banco de dados padrão)

Instale as dependências com:

```bash
pip install -r requirements.txt
```

---

## 🔧 Como Instalar

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/seuprojeto.git
cd seuprojeto
```

2. (Opcional) Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute as migrações para preparar o banco de dados:

```bash
python manage.py migrate
```

5. Crie um superusuário para acessar o admin:

```bash
python manage.py createsuperuser
```

6. Inicie o servidor:

```bash
python manage.py runserver
```

Acesse o sistema em `http://127.0.0.1:8000`.

---

## ✅ Recursos Disponíveis

- Login e controle de acesso com `@login_required`
- Cadastro, edição e exclusão de:
  - Alunos
  - Professores
  - Notas
  - Contratos
  - Faltas
  - Notas
  - Histórico Acadêmico
  - Calendário Escolar
  - Calendário de Aulas
  - Matérias
- Interface web com mensagens de feedback ao usuário
- Integração com banco de dados via Django ORM
- Validação de dados nos formulários
- Layout responsivo básico
- Proteção CSRF

---

## ⚙️ Testes Realizados

### 🔩 Testes manuais

- Login e logout
- Cadastro, visualização e alteração de alunos e professores
- Lançamento de notas
- Teste de permissões: páginas protegidas não acessíveis sem login

### ⌨️ Comentários no código

- Funções e métodos importantes comentados
- Separação clara entre models, views e templates

---

## 🖥 Interface e Experiência

- Interface intuitiva com templates Django
- Formulários bem rotulados
- Navegação simples

---

## 📦 Deploy

Para rodar em produção:

- Ajuste `DEBUG = False` em `settings.py`
- Configure `ALLOWED_HOSTS` com o domínio do servidor
- Use Gunicorn + Nginx para servir
- Considere PostgreSQL para produção

---

## 🛠️ Tecnologias

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [SQLite](https://www.sqlite.org/index.html)
- HTML5 e CSS3

---

## 📄 Sobre a Documentação

Este arquivo traz todas as orientações para instalação, uso e testes. O código está comentado para explicar pontos importantes da lógica e autenticação.

---

## 📈 Critérios de Avaliação

| Critério                         | Peso |
|----------------------------------|------|
| Organização do Código            | 20%  |
| Funcionalidades                  | 30%  |
| Interface do Usuário             | 15%  |
| Documentação e Comentários       | 10%  |
| Testes                           | 10%  |
| Segurança e Performance          | 10%  |
| Inovações e Extras               | 5%   |

---

## ✒️ Autor

- **Gabriel Isac Messias Tomaz** – *Desenvolvimento e documentação* – [https://github.com/GIMT7](https://github.com/GIMT7)

---

⌨️ Por Gabriel Isac 💡