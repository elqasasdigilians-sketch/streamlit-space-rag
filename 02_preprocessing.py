import re

def clean_text(text: str) -> str:
    """
    دالة تنظيف نصية بـ Vanilla Python لتنظيف المسافات والأسطر والرموز الزائدة.
    """
    # 1. استبدال المسافات والأسطر المتكررة بمسافة واحدة فقط
    text = re.sub(r'\s+', ' ', text)
    
    # 2. إزالة أي رموز غريبة غير قابلة للطباعة (Non-printable characters)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # 3. قص المسافات من أول وأخر النص
    return text.strip()

def preprocess_documents(documents: list) -> list:
    """
    دالة تأخذ قائمة المستندات من 01_documents.py وتطبق عليها التنظيف.
    """
    cleaned_docs = []
    for doc in documents:
        cleaned_docs.append({
            "source": doc["source"],
            "content": clean_text(doc["content"])
        })
    return cleaned_docs

# اختبار الملف منفصلاً
if __name__ == "__main__":
    sample_text = "   NASA's   Artemis program \n\n aims to land humans on the Moon!   "
    print("--- قبل التنظيف ---")
    print(repr(sample_text))
    
    cleaned = clean_text(sample_text)
    print("\n--- بعد التنظيف ---")
    print(repr(cleaned))