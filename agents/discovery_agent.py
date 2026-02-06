import asyncio
from crawl4ai import AsyncWebCrawler
from core.models import EventData 

class DiscoveryAgent:
    async def discover_events(self, urls: list[str]) -> list[EventData]:
        print("Discovering events from URLs...")
        collected_data = []
        
        async with AsyncWebCrawler() as crawler:
            for raw_url in urls:
              
                url = raw_url.strip()
                
                if not url.startswith(("http://", "https://")):
                    print(f"Invalid URL format: {url}")
                    continue
                

                print(f"Scanning: {url}")
                try:
                    result = await crawler.arun(url=url)
                    
                    if not result.success:
                        print(f"Failed: {url} - Error: {result.error_message}")
                        continue

                    # Trust score mantığı
                    trusted_domains = [
                        ".gov", ".edu", ".gov.tr", ".edu.tr",
                        ".gov.uk", ".gouv.fr", ".bund.de",
                        ".go.jp", ".gov.cn", ".gov.in",
                        ".eu", ".int"
                    ]
                    trust = 0.9 if any(ext in url for ext in trusted_domains) else 0.5
                    
                    # Markdown içeriği al
                    desc = result.markdown[:500] if result.markdown else "Content not available."
                    
                    event = EventData(
                        title=f"Data from {url}",
                        description=desc, 
                        source_url=url,
                        trust_score=trust
                    )
                    collected_data.append(event)
                    
                except Exception as e:
                    print(f"Unexpected error ({url}): {e}")

        return collected_data

