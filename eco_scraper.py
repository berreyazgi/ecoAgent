import os
import asyncio
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler
from ibm_watsonx_ai.foundation_models import ModelInference as Model

load_dotenv()

# Watsonx Yapılandırması
credentials = {"url": os.getenv("WATSONX_URL"), "apikey": os.getenv("WATSONX_APIKEY")}
project_id = os.getenv("PROJECT_ID")
model = Model(
    model_id="ibm/granite-3-8b-instruct",
    params={"decoding_method": "greedy", "max_new_tokens": 500},
    credentials=credentials,
    project_id=project_id
)

async def crawl_and_analyze(url):
    print(f"\n--- {url} taranıyor... ---")
    
    async with AsyncWebCrawler() as crawler:
        # Web sayfasını tarayıp Markdown'a çeviriyoruz
        result = await crawler.arun(url=url)
        raw_text = result.markdown[:4000] # Modeli yormamak için ilk 4000 karakteri alalım

        # Watsonx'e analiz yaptırıyoruz
        prompt = f"""
        Analyze the following web content and provide 3 practical water-saving tips.
        Content: {raw_text}

        Tips:
        """
        
        analysis = model.generate_text(prompt=prompt)
        return analysis

async def main():
    # Test için bir web sitesi seçelim
    target_url = "https://www.waterwise.org.uk/save-water/"
    result = await crawl_and_analyze(target_url)
    print("\nWatsonx Analizi:\n", result)

if __name__ == "__main__":
    asyncio.run(main())