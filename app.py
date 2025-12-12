import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# Configuração da página
st.set_page_config(page_title="Gerador de Recibos Pro", page_icon="🧾")

st.title("🧾 Gerador de Recibos Profissional")
st.write("Preencha os dados abaixo para gerar seu documento.")

st.divider()

# --- BLOCO 1: LOGOMARCA (A NOVIDADE) ---
st.subheader("1. Identidade Visual")
logo_upload = st.file_uploader("Envie sua Logomarca (Opcional)", type=["png", "jpg", "jpeg"])

# --- BLOCO 2: DADOS DO PRESTADOR ---
st.subheader("2. Seus Dados")
col1, col2 = st.columns(2)
with col1:
    empresa_nome = st.text_input("Nome da Empresa/Prestador", placeholder="Ex: João Refrigeração")
with col2:
    empresa_contato = st.text_input("Telefone/WhatsApp", placeholder="(XX) 99999-9999")

# --- BLOCO 3: DADOS DO CLIENTE ---
st.subheader("3. Dados do Cliente")
cliente_nome = st.text_input("Nome do Cliente", placeholder="Ex: Maria da Silva")

# --- BLOCO 4: DETALHES DO SERVIÇO ---
st.subheader("4. Detalhes do Serviço")
descricao = st.text_area("Descrição", placeholder="Ex: Manutenção completa...")
valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

# --- LÓGICA DO PDF ---
def gerar_pdf(empresa, contato, cliente, desc, vlr, logo_path=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # SE TIVER LOGO, COLA ELA NO TOPO
    if logo_path:
        # x=10 (margem esq), y=8 (margem topo), w=30 (largura 30mm)
        try:
            pdf.image(logo_path, x=10, y=8, w=30)
            pdf.ln(5) # Um pequeno espaço extra se tiver logo
        except:
            st.error("Erro ao processar a imagem. Tente outra.")

    # Título (Centralizado) - Ajustado para não bater na logo
    pdf.set_font("Arial", 'B', 16)
    # Se tiver logo, empurra o título um pouco pra direita ou pra baixo
    if logo_path:
        pdf.cell(0, 10, txt="RECIBO DE PAGAMENTO", ln=True, align='C')
    else:
        pdf.cell(0, 10, txt="RECIBO DE PAGAMENTO", ln=True, align='C')
        
    pdf.ln(10)

    # Dados do Prestador
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"Prestador: {empresa}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Contato: {contato}", ln=True)
    
    pdf.line(10, 50, 200, 50)
    pdf.ln(10)

    # Corpo
    texto = f"Recebi(emos) de {cliente} a importância de R$ {vlr:.2f} referente aos serviços abaixo:"
    pdf.multi_cell(0, 10, txt=texto)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'I', 11)
    pdf.multi_cell(0, 10, txt=f"Descrição: {desc}")
    
    pdf.ln(20)
    
    # Data e Assinatura
    hoje = date.today().strftime("%d/%m/%Y")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Data: {hoje}", ln=True, align='R')
    
    pdf.ln(20)
    pdf.cell(0, 10, txt="_"*40, ln=True, align='C')
    pdf.cell(0, 10, txt="Assinatura", ln=True, align='C')

    return pdf.output(dest='S').encode('latin-1')

# --- BOTÃO ---
st.divider()

if st.button("Gerar Recibo com Logo 🎨", type="primary"):
    if not empresa_nome or not cliente_nome:
        st.error("Preencha o Nome da Empresa e do Cliente!")
    else:
        # Lógica para salvar a imagem temporariamente
        caminho_logo = None
        if logo_upload:
            caminho_logo = "temp_logo.png"
            with open(caminho_logo, "wb") as f:
                f.write(logo_upload.getbuffer())
        
        # Gera o PDF
        pdf_bytes = gerar_pdf(empresa_nome, empresa_contato, cliente_nome, descricao, valor, caminho_logo)
        
        # Limpa o arquivo temporário (boa prática)
        if caminho_logo and os.path.exists(caminho_logo):
            os.remove(caminho_logo)

        st.success("Recibo gerado!")
        st.download_button("📥 Baixar PDF", data=pdf_bytes, file_name="recibo.pdf", mime="application/pdf")
        
        # Link do Zap
        if empresa_contato:
             zap_limpo = empresa_contato.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
             link_zap = f"https://wa.me/55{zap_limpo}?text=Seu%20recibo%20est%C3%A1%20pronto."
             st.link_button("💬 Enviar no WhatsApp", link_zap)