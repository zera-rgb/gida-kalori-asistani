import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Yemek Kalori Hesaplayıcı", page_icon="🥗")
st.title("📸 Yapay Zeka ile Kalori Hesaplayıcı")
st.write("Tabağınızın fotoğrafını yükleyin, yapay zeka yemeği tanıyıp kalorisini tahmin etsin!")

api_key = st.text_input("Gemini API Anahtarınızı yapıştırın:", type="password")
uploaded_file = st.file_uploader("Lütfen yemeğin fotoğrafını yükleyin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklediğiniz Tabağın Fotoğrafı", use_container_width=True)

    if st.button("🔍 Kaloriyi Hesapla"):
        if not api_key:
            st.warning("⚠️ Lütfen işlem yapmadan önce API Anahtarınızı girin.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('models/gemini-3.6-flash')
                
                prompt = """
                Sen uzman bir diyetisyen ve kalori hesaplama uzmanısın. 
                Sana verilen bu yemek fotoğrafını analiz et ve lütfen bana şu bilgileri çıkar:
                
                1. Yemeğin/Yemeklerin tahmini adı
                2. Gözle görünen ana malzemeler
                3. Tahmini porsiyon büyüklüğü
                4. **Tahmini toplam kalori miktarı (kcal)**
                5. Makro besin değerleri (Protein, Karbonhidrat, Yağ gramajları)
                
                Bilgileri net, samimi ve okunaklı bir şekilde Türkçe olarak listele. 
                (Bu değerlerin tahmini olduğunu da belirt.)
                """
                
                with st.spinner("Yapay zeka tabağınızı analiz ediyor, lütfen bekleyin... ⏳"):
                    response = model.generate_content([prompt, image])
                    
                st.success("✅ Analiz Başarıyla Tamamlandı!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")