import streamlit as st
import importlib
import json
import urllib.request
from openai import OpenAI

# ضبط إعدادات الصفحة
st.set_page_config(page_title="Space Generative RAG Engine", page_icon="🤖", layout="wide")

# دالة لجلب الموديلات المجانية المتاحة حالياً حيّة من OpenRouter
@st.cache_data(ttl=1800)  # تحديث القائمة تلقائياً كل 30 دقيقة
def fetch_live_free_models():
    url = "https://openrouter.ai/api/v1/models"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                # فلترة الموديلات المجانية الشغالة حالياً فقط
                free_models = [m['id'] for m in data.get('data', []) if ':free' in m['id']]
                if free_models:
                    return sorted(free_models)
    except Exception:
        pass
    # قائمة احتياطية في حال تعثر الاتصال
    return ["meta-llama/llama-3.3-70b-instruct:free", "qwen/qwen-2.5-72b-instruct:free"]

# استيراد دالة البحث من قاعدة البيانات
vdb_module = importlib.import_module("04_vector_db")
get_vector_db = vdb_module.get_vector_db
search_db = vdb_module.search_db

# تحميل قاعدة البيانات مرة واحدة (Caching)
@st.cache_resource
def load_db():
    return get_vector_db()

db = load_db()

# جلب قائمة الموديلات المجانية الحية
available_free_models = fetch_live_free_models()

# جلب المفتاح خفية وبشكل أوتوماتيكي كامل من الـ Secrets
openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY", "")

with st.sidebar:
    st.subheader("🤖 الموديلات المجانية المتاحة حالياً (الحية)")
    
    # اختيار الموديل من القائمة المجلوبة حياً من السيرفر
    model_choice = st.selectbox(
        "اختر نموذج الذكاء الاصطناعي:",
        options=available_free_models
    )
        "اختر نموذج الذكاء الاصطناعي:",
        options=available_free_models
    )
    
    st.caption(f"🟢 تم جلب {len(available_free_models)} موديل مجاني مجرّب وشغّال الآن من OpenRouter.")
    st.divider()

# عنوان التطبيق
st.title("🤖 Space Knowledge Generative RAG System")
st.markdown("بحث واسترجاع من قاعدة البيانات + توليد إجابة ذكية باستخدام OpenRouter.")

st.divider()

# منطقة الإدخال
col1, col2 = st.columns([3, 1])

with col1:
    user_query = st.text_input("💬 أكتب سؤالك بالعربية أو الإنجليزية:", placeholder="مثلاً: ما هو الثقب الأسود؟ أو What is the Artemis program?")

with col2:
    top_k = st.slider("عدد المصادر المسترجعة (Top K):", min_value=1, max_value=5, value=3)

# زر التوليد والبحث
if st.button("🚀 البحث وتوليد الإجابة", type="primary"):
    if not user_query.strip():
        st.error("رجاءً أدخل سؤالاً أو كلمة للبحث!")
    elif not openrouter_api_key.strip():
        st.warning("⚠️ يرجى إدخال مفتاح OpenRouter API Key في الشريط الجانبي (Sidebar) أولاً!")
    else:
        # 1. البحث والاسترجاع من قاعدة البيانات (Retrieval)
        with st.spinner("1️⃣ جاري البحث في قاعدة البيانات الاتجاهية (ChromaDB)..."):
            results = search_db(db, user_query, top_k=top_k)
            
        if results and 'documents' in results and results['documents'][0]:
            context_chunks = results['documents'][0]
            metadatas = results['metadatas'][0]
            
            # تجميع النصوص المسترجعة في سياق واحد (Context)
            context_text = "\n\n".join([f"Source [{i+1}]:\n{doc}" for i, doc in enumerate(context_chunks)])
            
            # صياغة الـ Prompt الهندسي الموجه
            # صياغة الـ Prompt المرن (يستعين بالمعلومات العامة لو الملفات ناقصة)
            prompt = f"""
You are an expert Space Science AI Assistant.
First, try to answer the user's question using the provided context below.
If the context contains the answer, base your response strictly on it.
If the context does NOT contain enough information, use your own general space knowledge to answer accurately, but add a brief note saying: "(Note: Answer complemented using general AI knowledge)".

Context:
{context_text}

User Question: {user_query}

Answer in a clean, professional, and well-structured manner (Answer in Arabic if asked in Arabic):
"""

            # 2. التوليد بواسطة OpenRouter (Generation)
            with st.spinner(f"2️⃣ جاري قراءة المستندات وتوليد الإجابة بواسطة ({model_choice})..."):
                try:
                    client = OpenAI(
                        base_url="https://openrouter.ai/api/v1",
                        api_key=openrouter_api_key,
                    )

                    completion = client.chat.completions.create(
                        model=model_choice,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )

                    response_text = completion.choices[0].message.content

                    st.success("✨ الإجابة المجهزة بواسطة الذكاء الاصطناعي (OpenRouter RAG Answer):")
                    st.markdown(response_text)
                    
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بـ OpenRouter API: {e}")

            st.divider()

            # 3. إظهار المصادر والمقاطع المسترجعة
            st.subheader("📚 المصادر والمقاطع التي اعتمد عليها الذكاء الاصطناعي (Context):")
            for idx, (doc_text, metadata) in enumerate(zip(context_chunks, metadatas)):
                with st.expander(f"📌 المصدر {idx + 1} - الملف: {metadata.get('source', 'غير معروف')}"):
                    st.write(doc_text)
                    
        else:
            st.warning("لم يتم العثور على معلومات مطابقة في قاعدة البيانات.")
