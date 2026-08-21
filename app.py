import streamlit as st
import importlib
import urllib.request
import json
import os
import base64

# 1️⃣ ضبط إعدادات الصفحة والتجاوب التلقائي مع الموبايل واللابتوب
st.set_page_config(
    page_title="Space Knowledge RAG System",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="auto"  # فتح/غلق القائمة الجانبية أوتوماتيكياً حسب نوع الجهاز
)

# 2️⃣ دالة لجلب الصورة الشخصية وتحويلها إلى Base64 لضمان ظهورها دائرية
def get_avatar_src():
    for filename in ["my_photo.png", "my_photo.png.png", "my_photo.jpg", "my_photo.jpeg"]:
        if os.path.exists(filename):
            try:
                with open(filename, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                return f"data:image/png;base64,{encoded}"
            except Exception:
                pass
    return "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

avatar_src = get_avatar_src()

# 3️⃣ تصميم CSS متكامل يشمل الـ Media Queries لشاشات الموبايل والتابلت واللابتوب
space_css = """
<style>
/* خلفية الفضاء مدمجة بطبقة داكنة ناعمة لتقليل التشتيت */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(10, 14, 26, 0.85), rgba(10, 14, 26, 0.90)), 
                url("https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* الشريط الجانبي بزجاج داكن راقي */
[data-testid="stSidebar"] {
    background-color: rgba(13, 18, 32, 0.94) !important;
    backdrop-filter: blur(12px);
    border-left: 1px solid rgba(255, 255, 255, 0.1);
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0) !important;
}

/* توضيح نصوص العناوين والفقرات */
h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown {
    color: #FFFFFF !important;
}

/* 🎯 تحسين مربع الإدخال (Input Box) */
.stTextInput input {
    background-color: rgba(22, 30, 48, 0.95) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    border: 2px solid rgba(255, 255, 255, 0.25) !important;
    font-size: 16px !important;
    padding: 12px !important;
    transition: all 0.3s ease-in-out !important;
    direction: auto !important;
}

/* عند مرور الماوس (Hover) أو الضغط عليه (Focus) */
.stTextInput input:hover, .stTextInput input:focus {
    border: 2px solid #ff4b4b !important;
    box-shadow: 0 0 18px rgba(255, 75, 75, 0.85) !important;
    font-weight: 900 !important;
    background-color: rgba(30, 40, 65, 1) !important;
    transform: translateY(-2px);
}

/* القائمة المنسدلة */
.stSelectbox > div > div {
    background-color: rgba(22, 30, 48, 0.95) !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* زر البحث والتوليد */
.stButton > button {
    background: linear-gradient(90deg, #ff4b4b 0%, #ff7b54 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    font-size: 16px !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease-in-out !important;
    box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
}

.stButton > button:hover {
    box-shadow: 0 0 20px rgba(255, 75, 75, 0.8) !important;
    transform: scale(1.02) !important;
}

/* 🎯 تصميم الصورة الشخصية الدائرية واسم المستخدم */
#user-profile-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 15px;
    padding-top: 10px;
}
#user-profile-container img {
    border-radius: 50%;
    width: 110px;
    height: 110px;
    object-fit: cover;
    border: 3px solid #ff4b4b;
    box-shadow: 0 0 20px rgba(255, 75, 75, 0.5);
    margin-bottom: 12px;
}
#user-profile-container h3 {
    text-align: center;
    font-weight: 900 !important;
    font-size: 21px !important;
    color: #FFFFFF !important;
    margin: 0;
    letter-spacing: 0.5px;
}

/* 🎯 صندوق عرض الإجابة مع اتجاه تلقائي (يمين للعربي / شمال للإنجليزي) */
.answer-box {
    background-color: rgba(22, 30, 48, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 18px;
    margin-top: 10px;
    color: #FFFFFF;
    font-size: 17px;
    line-height: 1.7;
    dir: auto;
    text-align: start;
    unicode-bidi: plaintext;
}

/* 📱💻📱 ========================================================= */
/* 🎯 MEDIA QUERIES (التجاوب الذكي مع مختلف مقاسات الشاشات) */
/* ================================================================ */

/* شاشات الأجهزة المتوسطة والتابلت (أقل من 992px) */
@media screen and (max-width: 992px) {
    .answer-box {
        font-size: 16px !important;
        padding: 16px !important;
    }
    #user-profile-container img {
        width: 95px !important;
        height: 95px !important;
    }
}

/* شاشات الموبايل الذكية (أقل من 768px) */
@media screen and (max-width: 768px) {
    /* إلغاء الـ fixed background لمنع بطء الحركة والتشتيت في الموبايل */
    [data-testid="stAppViewContainer"] {
        background-attachment: scroll !important;
    }
    
    /* تكبير وتوسيع زر التوليد ليشمل العرض بالكامل لسهولة الضغط بالأصبع */
    .stButton > button {
        width: 100% !important;
        font-size: 15px !important;
        padding: 14px !important;
    }

    /* تعديل أحجام النصوص والمربعات لتناسب شاشة الهاتف */
    .stTextInput input {
        font-size: 14px !important;
        padding: 10px !important;
    }
    
    .answer-box {
        font-size: 15px !important;
        padding: 14px !important;
    }

    #user-profile-container img {
        width: 85px !important;
        height: 85px !important;
    }

    #user-profile-container h3 {
        font-size: 18px !important;
    }
}

/* شاشات الموبايل الصغيرة جداً (أقل من 480px) */
@media screen and (max-width: 480px) {
    h1 {
        font-size: 22px !important;
    }
    .answer-box {
        font-size: 14px !important;
        line-height: 1.6 !important;
    }
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

# استيراد قاعدة البيانات
vdb_module = importlib.import_module("04_vector_db")
get_vector_db = vdb_module.get_vector_db
search_db = vdb_module.search_db

@st.cache_resource
def load_db():
    return get_vector_db()

db = load_db()

available_free_models = fetch_live_free_models()

# جلب الـ API Key في الخفاء من Secrets
openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY", "")

# 4️⃣ القائمة الجانبية (Sidebar)
with st.sidebar:
    # عرض الصورة الدائرية واسمك
    st.markdown(
        f"""
        <div id="user-profile-container">
            <img src="{avatar_src}" alt="Abdelrhman Khaled" />
            <h3>👨‍💻 Abdelrhman Khaled</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # اختيار الموديل
    st.markdown("**🤖 اختر نموذج الذكاء الاصطناعي:**")
    model_choice = st.selectbox(
        "اختر النموذج:",
        options=available_free_models,
        label_visibility="collapsed"
    )
    
    st.caption(f"🟢 تم جلب {len(available_free_models)} موديل مجاني شغال.")
    
    st.divider()
    
    # ❤️ إهداء خاص لدكتور أحمد يحيى
    st.markdown(
        """
        <div style="text-align: center; padding: 12px; background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.15);">
            <h3 style="color: #ff4b4b !important; margin: 0; font-size: 20px;">Eng - Abdelrhman Khaled ❤️</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# 5️⃣ واجهة التطبيق الرئيسية
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
                answer_text = result.get("answer", "لا توجد إجابة")
                
                st.success("✨ الإجابة:")
                
                # عرض الإجابة بداخل حاوية ذكية تضبط الاتجاه أوتوماتيكياً (يمين للعربي / شمال للإنجليزي)
                st.markdown(
                    f"""
                    <div class="answer-box" dir="auto">
                        {answer_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                with st.expander("📚 المصادر المسترجعة من قاعدة البيانات"):
                    for idx, doc in enumerate(result.get("sources", []), 1):
                        st.markdown(f"**مصدر {idx}:**")
                        st.info(doc)
            except Exception as e:
                st.error(f"حدث خطأ أثناء التنفيذ: {e}")
