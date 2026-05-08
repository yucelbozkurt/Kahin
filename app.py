from flask import Flask, render_template, request, jsonify
from google import genai
import random

app = Flask(__name__)

# --- YAPILANDIRMA ---
API_KEY = "AIzaSyA5g6turdbSOENfYzhC1crEafoAI8bpkmo" # Google AI Studio'dan aldığın anahtar
client = genai.Client(api_key=API_KEY)

# Kullanıcıya özel "Küçük Mesajlar" havuzu
ozel_mesajlar = [
    "Bugün yaydığın enerji o kadar tatlı ki, gökyüzü bile sana gülümsüyor! ✨",
    "Küçük patilerin büyük adımları seni harika yerlere götürecek, unutma. 🐾",
    "Yıldızlar bugün senin cesaretini fısıldıyor, hayallerine sıkıca sarıl. 💖",
    "Senin kalbin bir kristal kadar berrak, bugün o ışığı dışarı yansıtma vakti! 🔮"
]

@app.route('/')
def ana_sayfa():
    return render_template('index.html')

@app.route('/kehanet-al', methods=['POST'])
def kehanet_al():
    veri = request.json
    isim = veri.get('isim', 'Gizemli Yolcu')
    
    # Özel küçük mesaj seçimi
    rastgele_mesaj = random.choice(ozel_mesajlar)
    
    prompt = f"""
    Sen 'Kristal Patiler' adında, dünyanın en tatlı ve bilge kahinisin. 
    Kullanıcının adı: {isim}. 
    Ona özel, çok şirin, komik ve umut verici bir günlük kehanet yaz. 
    Mesajında mutlaka {isim} ismini geçir ve ona ismen hitap et.
    Cevabın 3 cümleyi geçmesin. 
    Sonuna 'Günün Şanslı Objesi: [Obje]' ekle ve ' Şunu unutma :Seni birisi çok seviyor onu görmezden gelme' de
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return jsonify({
            "kehanet": response.text,
            "ozel_mesaj": rastgele_mesaj
        })
    except Exception as e:
        return jsonify({"hata": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
