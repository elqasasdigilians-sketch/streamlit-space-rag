import urllib.request
import json
import os

# مواضيع الفضاء التي سيتم تحميلها
space_topics = [
    "Space_exploration",
    "NASA",
    "James_Webb_Space_Telescope",
    "Mars",
    "Black_hole",
    "Moon",
    "Solar_System",
    "Hubble_Space_Telescope",
    "International_Space_Station",
    "Artemis_program"
]

os.makedirs("data", exist_ok=True)

print("⏳ جاري تحميل مقالات الفضاء الحقيقية وصنع ملفات .txt...\n")

for topic in space_topics:
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={topic}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'SpaceRAGApp/1.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            pages = data['query']['pages']
            for page_id, page_data in pages.items():
                content = page_data.get('extract', '')
                if content:
                    file_path = os.path.join("data", f"{topic}.txt")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"✅ تم تحميل وتخزين: {topic}.txt")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء تحميل {topic}: {e}")

print("\n🎉 اكتمل تحميل كافة الملفات النصية بنجاح داخل مجلد data/!")