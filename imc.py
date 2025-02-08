import streamlit as st
import requests
from io import BytesIO
from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);


file_id = "120BXxDp-v1y2Uh-KTce4wjbTrPpGXdG1"
download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

st.title("CALCULO DO :red[*IMC*]")
st.subheader("O :red[*IMC*] é uma forma de avaliar se uma pessoa está com o peso ideal, abaixo do peso, acima do peso ou :red[OBESA].")
st.markdown("---")


peso = st.number_input(label = "Insira seu :red[peso](kg):", value=None, placeholder="ex: 68,23")
altura = st.number_input(label = "Insira sua :red[altura](m):", value=None, placeholder="ex: 1,70")

st.markdown("---")

if st.button(":red[CONFIRMAR]"):
    st.markdown("---")
    imc = float(peso/(altura**2))
    imc = round(imc,2)
    st.subheader(f"O valor do seu :red[IMC] é: {imc}")
    st.markdown("---")
    # Substitua pelo ID do seu arquivo no Google Drive

    st.title("Baixe aqui uma dieta personalizada para o seu :red[*imc*]!")

    try:
        response = requests.get(download_url, timeout=10)
        response.raise_for_status()  # Lança erro se a requisição falhar

        pdf_data = BytesIO(response.content)

        st.download_button(
            label=":red[Baixe seu *PDF* aqui]",
            data=pdf_data,
            file_name="Dieta para Pessoas com Diferentes Faixas de IMC.pdf",
            mime="application/pdf"
        )

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao baixar o arquivo: {e}")
    
    if imc <= 18.5:
        st.subheader("Muito magro, está :red[abaixo do peso]")
    elif 18.5 < imc <= 24.9:
        st.subheader(":red[Excelente], está no peso ideal")
    elif 25 <= imc <= 29.9:
        st.subheader("Cuidado, está :red[acima do peso]")
    elif 30 <= imc <= 34.9:
        st.subheader("CUIDADO! Você tem :red[obesidade grau 1]")
    elif 35 <= imc <= 39.9:
        st.subheader("CUIDADO! Você tem :red[obesidade grau 2]")
    elif imc > 40:
        st.subheader(":red[EMAGRECIMENTO URGENTE, PROCURE UM MÉDICO, VOCÊ TEM OBESIDADE GRAU 3]")
    
    sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
    selected = st.feedback("thumbs")
    if selected is not None:
        st.markdown(f"Obrigado pelo {sentiment_mapping[selected]}")
