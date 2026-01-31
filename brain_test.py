import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import Model

# .env dosyasındaki bilgileri yükle
load_dotenv()

# Ayarlar
credentials = {
    "url": os.getenv("WATSONX_URL"),
    "apikey": os.getenv("WATSONX_APIKEY")
}
project_id = os.getenv("PROJECT_ID")
model_id = "ibm/granite-3-0-8b-instruct" # Seçtiğimiz model

# Modeli Başlat
model = Model(
    model_id="ibm/granite-3-8b-instruct",
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 100
    },
    credentials=credentials,
    project_id=project_id
)

# Test Sorusu
prompt = "Sen bir Eco-Agent'sın. Su tasarrufu hakkında kısa bir slogan yaz."
response = model.generate_text(prompt=prompt)

print(f"Watsonx Cevabı: {response}")