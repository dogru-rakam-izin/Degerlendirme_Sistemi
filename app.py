import streamlit as st
import pandas as pd
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Doğru Rakam Özel Eğitim", layout="wide")

# --- BAŞLIK ---
st.title("🎯 Doğru Rakam Özel Eğitim Merkezi")
st.subheader("M-CHAT-R Otizm Tarama ve Takip Sistemi")

# --- MENÜ ---
menu = st.sidebar.selectbox("Menü", ["Yeni Test Uygula", "Kayıt Geçmişi"])

if menu == "Yeni Test Uygula":
    with st.form("mchat_form"):
        st.info("Lütfen öğrenci bilgilerini ve test sorularını eksiksiz doldurunuz.")
        
        # Öğrenci ve Öğretmen Bilgileri
        c1, c2, c3 = st.columns(3)
        with c1:
            ad_soyad = st.text_input("Öğrenci Ad Soyad")
        with c2:
            ay = st.number_input("Çocuğun Yaşı (Ay)", 16, 48, 24)
        with c3:
            ogretmen = st.text_input("Değerlendiren Öğretmen")

        st.divider()

        # M-CHAT-R SORULARI VE PUANLAMA MANTIĞI
        # Not: M-CHAT'te 2, 5 ve 12. sorular 'Evet' ise 1 puan; diğerleri 'Hayır' ise 1 puan kazandırır.
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            s1 = st.radio("1. Çocuğunuzu bir şeye bakması için işaret ettiğinizde bakar mı?", ["Evet", "Hayır"])
            s2 = st.radio("2. Çocuğunuzun işitme yeteneğinden hiç şüphelendiniz mi?", ["Evet", "Hayır"])
            s3 = st.radio("3. Çocuğunuz mış gibi yapar mı? (Örn: Boş bardaktan su içmek)", ["Evet", "Hayır"])
            s4 = st.radio("4. Çocuğunuz tırmanmayı sever mi?", ["Evet", "Hayır"])
            s5 = st.radio("5. Çocuğunuz gözlerinizin içine uzun süre bakar mı?", ["Evet", "Hayır"])
        
        with col_b:
            s6 = st.radio("6. Çocuğunuz işaret parmağıyla bir şeyi gösterir mi?", ["Evet", "Hayır"])
            s7 = st.radio("7. Çocuğunuz ilgi duyduğu şeyi size gösterir mi?", ["Evet", "Hayır"])
            s8 = st.radio("8. Çocuğunuz diğer çocuklarla ilgilenir mi?", ["Evet", "Hayır"])
            s9 = st.radio("9. Çocuğunuz size bir şey getirip gösterir mi?", ["Evet", "Hayır"])
            s10 = st.radio("10. Çocuğunuz ismine tepki verir mi?", ["Evet", "Hayır"])

        submit = st.form_submit_button("Sonucu Hesapla ve Veri Tabanına Kaydet")

        if submit:
            # PUANLAMA HESABI
            skor = 0
            # Soru 2, 5 ve 12 (burada 10 tanesini aldık örnek için) ters puanlanır
            if s1 == "Hayır": skor += 1
            if s2 == "Evet": skor += 1 # Ters soru
            if s3 == "Hayır": skor += 1
            if s4 == "Hayır": skor += 1
            if s5 == "Evet": skor += 1 # Ters soru
            if s6 == "Hayır": skor += 1
            if s7 == "Hayır": skor += 1
            if s8 == "Hayır": skor += 1
            if s9 == "Hayır": skor += 1
            if s10 == "Hayır": skor += 1

            # SONUÇ YORUMLAMA
            st.write(f"### Toplam Risk Skoru: {skor}")
            
            if skor <= 2:
                risk = "DÜŞÜK RİSK"
                st.success(f"Sonuç: {risk}. Gelişim takibine devam edilebilir.")
            elif 3 <= skor <= 7:
                risk = "ORTA RİSK"
                st.warning(f"Sonuç: {risk}. Takip testi yapılmalı veya uzman görüşü alınmalıdır.")
            else:
                risk = "YÜKSEK RİSK"
                st.error(f"Sonuç: {risk}. Acilen Çocuk Psikiyatrisi / RAM yönlendirmesi yapılmalıdır!")

            # BURADA KAYDETME FONKSİYONU ÇALIŞACAK (Adım 6)
            st.info("Veri tabanı bağlantısı bekleniyor... Veriler şu an yerel olarak hesaplandı.")
