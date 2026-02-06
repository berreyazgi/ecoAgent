import asyncio
import os
from dotenv import load_dotenv
# Bu importların senin 'agents' klasöründe olduğunu varsayıyorum
from agents.discovery_agent import DiscoveryAgent 
from agents.reasoning_agent import ReasoningAgent

load_dotenv()

class EventOrchestrator:
    def __init__(self):
        # Ajanları başlatıyoruz
        self.discovery = DiscoveryAgent()
        
        credentials = {
            "url": os.getenv("WATSONX_URL"),
            "apikey": os.getenv("WATSONX_APIKEY")
        }
        self.reasoning = ReasoningAgent(credentials, os.getenv("PROJECT_ID"))
        
        # Basit Önbellek (Cache)
        self.cache = {} 

    async def process_query(self, query: str, user_preferences: list = None):
        """
        Kullanıcı isteğini yöneten ana fonksiyon.
        Güvenlik önlemleri (Strip, HTTP check, Try-Except) burada uygulanır.
        """
        
        # 1. Önbellek Kontrolü
        if query in self.cache:
            return self.cache[query]

        # 2. Hedef URL'leri Belirleme (Burada Watsonx veya Google Search API kullanılabilir)
        # Şimdilik örnek URL listesi:
        raw_urls = [
            " https://www.operabale.gov.tr ",  # Boşluklu (Test için)
            "www.biletix.com",                # Hatalı: http yok (Test için)
            "https://tiyatrolar.com.tr"       # Düzgün
        ]

        combined_results = []

        # 3. Güvenli Tarama Döngüsü
        for raw_url in raw_urls:
            # --- GÜVENLİK ÖNLEMİ 1: Temizlik ---
            url = raw_url.strip() # Görünmez boşlukları sil

            # --- GÜVENLİK ÖNLEMİ 2: Protokol Kontrolü ---
            if not url.startswith("http"):
                print(f"⚠️ Geçersiz URL atlandı: {url}")
                continue # Döngünün başına dön, bu URL'yi pas geç

            # --- GÜVENLİK ÖNLEMİ 3: Hata Yakalama (Try-Except) ---
            try:
                print(f"🔍 Taranıyor: {url}")
                
                # Discovery Agent ile veriyi çek
                raw_data = await self.discovery.fetch_content(url)
                
                # Reasoning Agent ile veriyi işle
                structured_events = self.reasoning.extract_events(raw_data)
                
                # Sonuçları listeye ekle
                combined_results.append({
                    "source": url,
                    "trust_score": raw_data.get('trust_score', 5),
                    "events": structured_events
                })
                
            except Exception as e:
                # Bir site çökerse program durmasın, hatayı kaydet ve devam et
                print(f"❌ Hata oluştu ({url}): {e}")
                combined_results.append({
                    "source": url,
                    "trust_score": 0,
                    "error": f"Siteye erişilemedi: {str(e)}"
                })

        # Sonuçları önbelleğe kaydet
        self.cache[query] = combined_results
        return combined_results