def create_chunks(cleaned_docs: list, chunk_size: int = 6, overlap: int = 2) -> list:
    """
    تقطيع النصوص إلى أجزاء (Chunks) بـ Vanilla Python مع وجود تداخل (Overlap) لحفظ السياق.
    """
    chunks = []
    
    for doc in cleaned_docs:
        source = doc["source"]
        words = doc["content"].split()
        
        if not words:
            continue
            
        step = chunk_size - overlap
        chunk_id = 0
        
        for i in range(0, len(words), step):
            chunk_words = words[i : i + chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append({
                "id": f"{source}_chunk_{chunk_id}",
                "source": source,
                "content": chunk_text
            })
            chunk_id += 1
            
            if i + chunk_size >= len(words):
                break
                
    return chunks

# تجربة التقطيع بنص وهمي
if __name__ == "__main__":
    sample_docs = [{
        "source": "artemis.txt",
        "content": "The Artemis program is an ongoing human spaceflight program carried out by NASA to land humans on the Moon again. It utilizes the Space Launch System rocket and Orion spacecraft."
    }]
    
    chunked = create_chunks(sample_docs, chunk_size=10, overlap=3)
    print(f"✅ تم تقطيع النص إلى {len(chunked)} Chunks بنجاح:\n")
    
    for chunk in chunked:
        print(f"🔹 ID: {chunk['id']}")
        print(f"📄 Source: {chunk['source']}")
        print(f"📝 Content: {chunk['content']}\n")