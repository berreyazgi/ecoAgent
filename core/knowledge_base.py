from duckduckgo_search import DDGS

# --- SABİT VERİLER ---
SITE_DATABASE = {
    "opera": [
        {"name": "Devlet Opera ve Balesi", "url": "https://www.operabale.gov.tr", "type": "Resmi"},
    ],
    "hackathon": [
        {"name": "Kaggle", "url": "https://www.kaggle.com", "type": "Global"},
    ],
    "tiyatro": [
        {"name": "Tiyatrolar.com.tr", "url": "https://tiyatrolar.com.tr", "type": "Rehber"},
    ]
}

# --- FONKSİYONLAR ---

def search_online_sources(query: str, max_results=3):
    """DuckDuckGo ile internet araması yapar."""
    results = []
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=max_results))
            for r in search_results:
                results.append({
                    "name": r['title'],
                    "url": r['href'],
                    "type": "Web Sonucu",
                    "snippet": r['body']
                })
    except Exception as e:
        print(f"İnternet araması hatası: {e}") # Backend'de print loglaması daha güvenlidir
    return results

def get_best_sources(query: str, user_sites: list = None):
    """
    Yerel DB, Kullanıcı Siteleri ve İnterneti birleştirir.
    user_sites: Kullanıcının eklediği sitelerin listesi (Frontend'den gelir).
    """
    if user_sites is None:
        user_sites = []

    found_sites = []
    query_lower = query.lower()
    
    # A) Sabit Veritabanı Kontrolü
    for category, sites in SITE_DATABASE.items():
        if category in query_lower:
            found_sites.extend(sites)
            
    # B) Kullanıcının Eklediği Sitelerin Kontrolü
    # Not: Artık session_state yerine parametre olarak gelen listeyi kullanıyoruz.
    for site in user_sites:
        # Site verisinde 'category' anahtarı olmayabilir, kontrol edelim
        cat = site.get('category', '').lower()
        name = site.get('name', '').lower()
        
        if (cat in query_lower) or (query_lower in cat) or (query_lower in name):
            found_sites.append(site)
    
    # C) İnternet Araması
    web_results = search_online_sources(query)
    
    return found_sites + web_results