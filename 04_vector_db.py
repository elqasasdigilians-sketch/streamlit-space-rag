import chromadb
from sentence_transformers import SentenceTransformer

# تحميل نموذج تحويل النصوص إلى متجهات (نموذج خفيف وسريع وممتاز)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_vector_db(db_path="chroma_db", collection_name="space_docs"):
    """
    إنشاء أو فتح قاعدة بيانات ChromaDB حقيقية يتم حفظها على القرص الصلب.
    """
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name=collection_name)
    return collection

def add_chunks_to_db(collection, chunks):
    """
    تحويل قطع النصوص إلى Embeddings وتخزينها داخل ChromaDB.
    """
    if not chunks:
        print("⚠️ لا توجد قطعات (Chunks) للإضافة!")
        return

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["content"] for chunk in chunks]
    metadatas = [{"source": chunk["source"]} for chunk in chunks]

    # تحويل النصوص إلى أرقام ومتجهات
    embeddings = embedding_model.encode(documents).tolist()

    # حفظ المتجهات والنصوص في قاعدة البيانات
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )
    print(f"✅ تم حفظ {len(chunks)} قطعة بنجاح داخل قاعدة البيانات الاتجاهية!")

def search_db(collection, query_text: str, top_k: int = 1):
    """
    البحث في قاعدة البيانات عن أكثر القطع تشابهاً مع سؤال المستخدم.
    """
    query_embedding = embedding_model.encode([query_text]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    return results

# تجربة حية ومستقلة للملف
if __name__ == "__main__":
    sample_chunks = [
        {"id": "test_c0", "source": "artemis.txt", "content": "NASA's Artemis program aims to land humans on the Moon again."},
        {"id": "test_c1", "source": "jwst.txt", "content": "The James Webb Space Telescope observes distant galaxies in infrared."}
    ]

    # 1. فتح قاعدة البيانات وتخزين البيانات
    db = get_vector_db()
    add_chunks_to_db(db, sample_chunks)

    # 2. اختبار البحث بالسؤال
    query = "What is the goal of Artemis?"
    search_results = search_db(db, query, top_k=1)

    print("\n🔍 السؤال التجريبي:", query)
    print("📄 النص المسترجع من قاعدة البيانات:", search_results['documents'][0][0])