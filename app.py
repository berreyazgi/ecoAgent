import streamlit as st
import asyncio
import pandas as pd
from orchestrator import EventOrchestrator

# Sayfa Ayarları
st.set_page_config(page_title="AI Event Assistant", page_icon="🎭", layout="wide")

# Orchestrator'ı Başlat (Singleton yapısı: Sayfa yenilense de hafızada kalsın)
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = EventOrchestrator()

# --- Başlık ve Giriş Alanı ---
st.title("🎭 AI Event Assistant")
st.markdown("Yapay zeka destekli etkinlik ve hackathon arama asistanı.")

# Yan yana giriş alanları için kolonlar
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("Ne aramak istiyorsun?", "Ankara Devlet Opera ve Balesi Programı")
with col2:
    user_prefs = st.multiselect("İlgi Alanların", ["Opera", "Tiyatro", "Hackathon", "Bale", "Konser"])

# --- Analiz Butonu ---
if st.button("Etkinlikleri Bul", type="primary", use_container_width=True):
    if not query:
        st.warning("Lütfen bir arama konusu girin.")
    else:
        with st.spinner("🕵️ Ajanlar siteleri tarıyor ve analiz ediyor..."):
            # Tüm karmaşık işi Orchestrator halleder
            results = asyncio.run(st.session_state.orchestrator.process_query(query, user_prefs))
            
            if not results:
                st.info("Bu kriterlere uygun etkinlik bulunamadı veya sitelere erişilemedi.")
            else:
                st.success("Analiz Tamamlandı! İşte sonuçlar:")
                
                # --- Sonuçları Listeleme ---
                for item in results:
                    with st.expander(f"📍 Kaynak: {item['source']} (Güven Skoru: {item['trust_score']}/10)", expanded=True):
                        # Hata mesajı varsa göster
                        if "error" in item:
                            st.error(f"Hata: {item['error']}")
                        else:
                            # JSON verisini tabloya çevirip gösterelim
                            events_data = item.get('events', [])
                            if isinstance(events_data, list) and events_data:
                                df = pd.DataFrame(events_data)
                                st.dataframe(df, use_container_width=True, hide_index=True)
                            else:
                                st.write(events_data) # JSON liste değilse düz metin yaz