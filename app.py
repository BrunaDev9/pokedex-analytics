import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import os
from dotenv import load_dotenv

# Carrega as credenciais com segurança do .env
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Pokédex Analytics",
    page_icon="🦖",
    layout="wide"
)

st.title("🦖 Pokédex Analytics - Engenharia & BI Avançado")
st.markdown("---")

DB_URI = os.getenv("DB_URI")

@st.cache_data
def carregar_dados():
    try:
        conn = psycopg2.connect(DB_URI)
        query = """
            SELECT 
                c.id, c.name, c.hp, c.info, c.attack, c.damage, c.weak, c.ressis,
                t.typeName as tipo
            FROM tbl_cards c
            LEFT JOIN tbl_types t ON c.type_id = t.id;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Tratamento: extrai o número do dano (ex: "100+" ou "30" vira 100 e 30)
        df['damage_num'] = pd.to_numeric(df['damage'].str.extract(r'(\d+)')[0], errors='coerce').fillna(0)
        
        # Criação de métrica própria: Poder Total
        df['poder_total'] = df['hp'] + df['damage_num']
        return df
    except Exception as e:
        st.error(f"Erro ao conectar no banco Neon: {e}")
        return pd.DataFrame()

df_pokemon = carregar_dados()

# Dicionário de cores para os elementos (UX/UI)
CORES_TIPOS = {
    "Fire": "#FF421C", "Water": "#2C9BEF", "Grass": "#2CD268",
    "Electric": "#F4D03F", "Psychic": "#A569BD", "Fighting": "#E67E22",
    "Colorless": "#BDC3C7", "Dragon": "#8E44AD", "Dark": "#34495E"
}

if not df_pokemon.empty:
    #  Barra lateral com filtros avançados (Engenharia de Dados + UX/UI) 
    st.sidebar.header("🔍 Painel de Controle")
    
    busca_nome = st.sidebar.text_input("Buscar pelo Nome:", "").strip()
    
    tipos_disponiveis = sorted(df_pokemon['tipo'].dropna().unique().tolist())
    tipo_selecionado = st.sidebar.multiselect("Filtrar Elemento:", options=tipos_disponiveis, default=tipos_disponiveis)
    
    min_hp, max_hp = int(df_pokemon['hp'].min()), int(df_pokemon['hp'].max())
    filtro_hp = st.sidebar.slider("Filtrar por Faixa de HP:", min_hp, max_hp, (min_hp, max_hp))

    # Aplicando os filtros cruzados (Engenharia de Dados com Pandas)
    df_filtrado = df_pokemon[
        (df_pokemon['tipo'].isin(tipo_selecionado)) &
        (df_pokemon['name'].str.contains(busca_nome, case=False)) &
        (df_pokemon['hp'].between(filtro_hp[0], filtro_hp[1]))
    ]
    
    # Métricas de Resumo (KPIs) 
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Cards Exibidos", f"{len(df_filtrado)} / {len(df_pokemon)}")
    with col_m2:
        media_hp = int(df_filtrado['hp'].mean()) if not df_filtrado.empty else 0
        st.metric("Média de Vitalidade (HP)", f"{media_hp} HP")
    with col_m3:
        max_poder = int(df_filtrado['poder_total'].max()) if not df_filtrado.empty else 0
        st.metric("Maior Poder da Seleção", f"{max_poder} pts")
    with col_m4:
        tipo_comum = df_filtrado['tipo'].mode()[0] if not df_filtrado.empty else "Nenhum"
        st.metric("Elemento Dominante", tipo_comum)
        
    st.markdown("---")
    
    # Criação das abas de navegação (UX/UI) para organizar o conteúdo de forma intuitiva.
    aba_galeria, aba_graficos, aba_combate = st.tabs([
        "✨ Galeria Interativa", 
        "📊 Insights Estatísticos",
        "⚔️ Simulador de Combate (Data Match)"
    ])
    
    # Aba 01 - Galeria Interativa de Cards (Engenharia de Dados + UX/UI).
    with aba_galeria:
        if not df_filtrado.empty:
            cols = st.columns(4) # Grade de 4 cards por linha
            for idx, row in df_filtrado.reset_index().iterrows():
                col_atual = cols[idx % 4]
                with col_atual:
                    with st.container(border=True):
                        # Tratamento robusto para as URLs de imagem
                        nome_base = str(row['name']).lower().strip()
                        if "nidoran" in nome_base:
                            if "♂" in nome_base or "male" in nome_base:
                                nome_limpo = "nidoran-m"
                            elif "♀" in nome_base or "female" in nome_base:
                                nome_limpo = "nidoran-f"
                            else:
                                nome_limpo = "nidoran"
                        else:
                            nome_limpo = nome_base.replace(" ", "-").replace("♂", "-m").replace("♀", "-f").replace(".", "").replace("'", "")
                        
                        url_imagem = f"https://img.pokemondb.net/artwork/large/{nome_limpo}.jpg"
                        
                        # Nome e HP lado a lado.
                        col_n, col_h = st.columns([2, 1])
                        col_n.subheader(f"**{row['name']}**")
                        col_h.markdown(f"❤️ `{row['hp']} HP`")
                        
                        st.image(url_imagem, use_container_width=True)
                        st.caption(f"_{row['info']}_")
                        
                        # Estilização com base na cor do tipo.
                        cor_badge = CORES_TIPOS.get(row['tipo'], "#BDC3C7")
                        st.markdown(f"**Elemento:** <span style='background-color:{cor_badge}; padding:2px 8px; border-radius:5px; color:white; font-weight:bold;'>{row['tipo']}</span>", unsafe_allow_html=True)
                        
                        st.markdown(f"⚔️ **Ataque:** {row['attack']} | 💥 **Dano:** `{row['damage']}`")
                        st.caption(f"❌ Fraqueza: {row['weak']} | 🛡️ Resistência: {row['ressis']}")
        else:
            st.info("Nenhum card atende aos critérios dos filtros aplicados.")
            
    # Aba 02 - Insights Estatísticos Avançados (Engenharia de Dados + Visualização com Plotly).
    with aba_graficos:
        if not df_filtrado.empty:
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                st.markdown("#### 💪 Distribuição de Poder Médio por Elemento")
                df_grupo = df_filtrado.groupby('tipo')['poder_total'].mean().reset_index().sort_values(by='poder_total', ascending=False)
                fig_bar = px.bar(df_grupo, x='tipo', y='poder_total', labels={'tipo':'Tipo', 'poder_total':'Poder Médio'}, template="plotly_dark", color='tipo', color_discrete_map=CORES_TIPOS)
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with col_g2:
                st.markdown("#### 🎯 Correlação: Pontos de HP vs Dano")
                fig_scatter = px.scatter(df_filtrado, x='hp', y='damage_num', hover_name='name', color='tipo', color_discrete_map=CORES_TIPOS, labels={'hp':'Pontos de HP', 'damage_num':'Dano Numérico'}, template="plotly_dark", size='poder_total')
                st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Sem dados suficientes para gerar as análises estatísticas.")

    # Aba 03 - Simulador de Combate (Métrica de Valor de Portfólio).
    with aba_combate:
        st.markdown("#### ⚔️ Data Match-Up: Análise Comparativa de Combate")
        st.markdown("Selecione dois Pokémon para comparar suas estatísticas no banco de dados e determinar vantagens táticas.")
        
        lista_completa_nomes = sorted(df_pokemon['name'].unique().tolist())
        
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            p1_nome = st.selectbox("Escolha o primeiro Pokémon:", lista_completa_nomes, index=0)
        with col_sel2:
            p2_nome = st.selectbox("Escolha o segundo Pokémon:", lista_completa_nomes, index=min(1, len(lista_completa_nomes)-1))
            
        if p1_nome and p2_nome:
            p1_data = df_pokemon[df_pokemon['name'] == p1_nome].iloc[0]
            p2_data = df_pokemon[df_pokemon['name'] == p2_nome].iloc[0]
            
            # Layout de comparação lado a lado.
            col_p1, col_vs, col_p2 = st.columns([2, 1, 2])
            
            with col_p1:
                st.markdown(f"### {p1_data['name']}")
                nome_base1 = str(p1_data['name']).lower().strip()
                if "nidoran" in nome_base1:
                    nome_limpo1 = "nidoran-m" if "♂" in nome_base1 or "male" in nome_base1 else "nidoran-f"
                else:
                    nome_limpo1 = nome_base1.replace(" ", "-").replace("♂", "-m").replace("♀", "-f").replace(".", "").replace("'", "")
                st.image(f"https://img.pokemondb.net/artwork/large/{nome_limpo1}.jpg", width=180)
                st.markdown(f"**Tipo:** `{p1_data['tipo']}` | **HP:** `{p1_data['hp']}`")
                st.markdown(f"💥 **Ataque Principal:** {p1_data['attack']} ({p1_data['damage_num']} Dano)")
                
                # Regra de negócio: p1 tem vantagem contra p2?
                if str(p1_data['tipo']).lower() in str(p2_data['weak']).lower():
                    st.success("🔥 Vantagem Tática: Este Pokémon atinge a fraqueza do oponente!")
                    
            with col_vs:
                st.markdown("<h1 style='text-align: center; margin-top: 50px;'>VS</h1>", unsafe_allow_html=True)
                
            with col_p2:
                st.markdown(f"### {p2_data['name']}")
                nome_base2 = str(p2_data['name']).lower().strip()
                if "nidoran" in nome_base2:
                    nome_limpo2 = "nidoran-m" if "♂" in nome_base2 or "male" in nome_base2 else "nidoran-f"
                else:
                    nome_limpo2 = nome_base2.replace(" ", "-").replace("♂", "-m").replace("♀", "-f").replace(".", "").replace("'", "")
                st.image(f"https://img.pokemondb.net/artwork/large/{nome_limpo2}.jpg", width=180)
                st.markdown(f"**Tipo:** `{p2_data['tipo']}` | **HP:** `{p2_data['hp']}`")
                st.markdown(f"💥 **Ataque Principal:** {p2_data['attack']} ({p2_data['damage_num']} Dano)")
                
                # Regra de negócio: p2 tem vantagem contra p1?
                if str(p2_data['tipo']).lower() in str(p1_data['weak']).lower():
                    st.success("🔥 Vantagem Tática: Este Pokémon atinge a fraqueza do oponente!")

            # Bloco de insights comparativos (Engenharia de Dados + BI) para determinar o "vencedor estatístico" com base nas métricas do banco de dados.
            st.markdown("---")
            st.markdown("#### 🧠 O Veredito dos Dados (Data Insights)")
            
            # Cálculo das métricas absolutas e relativos para o componente st.metric.
            dif_hp = abs(p1_data['hp'] - p2_data['hp'])
            dif_dano = abs(p1_data['damage_num'] - p2_data['damage_num'])
            
            # Labels descritivos claros indicando quem possui a maior métrica.
            label_hp = f"Mais Vitalidade: {p1_data['name'] if p1_data['hp'] >= p2_data['hp'] else p2_data['name']}"
            label_dano = f"Mais Dano Bruto: {p1_data['name'] if p1_data['damage_num'] >= p2_data['damage_num'] else p2_data['name']}"
            
            if p1_data['hp'] == p2_data['hp']: label_hp = "Vitalidade (Empate)"
            if p1_data['damage_num'] == p2_data['damage_num']: label_dano = "Dano Bruto (Empate)"

            # Determina quem tem maior Poder Estatístico Geral.
            if p1_data['poder_total'] > p2_data['poder_total']:
                vencedor_estatistico = p1_data['name']
                vantagem_pts = p1_data['poder_total'] - p2_data['poder_total']
                detalhe_veredito = f"**{p1_data['name']}** possui uma vantagem combinada de **{vantagem_pts} pontos** sobre {p2_data['name']}."
            elif p2_data['poder_total'] > p1_data['poder_total']:
                vencedor_estatistico = p2_data['name']
                vantagem_pts = p2_data['poder_total'] - p1_data['poder_total']
                detalhe_veredito = f"**{p2_data['name']}** possui uma vantagem combinada de **{vantagem_pts} pontos** sobre {p1_data['name']}."
            else:
                vencedor_estatistico = "Empate Técnico"
                detalhe_veredito = "Ambos possuem o mesmo poder estatístico somado no banco de dados."

            # Renderiza as KPIs de forma limpa e profissional.
            col_v1, col_v2, col_v3 = st.columns(3)
            with col_v1:
                st.metric(label=label_hp, value=f"{p1_data['hp']} vs {p2_data['hp']}", delta=f"{dif_hp} HP de dif." if dif_hp > 0 else None)
            with col_v2:
                st.metric(label=label_dano, value=f"{int(p1_data['damage_num'])} vs {int(p2_data['damage_num'])}", delta=f"{dif_dano} pts de dif." if dif_dano > 0 else None)
            with col_v3:
                st.metric(label="Líder Estatístico Geral", value=vencedor_estatistico)
                
            # Caixa de texto contextualizada baseada nas fraquezas cruzadas.
            st.info(f"📋 **Análise de Cenário:** {detalhe_veredito}")
            
            # Adiciona uma camada de inteligência se houver vantagem elemental ativa.
            v1_efetivo = str(p1_data['tipo']).lower() in str(p2_data['weak']).lower()
            v2_efetivo = str(p2_data['tipo']).lower() in str(p1_data['weak']).lower()
            
            if v1_efetivo and not v2_efetivo:
                st.warning(f"⚠️ **Fator de Risco:** Apesar dos números brutos, **{p1_data['name']}** explora diretamente a fraqueza elemental de {p2_data['name']}, o que pode alterar o resultado prático!")
            elif v2_efetivo and not v1_efetivo:
                st.warning(f"⚠️ **Fator de Risco:** Apesar dos números brutos, **{p2_data['name']}** explora diretamente a fraqueza elemental de {p1_data['name']}, o que pode alterar o resultado prático!")

            # Gráfico de barras comparativo
            st.markdown("#### 📊 Comparativo Direto de Atributos")
            df_comp = pd.DataFrame([
                {"Pokémon": p1_data['name'], "Atributo": "Pontos de HP", "Valor": p1_data['hp']},
                {"Pokémon": p1_data['name'], "Atributo": "Dano do Ataque", "Valor": p1_data['damage_num']},
                {"Pokémon": p2_data['name'], "Atributo": "Pontos de HP", "Valor": p2_data['hp']},
                {"Pokémon": p2_data['name'], "Atributo": "Dano do Ataque", "Valor": p2_data['damage_num']}
            ])
            
            fig_comp = px.bar(
                df_comp, 
                x="Atributo", 
                y="Valor", 
                color="Pokémon", 
                barmode="group",
                template="plotly_dark",
                color_discrete_sequence=["#2C9BEF", "#FF421C"]
            )
            st.plotly_chart(fig_comp, use_container_width=True)
            
else:
    st.warning("Banco de dados vazio ou inacessível.")