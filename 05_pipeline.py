import importlib

# استيراد الوظائف من الملفات الـ 4 السابقة
doc_module = importlib.import_module("01_documents")
prep_module = importlib.import_module("02_preprocessing")
chunk_module = importlib.import_module("03_chunking")
vdb_module = importlib.import_module("04_vector_db")

load_documents = doc_module.load_documents
preprocess_documents = prep_module.preprocess_documents
create_chunks = chunk_module.create_chunks
get_vector_db = vdb_module.get_vector_db
add_chunks_to_db = vdb_module.add_chunks_to_db
search_db = vdb_module.search_db

def run_rag_indexing_pipeline(data_dir="data"):
    """
    تشغيل خط الإنتاج الكامل: القراءة -> التنظيف -> التقطيع -> التخزين في ChromaDB.
    """
    print("🚀 بدء تشغيل الـ RAG Pipeline...\n")
    
    # 1. قراءة المستندات
    raw_docs = load_documents(data_dir)
    print(f"1️⃣ تم قراءة {len(raw_docs)} مستند(ات) من مجلد '{data_dir}'.")
    
    if not raw_docs:
        print("⚠️ مجلد البيانات فاضي حالياً. سيعمل النظام عند إضافة ملفات فيه للاحقاً.")
        return None

    # 2. تنظيف النصوص
    cleaned_docs = preprocess_documents(raw_docs)
    print("2️⃣ تم تنظيف النصوص بنجاح.")

    # 3. تقطيع النصوص
    chunks = create_chunks(cleaned_docs, chunk_size=50, overlap=10)
    print(f"3️⃣ تم تقطيع النصوص إلى {len(chunks)} قطعة (Chunks).")

    # 4. التخزين في قاعدة البيانات الاتجاهية
    db = get_vector_db()
    add_chunks_to_db(db, chunks)
    print("\n✅ اكتملت عملية الفهرسة والتخزين بنجاح!")
    
    return db

# اختبار خط الإنتاج
if __name__ == "__main__":
    # تشغيل خط الإنتاج بالكامل
    db = run_rag_indexing_pipeline()
    
    # تجربة سؤال في حالة وجود قاعدة بيانات
    if db:
        user_query = "Tell me about space exploration"
        print(f"\n🔍 جاري البحث عن: '{user_query}'...")
        results = search_db(db, user_query, top_k=2)
        
        print("\n📄 القطع الأكثر صلة التي تم العثور عليها:")
        for idx, doc_text in enumerate(results['documents'][0]):
            print(f"   [{idx+1}] {doc_text}")