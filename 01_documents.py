import os

def load_documents(data_dir="data"):
    """
    دالة لقراءة كافة الملفات النصية من مجلد البيانات،
    وترجع قائمة تحتوي على محتوى كل ملف واسمه.
    """
    documents = []
    
    # 1. التأكد من وجود مجلد البيانات
    if not os.path.exists(data_dir):
        print(f"⚠️ تنبيه: المجلد '{data_dir}' غير موجود!")
        return documents

    # 2. المرور على جميع الملفات داخل مجلد data
    for filename in os.listdir(data_dir):
        # قراءة الملفات النصية فقط (.txt أو .md)
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(data_dir, filename)
            
            # قراءة محتوى الملف مع دعم ترميز utf-8
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
                # إضافة المعجم الخاص بالمستند
                documents.append({
                    "source": filename,
                    "content": content
                })
                
    return documents

# الجزء الخاص باختبار الكود
if __name__ == "__main__":
    docs = load_documents()
    print(f"✅ تم تحميل {len(docs)} مستند(ات) بنجاح.")
    for doc in docs:
        print(f"📄 اسم الملف: {doc['source']}")