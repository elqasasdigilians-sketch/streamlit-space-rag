import streamlit as st
import importlib
import urllib.request
import json

# 1️⃣ ضبط إعدادات الصفحة والـ Dark Mode
st.set_page_config(
    page_title="Space Knowledge RAG System",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2️⃣ تصميم الخلفية الفضائية والـ Dark Mode وتأثير الـ Hover المميز لمربع الإدخال
space_css = """
<style>
/* خلفية الفضاء العالية الدقة */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* الشريط الجانبي (Glassmorphism Dark) */
[data-testid="stSidebar"] {
    background-color: rgba(11, 15, 25, 0.88) !important;
    backdrop-filter: blur(12px);
    border-left: 1px solid rgba(255, 255, 255, 0.1);
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0) !important;
}

/* تحويل كل النصوص للون الأبيض */
h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown {
    color: #FFFFFF !important;
}

/* 🎯 تأثير الـ Hover والـ Bold الثقيل لمربع الإدخال (Input Box) */
.stTextInput input {
    background-color: rgba(255, 255, 255, 0.08) !important;
    color: white !important;
    border-radius: 10px !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    font-size: 16px !important;
    transition: all 0.3s ease-in-out !important;
}

/* عند مرور الماوس (Hover) أو الضغط عليه (Focus) */
.stTextInput input:hover, .stTextInput input:focus {
    border: 2px solid #ff4b4b !important; /* إطار أحمر فضائي نيون */
    box-shadow: 0 0 20px rgba(255, 75, 75, 0.85) !important; /* توهج خيالي حول المربع */
    font-weight: 900 !important; /* خط BOLD ثقيل جداً */
    background-color: rgba(255, 255, 255, 0.18) !important;
    transform: translateY(-2px) scale(1.01); /* حركة بروز راقية */
}

/* تصميم زر البحث */
.stButton > button {
    background: linear-gradient(90deg, #ff4b4b 0%, #ff7b54 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    font-size: 16px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease-in-out !important;
}

.stButton > button:hover {
    box-shadow: 0 0 15px rgba(255, 75, 75, 0.9) !important;
    transform: scale(1.03) !important;
}
</style>
"""
st.markdown(space_css, unsafe_allow_html=True)

# جلب قائمة الموديلات المجانية
def fetch_live_free_models():
    try:
        url = "https://openrouter.ai/api/v1/models"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                free_models = [m['id'] for m in data.get('data', []) if ':free' in m['id']]
                if free_models:
                    return sorted(free_models)
    except Exception:
        pass
    return ["meta-llama/llama-3.3-70b-instruct:free", "qwen/qwen-2.5-72b-instruct:free"]

# استيراد قاعدة البيانات - (تم إصلاح اسم الدالة هنا search_db)
vdb_module = importlib.import_module("04_vector_db")
get_vector_db = vdb_module.get_vector_db
search_db = vdb_module.search_db

@st.cache_resource
def load_db():
    return get_vector_db()

db = load_db()

available_free_models = fetch_live_free_models()

# جلب الـ API Key في الخفاء
openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY", "")

# 3️⃣ القائمة الجانبية (Sidebar)
with st.sidebar:
    # محاولة عرض صورتك الشخصية لو رفعتها باسم my_photo.png أو استخدام الأيقونة
    try:
        st.image("my_photo.png", width=110)
    except:
        st.image("my_photo.png.png", width=110)
    
    st.subheader("🤖 الموديلات المتاحة")
    
    model_choice = st.selectbox(
        "اختر نموذج الذكاء الاصطناعي:",
        options=available_free_models
    )
    
    st.caption(f"🟢 تم جلب {len(available_free_models)} موديل مجاني شغال.")
    
    st.divider()
    
    # ❤️ إهداء خاص لدكتور يحيى
    st.markdown(
        """
        <div style="text-align: center; padding: 12px; background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.15);">
            <h3 style="color: #ff4b4b !important; margin: 0; font-size: 18px;"> شكراً دكتور احمد يحيى ❤️</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# 4️⃣ واجهة التطبيق الرئيسية
st.title("🌌 Space Knowledge Generative RAG System")
st.markdown("بحث واسترجاع من قاعدة البيانات + توليد إجابة ذكية باستخدام OpenRouter.")
st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input("أكتب سؤالك بالعربية أو الإنجليزية:", placeholder="مثال: كلمني عن كوكب المريخ")

with col2:
    top_k = st.slider("عدد المصادر المسترجعة (Top K):", min_value=1, max_value=5, value=3)

if st.button("🚀 البحث وتوليد الإجابة"):
    if not query:
        st.warning("يرجى إدخال سؤال أولاً!")
    elif not openrouter_api_key:
        st.error("لم يتم العثور على API Key في الـ Secrets!")
    else:
        with st.spinner("جاري البحث في قاعدة البيانات وتوليد الإجابة..."):
            try:
                pipeline_module = importlib.import_module("05_pipeline")
                generate_answer = pipeline_module.generate_answer
                
                result = generate_answer(query, db, openrouter_api_key, model_name=model_choice, top_k=top_k)
                
                st.success("✨ الإجابة:")
                st.write(result.get("answer", "لا توجد إجابة"))
                
                with st.expander("📚 المصادر المسترجعة من قاعدة البيانات"):
                    for idx, doc in enumerate(result.get("sources", []), 1):
                        st.markdown(f"**مصدر {idx}:**")
                        st.info(doc)
            except Exception as e:
                st.error(f"حدث خطأ أثناء التنفيذ: {e}")
