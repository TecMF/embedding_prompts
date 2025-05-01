import re
from typing import List, Tuple
from docling.document_converter import DocumentConverter

from BM25.modulos_bm25.processa_texto import ProcessaTexto
from BM25.modulos_bm25.processa_bm25 import ProcessaBM25


class PreparaTextoLLM:
    """
    Classe que prepara o texto do documento a ser analisado pelo LLM
    utilizando BM25.
    """

    def __init__(self):
        """
        Construtor da classe PreparaTextoLLM.
        """

        self.__regex_dict = {}

    def separarTextoArquivo(self, caminho: str, page_limit: int = None, lang: str = "english") -> List[str]:
        """
        Método que extrai o texto de um arquivo em pdf e separa em frases.

        Args:
            caminho (str): o caminho do arquivo a ser analisado
            page_limit (int): limite de páginas a serem analisadas para a conversão.
            lang (str): string com a linguagem a ser utilizada para tokenização.

        Returns:
            List[str]: uma lista com as frases (strings) do texto.
        """
        # Converte o PDF para texto
        converte_pdf = DocumentConverter()
        converted = converte_pdf.convert(caminho)

        doc_text = converted.document.export_to_text()

        self.__lista_frases = ProcessaTexto.separaFrases(doc_text, lang)
        return self.__lista_frases

    def regexFrases(
        self, field_name: str, frases: List[str] = None, n_vizinhos: int = 0
    ) -> List[str]:
        """
        Método que identifica quais frases do texto são realmente relevantes para a informação buscada em questão,
        com base em padrões de regex.

        Args:
            field_name (str): nome do campo a ter os regex verificados
            frases (List[str]): lista com as frases que compõem o texto do documento analisado.
            n_vizinhos (int): quantidade de frases próximas às que casarem com os padrões que devem ser
            levadas em consideração (para fins de contexto).

        Returns:
            List[str]: lista (possivelmente vazia) com frases que contenham texto relevante para avaliação.
        """

        if frases is None:
            frases = self.__lista_frases

        regex_patterns = self.__regex_dict.get(field_name)
        if regex_patterns is not None:
            # Identifica os índices com o padrão e os vizinhos
            filtered_indices = list()
            for i, frase in enumerate(frases):
                if (
                    re.search(
                        "|".join(regex_patterns), frase, flags=re.IGNORECASE | re.DOTALL
                    )
                    is not None
                ):
                    vizinho_min = max(i - n_vizinhos, 0)
                    vizinho_max = min(i + n_vizinhos, len(frases) - 1)
                    filtered_indices.extend(range(vizinho_min, vizinho_max + 1))

            # Remove índices repetidos e ordena
            filtered_indices = sorted(set(filtered_indices))

            # Retorna as frases
            return [frases[i] for i in filtered_indices]
        return list()

    def preparaFrasesBM25(self, frases_verificar: List[str]) -> None:
        """
        Método que cria uma instância da classe ProcessaBM25, preenchendo o atributo __processa_bm25

        Args:
            frases_verificar (List[str]): lista com as frases a serem passadas para o consturtor de ProcessaBM25.
        """
        self.__processa_bm25 = ProcessaBM25(frases_verificar)

    def bm25FrasesUniao(
        self,
        lista_frases: List[str],
        query: List[str],
        topn: int = 3,
        n_vizinhos: int = 1,
    ) -> str:
        """
        Realiza a query no BM25 e obtém os índices dos elementos do texto para fazer a união das
        substrings em um texto final.

        Args:
            lista_frases (List[str]): lista com as strings que compõem o texto na íntegra
            query (List[str]): lista com os contextos dos campos a serem avaliados
            topn (int): quantidade de índices a serem considerados
            n_vizinhos (int): quantidade de frases próximas às que casarem com os padrões que devem ser
            levadas em consideração (para fins de contexto).

        Returns:
            str: string com o texto final.
        """
        # Obtém os índices dos elementos do texto mais próximos à query
        indices_per_query: List[List[int]] = self.__processa_bm25.query_bm25_indices(
            query, topn=topn, n_vizinhos=n_vizinhos
        )

        # Prepara um conjunto para eliminar índices repetidos
        set_indices = {
            index for indices_list in indices_per_query for index in indices_list
        }

        # Ordena o conjunto em uma lista de índices
        lst_ordenada = sorted(set_indices)

        # Prepara o texto combinado das frases
        txt_final = ""
        for i in lst_ordenada:
            if i > 0:
                txt_final += " "
            txt_final += f"{lista_frases[i]}"

        return txt_final

    def bm25TopFrases(
        self,
        frases_verificar: List[str],
        query: List[str],
        topn_query: int | List[int] = 3,
        topn_frases: int = -1,
        n_vizinhos=0,
    ) -> str:
        """
        Realiza a query no BM25 e verifica os scores para determinar as top N frases em geral
        e retornar o texto combinado dessas frases.

        Args:
            frases_verificar (List[str]): lista de frases a serem checadas.
            query (List[str]): lista com as queries de BM25.
            topn_query (int | List[int]): quantidade de frases a serem consideradas - ou lista de quantidades,
            a depender da quantidade de queries envolvidas.
            topn_frases (int): quantidade máxima de frases a serem consideradas. Um hard limit, usado apenas
            em casos extremos. Por default, -1.
            n_vizinhos (int): quantidade de frases vizinhas (antes e depois) das frases selecionadas.

        Returns:
            str: string com o texto combinado das frases mais relevantes.
        """
        # Obtém os índices dos elementos do texto mais próximos à query
        indices_scores_per_query: List[Tuple[List[int], List[float]]] = (
            self.__processa_bm25.query_bm25_indices(
                query, topn=topn_query, n_vizinhos=n_vizinhos, get_scores=True
            )
        )

        # Prepara a lista de resultados e ordena pelos scores
        results_list = [
            (indices[i], scores[i])
            for indices, scores in indices_scores_per_query
            for i in range(len(indices))
        ]
        results_list.sort(key=lambda row: row[1], reverse=True)

        top_frases = dict()
        for result in results_list:
            index, score = result
            if top_frases.get(index) is None:
                top_frases[index] = score

            if len(top_frases) == topn_frases:
                break

        # Monta a lista de índices
        lst_indices = list(top_frases.keys())

        # Adiciona vizinhos às frases sem considerar o limite de top N
        if n_vizinhos > 0:
            lst_vizinhos = self.__processa_bm25.get_vizinhos(lst_indices, n_vizinhos)
            lst_indices.extend(lst_vizinhos)

        # Ordena a lista resultante das top frases com seus vizinhos
        lst_indices = sorted(lst_indices)
        lst_indices = [
            index
            for i, index in enumerate(lst_indices)
            if i + 1 == len(lst_indices) or index != lst_indices[i + 1]
        ]

        # Prepara o texto combinado das frases
        txt_final = ""
        for i, index in enumerate(lst_indices):
            if i > 0:
                last_index = lst_indices[i - 1]
                if (
                    frases_verificar[index][0].isdigit()
                    and not frases_verificar[last_index][-2].isdigit()
                ) or (
                    frases_verificar[last_index][-2].isdigit()
                    and not frases_verificar[index][0].isdigit()
                ):
                    txt_final += " "
            txt_final += frases_verificar[index]

        return txt_final
