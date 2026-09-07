import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="Gıda ve Kalori Analiz Asistanı", page_icon="🥗")
st.title("🥗 Akıllı Gıda ve Kalori Analiz Asistanı")
st.write("Tabağınızın fotoğrafını yükleyin; sistem GitHub'daki kaynak kütüphanenizi (sources klasörü) arka planda tarayarak uzman analizi yapsın!")

# 1. API Anahtarı
api_key = st.text_input("Gemini API Anahtarınızı yapıştırın:", type="password")

# 2. Yemek Fotoğrafı Yükleme
uploaded_file = st.file_uploader("Lütfen tabağın fotoğrafını yükleyin...", type=["jpg", "jpeg", "png"])

# GitHub'daki 'sources' klasöründen kaynakları otomatik okuma fonksiyonu
def load_sources_from_folder():
    sources_text = ""
    folder_path = "sources"
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        sources_text += f"\n\n--- KAYNAK DOSYA: {filename} ---\n{content}\n"
                except Exception as e:
                    # Okunamayan binary dosyaları atlıyoruz
                    pass
    return sources_text

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklediğiniz Tabağın Fotoğrafı", use_container_width=True)

    if st.button("🔍 Kütüphane Destekli Analizi Başlat"):
        if not api_key:
            st.warning("⚠️ Lütfen işlem yapmadan önce API Anahtarınızı girin.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('models/gemini-3.6-flash')
                
                # Aryadaki sources klasöründen tüm metinleri çekiyoruz
                library_knowledge = load_sources_from_folder()
                
                prompt = f"""
                Sen uzman bir gıda mühendisi ve diyetisyensin. 
                Sana aşağıda projeye ait kütüphane kaynakları (ders notları, teknik metinler) veriliyor. 
                Bu kaynaklardaki bilgileri, formülleri ve standartları baz alarak yüklenen yemek fotoğrafını detaylıca analiz et.
                
                KÜTÜPHANE KAYNAKLARIMIZ:
                {library_knowledge if library_knowledge else "Ek kaynak bulunamadı, genel gıda mühendisliği kurallarıyla devam et."}
                
                Şu bilgileri çıkar:
                1. Yemeğin/Yemeklerin tahmini adı ve içeriği
                2. Gözle görünen ana bileşenler
                3. Tahmini porsiyon büyüklüğü ve kalori miktarı (kcal)
                4. Makro besin değerleri (Protein, Karbonhidrat, Yağ)
                5. Kütüphanedeki kaynaklara dayalı teknik bir değerlendirme veya mühendislik yorumu.
                
                Bilgileri net, profesyonel ve Türkçe olarak listele.
                """
                
                contents = [prompt, image]

                with st.spinner("Yapay zeka kütüphanenizi tarıyor ve tabağınızı analiz ediyor... ⏳"):
                    response = model.generate_content(contents)
                    
                st.success("✅ Analiz Başarıyla Tamamlandı!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
