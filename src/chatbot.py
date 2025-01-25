def chatbot_response(user_input, model, index):
    """
    Kullanıcıdan gelen girdiye göre chatbot yanıtı üretir.
    """
    from sentence_transformers import util

    # Kullanıcı girdisini embedding'e çevir
    user_embedding = model.encode(user_input)

    # Pinecone'da benzerlik araması yap
    query_results = index.query(
        vector=user_embedding.tolist(),
        top_k=1,
        include_metadata=True
    )

    # En iyi sonucu al
    if query_results["matches"]:
        top_result = query_results["matches"][0]
        return top_result["metadata"]["answer"]
    else:
        return "Üzgünüm, sorunuza uygun bir yanıt bulamadım."
