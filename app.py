import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
import streamlit as st
from engine.rules import PetAdvisor
from engine.facts import UserPreferences
from engine.facts import Animal

# Configuração da página
st.set_page_config(page_title="Pet Recommender", page_icon="🐾")

# Título e descrição
st.title("🐶🐱 Descubra seu Pet Ideal!")
st.markdown("Responda algumas perguntas e receba uma recomendação personalizada!")

# Formulário de perguntas
with st.form("pet_form"):
    st.subheader("Suas Preferências")
    
    espaco = st.selectbox(
        "Qual o espaço disponível?",
        ["Pequeno (apartamento)", "Médio (casa sem quintal)", "Grande (casa com quintal)"],
        key="espaco"
    )
    
    custo = st.selectbox(
        "Qual seu orçamento mensal para cuidados?",
        ["Baixo (até R$ 100)", "Médio (R$ 100-300)", "Alto (acima de R$ 300)"],
        key="custo"
    )
    
    energia = st.radio(
        "Seu nível de energia/atividade:",
        ["Baixo (sou tranquilo/a)", "Médio", "Alto (adoro atividades físicas)"],
        key="energia"
    )
    
    afeto = st.slider(
        "Quanto afeto você espera do pet?",
        1, 5, 3,
        key="afeto"
    )
    
    alergia = st.checkbox("Tenho alergia a pelo/penas", key="alergia")
    
    submit_button = st.form_submit_button("Descobrir meu pet!")

# Processamento ao enviar o formulário
if submit_button:
    # Mapeia respostas para o formato do sistema especialista
    espaco_map = {
        "Pequeno (apartamento)": "pequeno",
        "Médio (casa sem quintal)": "medio",
        "Grande (casa com quintal)": "grande"
    }
    
    custo_map = {
        "Baixo (até R$ 100)": "baixo",
        "Médio (R$ 100-300)": "medio",
        "Alto (acima de R$ 300)": "alto"
    }
    
    # Executa o motor de inferência
    engine = PetAdvisor()
    engine.reset()
    engine.declare(UserPreferences(
        espaco=espaco_map[espaco],
        custo=custo_map[custo],
        energia=energia.split(" ")[0].lower(),
        afeto="alto" if afeto >= 4 else "medio" if afeto == 3 else "baixo",
        alergia_pelo=alergia
    ))
    engine.run()
    
    # Exibe a recomendação
    st.subheader("🎉 Recomendação:")
    for fato in engine.facts:
        if isinstance(fato, Animal) and hasattr(fato, "recomendado"):
            st.success(f"**{fato['recomendado'].capitalize()}** é o pet perfeito para você!")
            st.image(f"images/{fato['recomendado']}.jpg", width=200)  # Adicione imagens em uma pasta /images/
            break
    else:
        st.warning("Nenhum pet encontrado. Ajuste suas preferências!")