import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
import streamlit as st
from experta import Fact
from engine.rules import PetAdvisor
from engine.facts import UserPreferences, Animal

# Configuração da página
st.set_page_config(page_title="Pet Recommender", page_icon="🐾")

# Título e descrição
st.title("🐶🐱 Descubra seu Pet Ideal!")
st.markdown("Responda algumas perguntas e receba uma recomendação personalizada! 🎉")

# Formulário de perguntas
with st.form("pet_form"):
    st.subheader("Preencha seu perfil")

    # Tipo de moradia
    tipo_casa = st.selectbox(
        "🏠 Tipo de moradia:",
        ["Apartamento", "Casa", "Condomínio"],
        key="tipo_casa"
    )

    # Espaço disponível
    espaco = st.radio(
        "🛋️ Espaço disponível:",
        ["Pequeno", "Médio", "Grande"],
        key="espaco"
    )

    # Orçamento mensal
    custo = st.selectbox(
        "💰 Orçamento mensal:",
        ["Baixo", "Médio", "Alto"],
        key="custo"
    )

    # Nível de energia
    energia = st.slider(
        "⚡ Seu nível de energia:",
        1, 5, 3,
        help="Quão ativo(a) você é no dia a dia?",
        key="energia"
    )

    # Necessidade de afeto
    afeto = st.slider(
        "💖 Necessidade de afeto:",
        1, 5, 3,
        help="Quanto carinho você espera do pet?",
        key="afeto"
    )

    # Tempo disponível
    tempo_disponivel = st.selectbox(
        "⏰ Tempo livre diário:",
        ["muito", "medio", "pouco"],
        key="tempo_disponivel"
    )

    # Interação desejada
    interacao = st.checkbox(
        "🤝 Desejo interagir com meu pet?",
        key="interacao"
    )

    # Alergia a pelos/penas
    alergia = st.checkbox(
        "🤧 Tenho alergia a pelo/penas",
        key="alergia"
    )

    # Nojo a roedores
    nojo_roedor = st.checkbox(
        "🚫 Tenho nojo de roedores",
        key="nojo_roedor"
    )

    # Ambiente rural
    ambiente_rural = st.checkbox(
        "🌾 Moro em área rural",
        key="ambiente_rural"
    )

    # Animal exótico
    animal_exotico = st.checkbox(
        "🦎 Tenho interesse em animal exótico",
        key="animal_exotico"
    )

    submit_button = st.form_submit_button("🔍 Descobrir meu pet!")

# ---- Processamento ----
if submit_button:
    # Função utilitária para mapear níveis de 1-5 para categorias
    def nivel_valor(valor):
        if valor <= 2:
            return "baixo"
        if valor >= 4:
            return "alto"
        return "medio"

    # Reset e declaração de preferências corretamente
    engine = PetAdvisor()
    engine.reset()
    engine.declare(UserPreferences(
        tipo_casa=tipo_casa,
        espaco=espaco.lower(),
        custo=custo.lower(),
        energia=nivel_valor(energia),
        afeto=nivel_valor(afeto),
        tempo_disponivel=tempo_disponivel,
        interacao_desejada=interacao,
        alergia_pelo=alergia,
        nojo_roedor=nojo_roedor,
        ambiente_rural=ambiente_rural,
        animal_exotico=animal_exotico
    ))
    engine.run()

    # Exibição de resultados
    st.subheader("🎉 Recomendação:")
    recomendacao = None
    for fato in engine.facts.values():
        if isinstance(fato, Animal) and "recomendado" in fato:
            recomendacao = fato["recomendado"]
            break

    if recomendacao:
        st.success(f"**{recomendacao.capitalize()}** é o pet perfeito para você!")
        st.image(f"images/{recomendacao}.jpg", width=300)
    else:
        st.warning("Nenhum pet perfeito encontrado. Tente ajustar suas preferências!")