import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Doğru Rakam Özel Eğitim", layout="wide", page_icon="🎯")

# --- GOOGLE SHEETS BAĞLANTISI ---
# secrets.toml dosyanı otomatik olarak kullanır
conn = st.connection("gsheets", type=GSheetsConnection)

# --- BAŞLIK VE KURUMSAL KİMLİK ---
st.title("🎯 Doğru Rakam Özel Eğitim Merkezi")
st.subheader("Dijital Değerlendirme ve Kayıt Sistemi")

# --- YAN MENÜ ---
menu = st.sidebar.selectbox("İşlem Menüsü", ["M-CHAT Testi Uygula", "Geçmiş Kayıtları İncele"])

if menu == "M-CHAT Testi Uygula":
    st.write("### M-CHAT-R/F Otizm Tarama Ölçeği")
    st.info("Bu test 16-30 ay arası çocuklar için ön değerlendirme amaçlıdır.")

    with st.form("mchat_form"):
        # 1. BÖLÜM: KİMLİK BİLGİLERİ
        c1, c2, c3 = st.columns(3)
        with c1:
            ad_soyad = st.text_input("Öğrenci Ad Soyad")
        with c2:
            ay = st.number_input("Çocuğun Yaşı (Ay)", 16, 48, 24)
        with c3:
            ogretmen = st.text_input("Değerlendiren Öğretmen")

        st.divider()

        # 2. BÖLÜM: TEST SORULARI (20 SORU)
        st.write("**Lütfen soruları gözlemlerinize dayanarak 'Evet' veya 'Hayır' şeklinde yanıtlayın.**")
        
        col_sol, col_sag = st.columns(2)
        
        with col_sol:
            s1 = st.radio("1. İşaret ettiğiniz yere bakar mı?", ["Evet", "Hayır"])
            s2 = st.radio("2. İşitme kaybı şüpheniz var mı?", ["Evet", "Hayır"]) # Ters
            s3 = st.radio("3. 'Mış gibi' oyun oynar mı?", ["Evet", "Hayır"])
            s4 = st.radio("4. Tırmanmayı sever mi?", ["Evet", "Hayır"])
            s5 = st.radio("5. Göz teması kurar mı?", ["Evet", "Hayır"])
            s6 = st.radio("6. İstediği şeyi parmağıyla gösterir mi?", ["Evet", "Hayır"])
            s7 = st.radio("7. İlgi duyduğu şeyi size gösterir mi?", ["Evet", "Hayır"])
            s8 = st.radio("8. Diğer çocuklarla ilgilenir mi?", ["Evet", "Hayır"])
            s9 = st.radio("9. Size bir şey getirip gösterir mi?", ["Evet", "Hayır"])
            s10 = st.radio("10. İsmine tepki verir mi?", ["Evet", "Hayır"])

        with col_sag:
            s11 = st.radio("11. Size gülümser mi?", ["Evet", "Hayır"])
            s12 = st.radio("12. Günlük seslerden rahatsız olur mu?", ["Evet", "Hayır"]) # Ters
            s13 = st.radio("13. Yürür mü?", ["Evet", "Hayır"])
            s14 = st.radio("14. Gözünüzün içine bakar mı?", ["Evet", "Hayır"])
            s15 = st.radio("15. Hareketlerinizi taklit eder mi?", ["Evet", "Hayır"])
            s16 = st.radio("16. Başınızı çevirdiğiniz yere bakar mı?", ["Evet", "Hayır"])
            s17 = st.radio("17. Sizin ona bakmanızı sağlar mı?", ["Evet", "Hayır"])
            s18 = st.radio("18. Söylediğinizi anlıyor gibi mi?", ["Evet", "Hayır"])
            s19 = st.radio("19. Olağandışı bir durum olursa size bakar mı?", ["Evet", "Hayır"])
            s20 = st.radio("20. Hareketli oyunları sever mi?", ["Evet", "Hayır"])

        # KAYDET BUTONU
        submit = st.form_submit_button("Sonucu Hesapla ve Kaydet")

        if submit:
            if not ad_soyad or not ogretmen:
                st.warning("Lütfen öğrenci ve öğretmen adını giriniz.")
            else:
                # PUANLAMA MANTIĞI (M-CHAT-R Standardı)
                skor = 0
                cevaplar = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20]
                
                # Soru 2, 5 ve 12 "Evet" ise risk puanı; diğerleri "Hayır" ise risk puanı
                for i, cevap in enumerate(cevaplar):
                    soru_no = i + 1
                    if soru_no in [2, 5, 12]:
                        if cevap == "Evet": skor += 1
                    else:
                        if cevap == "Hayır": skor += 1

                # RİSK ANALİZİ
                if skor <= 2: risk, renk = "DÜŞÜK RİSK", "green"
                elif 3 <= skor <= 7: risk, renk = "ORTA RİSK", "orange"
                else: risk, renk = "YÜKSEK RİSK", "red"

                # GOOGLE SHEETS'E KAYIT
                yeni_veri = pd.DataFrame([{
                    "Tarih": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Öğretmen": ogretmen,
                    "Öğrenci": ad_soyad,
                    "Yaş (Ay)": ay,
                    "Skor": skor,
                    "Risk": risk
                }])

                # Veriyi mevcut tabloya ekle
                try:
                    mevcut_veri = conn.read(worksheet="mchat_kayitlari")
                    guncel_tablo = pd.concat([mevcut_veri, yeni_veri], ignore_index=True)
                    conn.update(worksheet="mchat_kayitlari", data=guncel_tablo)
                    
                    st.divider()
                    st.markdown(f"### Değerlendirme Sonucu: :{renk}[{risk}]")
                    st.write(f"**Toplam Risk Puanı:** {skor}")
                    st.success("Veri başarıyla Doğru Rakam veri tabanına kaydedildi!")
                except Exception as e:
                    st.error(f"Veri kaydedilirken bir hata oluştu: {e}")

elif menu == "Geçmiş Kayıtları İncele":
    st.write("### Kurum Kayıt Geçmişi")
    try:
        veriler = conn.read(worksheet="mchat_kayitlari")
        st.dataframe(veriler, use_container_width=True)
    except:
        st.warning("Henüz kaydedilmiş bir veri bulunamadı veya sayfa ismi 'mchat_kayitlari' değil.")
