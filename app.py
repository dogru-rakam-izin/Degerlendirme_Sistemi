import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Doğru Rakam Değerlendirme", layout="centered")

# Kurumsal Başlık
st.title("🎯 Doğru Rakam Özel Eğitim")
st.subheader("Dijital Değerlendirme ve Takip Paneli")

# Yan Menü (Sidebar)
menu = st.sidebar.selectbox("İşlem Seçiniz", ["Ana Sayfa", "M-CHAT Testi Uygula", "Geçmiş Kayıtlar"])

if menu == "Ana Sayfa":
    st.info("Hoş geldiniz. Sol menüden uygulamak istediğiniz testi seçerek işleme başlayabilirsiniz.")
    # Buraya kurumun vizyonu veya kısa bir kullanım kılavuzu eklenebilir.

elif menu == "M-CHAT Testi Uygula":
    st.write("### M-CHAT-R Otizm Tarama Ölçeği")
    st.caption("16-30 ay arası çocuklar için uygundur.")
    
    # Form Alanı
    with st.form("test_formu"):
        col1, col2 = st.columns(2)
        with col1:
            ogrenci = st.text_input("Öğrenci Ad Soyad")
            ogretmen = st.text_input("Değerlendiren Öğretmen")
        with col2:
            ay = st.number_input("Çocuğun Yaşı (Ay)", min_value=16, max_value=48)
            tarih = st.date_input("Test Tarihi")
            
        st.divider()
        st.write("**Lütfen soruları gözlemlerinize göre yanıtlayın:**")
        
        # Örnek bir soru yapısı
        s1 = st.radio("1. Çocuğunuzu bir şeye bakması için işaret ettiğinizde bakar mı?", ["Evet", "Hayır"])
        
        submit = st.form_submit_button("Sonucu Hesapla ve Kaydet")
