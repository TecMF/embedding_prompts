from pathlib import Path

from BM25.modulos_bm25.texto_para_llm import PreparaTextoLLM
from BM25.modulos_bm25.processa_texto import ProcessaTexto
from BM25.queries import Queries

if __name__ == "__main__":

    # Passando os pdfs para txt para facilitar o BM25 posteriormente
    """
    pdfs_ptbr = Path(r"BM25/exemplos/portuguese").glob("*.pdf")

    for pdf in pdfs_ptbr:
        doc_text = ""
        doc = pymupdf.Document(pdf)
        for page in doc:
            doc_text += page.get_text()
        with open(Path(r"BM25/exemplos/portuguese/as_text") / (Path(pdf).name + ".txt"), "w", encoding="utf-8") as file:
            file.write(doc_text)

    pdfs_en = Path(r"BM25/exemplos/english").glob("*.pdf")

    for pdf in pdfs_en:
        doc_text = ""
        doc = pymupdf.Document(pdf)
        for page in doc:
            doc_text += page.get_text()
        with open(Path(r"BM25/exemplos/english/as_text") / (Path(pdf).name + ".txt"), "w", encoding="utf-8") as file:
            file.write(doc_text)
    """

    queries = Queries()

    for key, value in queries.getAllInformation().items():
        id = key
        queries_pt = value["queries_pt"]
        queries_en = value["queries_en"]
        top_n = value["top_n"]
        vizinhos = value["vizinhos"]
        for path in Path(r"BM25/exemplos/english/as_text").glob("*.txt"):
            with open(path, "r", encoding="utf-8") as input:
                print("Lendo " + path.name + " para o termo " + id + " (em inglês)...")
                doc_text = input.read()
                lista_frases = ProcessaTexto.separaFrases(doc_text, "english")
                prepara_texto = PreparaTextoLLM()
                prepara_texto.preparaFrasesBM25(lista_frases)
                saidaBM25 = prepara_texto.bm25FrasesUniao(lista_frases, queries_en, top_n, vizinhos)
                with open(Path("BM25/output/english") / id / (path.name + ".txt"), "w", encoding='utf-8') as output:
                    output.write(saidaBM25)
                    output.close()
                input.close()
        
        for path in Path(r"BM25/exemplos/portuguese/as_text").glob("*.txt"):
            with open(path, "r", encoding="utf-8") as file:
                print("Lendo " + path.name + " para o termo " + id + " (em português)...")
                doc_text = file.read()
                lista_frases = ProcessaTexto.separaFrases(doc_text, "portuguese")
                prepara_texto = PreparaTextoLLM()
                prepara_texto.preparaFrasesBM25(lista_frases)
                saidaBM25 = prepara_texto.bm25FrasesUniao(lista_frases, queries_en, top_n, vizinhos)
                with open(Path("BM25/output/portuguese") / id / (path.name + ".txt"), "w", encoding='utf-8') as output:
                    output.write(saidaBM25)
                    output.close()
                input.close()

    """
    # Obtendo o texto como lista de strings
    # Conversão de pdf via PyMuPdf
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
    """
