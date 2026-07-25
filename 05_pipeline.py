import urllib.request
import json
import importlib

def generate_answer(query, db, api_key, model_name="meta-llama/llama-3.3-70b-instruct:free", top_k=3):
    # 1️⃣ البحث في قاعدة البيانات لاسترجاع النصوص ذات الصلة
    try:
        vdb_module = importlib.import_module("04_vector_db")
        search_db = vdb_module.search_db
        docs = search_db(db, query, top_k=top_k)
    except Exception:
        docs = []

    # تجهيز النصوص المسترجعة
    sources_text = []
    for doc in docs:
        if hasattr(doc, 'page_content'):
            sources_text.append(doc.page_content)
        else:
            sources_text.append(str(doc))

    context = "\n\n---\n\n".join(sources_text) if sources_text else "لا توجد مصادر مسترجعة ذات صلة مباشرة."

    # 2️⃣ صياغة الـ Prompt المحكم بزجاج حماية (Guardrails) لمنع الخروج عن نطاق الفضاء
    system_instruction = """أنت مساعد ذكاء اصطناعي متخصص حصرياً في علوم الفضاء، الفلك، المجرات، الأجسام السماوية، واستكشاف الفضاء.

🚨 قواعد صارمة جداً يجب اتباعها حرفياً:
1. فحص مجال السؤال: إذا كان سؤال المستخدم خارج نطاق الفضاء وعلوم الفلك (مثل: الطبخ، الكيك، الرياضة، البرمجة العامة، السياسة، الحياة اليومية، إلخ)، يُحظر عليك إجابة السؤال إطلاقاً، ويجب عليك الرد فوراً بالرسالة التالية فقط (حسب لغة السؤال):
   - بالعربية: "عذراً، هذا النظام مخصص فقط للإجابة عن الأسئلة المتعلقة بالفضاء وعلوم الفلك واستكشاف الكون."
   - بالإنجليزية: "Sorry, this system is strictly dedicated to answering questions related to space, astronomy, and space exploration."

2. إذا كان السؤال متعلقاً بالفضاء وعلوم الفلك:
   - استخدم المصادر المرفقة أدناه كمرجع أولي للحصول على المعلومات.
   - إذا كانت المصادر غير كافية أو لا تحتوي على كافة التفاصيل، يُسمح لك باستكمال الإجابة والتوسع فيها باستخدام معرفتك العلمية الذاتية، بشرط أن تظل الإجابة حصرياً في نطاق علوم الفضاء والفلك.
"""

    prompt = f"""{system_instruction}

المصادر والمراجع المرفقة من قاعدة البيانات:
{context}

سؤال المستخدم:
{query}

الإجابة:"""

    # 3️⃣ الإرسال إلى OpenRouter API
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.io",
        "X-Title": "Space Knowledge RAG"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1  # درجة حرارة منخفضة لضمان الالتزام الصارم بالقواعد
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                result = json.loads(response.read().decode('utf-8'))
                answer = result['choices'][0]['message']['content']
            else:
                answer = f"خطأ في الاتصال بالنموذج (Status Code: {response.status})"
    except Exception as e:
        answer = f"تعذر توليد الإجابة من النموذج: {e}"

    return {
        "answer": answer,
        "sources": sources_text
    }
