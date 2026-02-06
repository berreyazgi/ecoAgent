import os
from ibm_watsonx_ai.foundation_models import Model
from core.models import EventData

class ReasoningAgent:
    def __init__(self, credentials, project_id, model_id="ibm/granite-3-8b-instruct"):
        self.model = Model(
            model_id="ibm/granite-3-8b-instruct",
            credentials={
                "url": os.getenv("WATSONX_URL"),
                "apikey": os.getenv("WATSONX_APIKEY")
            },
            project_id=os.getenv("PROJECT_ID"),
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 1000, # Tablo için uzun cevap izni
                "repetition_penalty": 1.1
            }
        )

    def analyze_and_summarize(self, events: list[EventData]) -> str:
        # Verileri stringe çevir
        combined_text = "\n".join([f"SOURCE: {e.source_url}\nCONTENT: {e.description[:2000]}" for e in events])
        
        # --- PROMPT MÜHENDİSLİĞİ (TABLO FORMATI İÇİN) ---
        prompt = f"""
        You are a professional event analyst. Analyze the following raw web data.

        TASKS:
        1. Find the Event Name, Date, Location, and Type from the text.
        2. Convert the dates to "DD.MM.YYYY" format (Normalize).
        3. **EXPECTED to be a Markdown Table.**
        4. Write a short executive summary below the table.

        Data:
        {combined_text}

        ANSWER IN MARKDOWN TABLE FORMAT:
        | Activity Name | Date | Location | Type | Source |
        |---|---|---|---|---|
        | ... | ... | ... | ... | ... |

        Analysis Summary:
        """
        
        return self.model.generate_text(prompt)