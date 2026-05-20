# 🦖 Pokédex Analytics — Engenharia de Dados & BI Avançado

> Uma aplicação web analítica de ponta a ponta que transforma dados brutos e semiestruturados de cards colecionáveis em um ecossistema de **Business Intelligence**. O projeto integra modelagem de banco de dados relacional na nuvem, pipelines de tratamento de dados e uma interface de usuário altamente interativa focada em tomada de decisão e análise tática.

🔗 **[Acesse a aplicação ao vivo](https://pokedex-analytics.streamlit.app/)**

---

## 📐 Arquitetura do Projeto

O ecossistema foi desenhado seguindo as melhores práticas de mercado para segregação de camadas:

| Camada | Tecnologia | Responsabilidade |
|---|---|---|
| **Storage** | PostgreSQL (Neon) | Persistência, integridade referencial e isolamento de ambientes |
| **Processing** | Python + Pandas + Regex | Ingestão, limpeza, tratamento de strings e tipagem dinâmica |
| **Analytics** | Streamlit + Plotly Express | Painel interativo para descoberta de insights em tempo real |

---

## ⚡ Funcionalidades Chave

- **📊 Painel de Controle de BI** — Filtros cruzados e simultâneos por nome, elemento dominante e faixas de vitalidade (HP), simulando o comportamento nativo de ferramentas de mercado.

- **📈 Métricas Executivas (KPIs)** — Cards de alto nível que calculam dinamicamente volumetria de dados, médias de poder, elementos dominantes e lideranças estatísticas.

- **⚔️ Data Match-Up (Simulador Avançado)** — Algoritmo de cruzamento de dados que avalia dois alvos simultâneos, calcula deltas de atributos, detecta empates técnicos e injeta uma camada de inteligência de risco baseada em vantagens e fraquezas elementais (regras de negócio cruzadas).

- **🔬 Análise Estatística Visual** — Gráficos de distribuição de poder médio por elemento e dispersão de correlação entre variáveis numéricas (HP vs. Dano).

---

## 🛠️ Engenharia de Dados & Lógica de Negócio

### 1. Modelagem Relacional (SQL)

O banco de dados foi estruturado utilizando **chaves estrangeiras** para otimização de consultas e eliminação de redundâncias entre as tabelas de cards e elementos originais. Os scripts de migração e versionamento de dados estão documentados e isolados na pasta do projeto.

### 2. Regex e Engenharia de Atributos (Feature Engineering)

Os dados brutos de ataques continham caracteres especiais e sufixos textuais (como `"100+"`, `"30x"`). Para viabilizar análises estatísticas e cálculos matemáticos complexos, foi aplicada uma extração via **Expressões Regulares (Regex)** isolando os números no Pandas, gerando em seguida a métrica de **Poder Combinado** (HP + Dano Tratado).

### 3. Tratamento de Strings para Integração de Imagens Externos

Para garantir que a renderização visual de recursos externos funcionasse sem quebras em casos de nomes com caracteres especiais (como `Farfetch'd`, `Mr. Mime` ou `Nidoran`), foi desenvolvida uma **função de higienização de strings** baseada em regras de negócio estritas de marca, mapeando as variantes de gênero masculino/feminino e limpando pontuações das URLs.

---

## 📂 Estrutura do Repositório

```
pokedex-analytics/
│
├── db_scripts/
│   ├── 01_initial_seed.sql       # Estrutura inicial do banco
│   ├── 02_bulk_cards_1.sql       # Carga massiva de dados (parte 1)
│   └── ...                       # Scripts incrementais seguintes
│
├── app.py                        # Código fonte principal (Streamlit)
├── requirements.txt              # Dependências do projeto
├── .gitignore                    # Bloqueia arquivos sensíveis (.env)
└── README.md
```

---

## 🚀 Como Executar o Projeto Localmente

**1. Clone o repositório:**
```bash
git clone https://github.com/BrunaDev9/pokedex-analytics.git
cd pokedex-analytics
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**3. Configure as Variáveis de Ambiente:**

Crie um arquivo `.env` na raiz do projeto e adicione a sua string de conexão:
```env
DB_URI="postgresql://usuario:senha@host:porta/banco?sslmode=require"
```

**4. Execute a aplicação:**
```bash
streamlit run app.py
```

---

## 🔒 Segurança de Dados

Este projeto segue rigorosamente boas práticas de segurança:

- ✅ Nenhuma credencial exposta no histórico do Git
- ✅ Gestão de credenciais em produção via **variáveis de ambiente criptografadas** (Secrets)
- ✅ Arquivo `.gitignore` configurado para bloquear arquivos `.env` locais
