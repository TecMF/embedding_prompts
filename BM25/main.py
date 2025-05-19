from pathlib import Path

from BM25.modulos_bm25.texto_para_llm import PreparaTextoLLM

if __name__ == "__main__":

    # Obtendo o texto como lista de strings
    # Conversão de pdf via Docling
    input_pdf = Path(r"BM25/exemplos") / r"NBRISO-IEC 27035.pdf"
    prepara_texto = PreparaTextoLLM()
    lista_frases = prepara_texto.separarTextoArquivo(input_pdf, lang="english")

    prepara_texto.preparaFrasesBM25(lista_frases)

    # Lista de queries para o BM25
    lista_queries1 = ["vulnerability",
                     "vulnerabilities",
                     "vulnerable",
                     "services",
                     "server",
                     "systems",
                     "networks"]
    # Top n - a quantidade de índices a serem considerados
    top_n = 15
    # Vizinhos - quantidade de frases "vizinhas" aos índices encontrados que serão consideradas
    # Importante para contexto
    vizinhos = 1

    # Todas as frases relevantes
    contexto = prepara_texto.bm25FrasesUniao(lista_frases, lista_queries1, top_n, vizinhos)
    # Apenas as de melhor score
    contexto1 = prepara_texto.bm25TopFrases(lista_frases, lista_queries1, top_n, -1, vizinhos)

    with open(Path("BM25/output") / "pre_prompt1.txt", "w", encoding='utf-8') as file:
        file.write(contexto1)
        file.close()

    # Lista de queries para o BM25
    lista_queries2 = ["incident",
                     "response",
                     "assessment",
                     "confirmation",
                     "action",
                     "responses",
                     "actions",
                     "activities",
                     "management"]

    contexto2 = prepara_texto.bm25TopFrases(lista_frases, lista_queries2, top_n, -1, vizinhos)

    with open(Path("BM25/output") / "pre_prompt2.txt", "w", encoding='utf-8') as file:
        file.write(contexto2)
        file.close()
