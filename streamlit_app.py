import streamlit as st
import requests
import pandas as pd

# URL da API do ThingSpeak para coletar dados
THINGSPEAK_FEEDS_URL = "https://api.thingspeak.com/channels/2707291/feeds.json?api_key=H0ZZ4BGAW2I73FRE&results=10"  

def fetch_data():
    response = requests.get(THINGSPEAK_FEEDS_URL)
    data = response.json()
    print(data)  #response da API
    if 'feeds' in data:
        feeds = data['feeds']
        return pd.DataFrame(feeds)
    else:
        return pd.DataFrame()  # Retorna um DataFrame vazio se 'feeds' não existir

st.title("Sistema de Alerta IoT - Monitoramento em Tempo Real")

# Coleta de dados do ThingSpeak
df = fetch_data()

# Verificar se o DataFrame não está vazio antes de plotar
if not df.empty:
    # Converção dos campos para numérico
    df['Botao'] = pd.to_numeric(df['field1'], errors='coerce')
    df['Temperatura'] = pd.to_numeric(df['field2'], errors='coerce')

    # Visualização dos alertas e dados do sensor
    st.subheader("Alertas de Botão e Sensores")
    st.line_chart(df[['Botao', 'Temperatura']])  # field1 para botão, field2 para temperatura

    # Mapa interativo (exemplo usando coordenadas fictícias)
    st.subheader("Localização Aproximada do Dispositivo")
    st.map(pd.DataFrame({'lat': [-8.05], 'lon': [-34.9]}))  # Recife, PE como exemplo
else:
    st.warning("Nenhum dado disponível.")

# Função de Notificação
def send_email():
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText("Alerta de temperatura ou botão pressionado!")
    msg['Subject'] = "Alerta IoT"
    msg['From'] = "kekav64024@jameagle.com"  # Altere para seu e-mail
    msg['To'] = "kekav64024@jameagle.com"  # Altere para o e-mail do destinatário

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("kekav64024@jameagle.com", "kekav64024@jameagle.com")  # Altere para suas credenciais
        server.send_message(msg)

if st.button("Enviar Alerta por E-mail"):
    send_email()
    st.success("Alerta enviado!")
