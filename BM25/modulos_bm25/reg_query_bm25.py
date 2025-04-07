import re
from typing import Callable, Iterable, List, Tuple

import nltk
import numpy as np
import rank_bm25


class ProcessaBM25:
    """
    Classe que utiliza BM25 para processar texto.
    """

    def __init__(
        self,
        lista_frases_contexto: List[str],
        funcao_preprocessar: Callable[[str], str] = None,
    ) -> None:
        """
        Construtor da classe ProcessaBM25.

        Args:
            lista_frases_contexto (List[str]): lista contendo as frases que dão o contexto para o Bm25.
            funcao_preprocessar: (Callable[[str], str]): função que realiza o pré-processamento do texto. Caso nenhuma
            seja passada, a classe utiliza por padrão __preprocessar_texto.
        """

        self.__funcao_preprocessar = (
            self.__preprocessar_texto
            if funcao_preprocessar is None
            else funcao_preprocessar
        )
        self.__frases_contexto = lista_frases_contexto

        # Divide o documento em vetores de palavras por frase, após um pré-processamento do texto
        try:
            nltk.data.find("corpora/stopwords/english")
        except Exception:
            nltk.download("stopwords")

        self.__corpus_contexto = [
            [
                word
                for word in self.__funcao_preprocessar(document).split()
                if len(word) > 2
                and word not in set(nltk.corpus.stopwords.words("english"))
            ]
            for document in lista_frases_contexto
        ]

    def __adicionar_n_vizinhos(self, lista_indices: List[int], n: int = 0) -> List[int]:
        """
        Adiciona, para cada resultado do BM25, os seus n vizinhos. Supondo um texto dividido por
        frases, se o BM25 selecionou a frase de índice 14, com esta função com n=1, seria retornado o texto com
        as frases índice 12, 13 e 14. Pressupõe que o conjunto de textos enviado está ordenado.

        Args:
            lista_indices (List[int]): lista com os índices do resultado do BM25.
            n (int): quantidade de vizinhos a serem considerados ao redor dos índices em lista_indices.

        Returns:
            List[int]: lista com os índices de lista_indices, além dos índices vizinhos.
        """
        if n == 0:
            return lista_indices

        lista_indices_res = []
        for i in lista_indices:
            lista_indices_res.extend(range(max(0, i - n), i + n + 1))

        # Removendo os duplicados preservando a ordem
        lista_indices_res = sorted(set(lista_indices_res))

        return lista_indices_res

    def __adicionar_n_vizinhos_de_lista(
        self, top_n: List[int], n_vizinhos: int, len_lista_original: int
    ) -> List[int]:
        """
        Adiciona os vizinhos de acordo com n_vizinhos, mas exclui os que saem dos índices da lista original.

        Args:
            top_n (List[int]): lista com os índices originais.
            n_vizinhos (int): quantidade de vizinhos a serem levados em consideração.
            len_lista_original (int): tamanho da lista original.

        Returns:
            List[int]: lista dos índices atualizada com os vizinhos.
        """
        lista_indices_estendido = self.__adicionar_n_vizinhos(top_n, n_vizinhos)

        # except IndexError: ## se lista de indices estendida está fora dos limites da lista original, eu a faço 'caber'
        n_max = len_lista_original - 1
        lista_reduzida = [i for i in lista_indices_estendido if 0 <= i and i <= n_max]
        # top_docs_ext = [lista_sintetica[i] for i in lista_reduzida]

        return lista_reduzida

    def __retornar_porcentagens(self, match: re.Match[str]) -> str:
        """
        Identifica uma porcentagem numa string, retornando uma categoria percentual.

        Categorias:
            0: __nporcentzero__
            0 < valor < 20: __nporcentbaixa__
            20 <= valor < 50: __nporcentmedia__
            50 <= valor < 95: __nporcent95__
            95 <= valor: __nporcentalta__

        Args:
            match (re.Match[str]): casamento de regex do padrão de porcentagem

        Returns:
            str: string com a categoria em que esse percentual se encontra.
        """

        if match is not None:
            match = match.group().replace(" ", "").replace(",", ".").replace("%", "")
            match = float(match)
            if match == 0.0:
                return " __nporcentzero__ "
            elif match <= 20.0:
                return " __nporcentbaixa__ "
            elif match <= 50.0:
                return " __nporcentmedia__ "
            elif match == 95.0:
                return " __nporcent95__ "
            else:
                return " __nporcentalta__ "

    # TODO reavaliar essa função aqui
    def __preprocessar_texto(self, f: str) -> str:
        """
        Função de pré-processamento. Ideia é generalizar conceitos que tornem mais fácil a busca.
        Seu linter pode dar flag de que a função não está sendo acessada, mas vale lembrar que ela é o valor
        default da função de pré-processamento do construtor da classe.

        Args:
            f (str): string com o texto a ser processado.

        Returns:
            str: a string após ser processada.
        """
        flags = re.IGNORECASE | re.DOTALL
        meses = (
            "janeiro",
            "fevereiro",
            "março",
            "abril",
            "maio",
            "junho",
            "julho",
            "agosto",
            "setembro",
            "outubro",
            "novembro",
            "dezembro",
        )
        f = f.lower().replace("\n", "")

        # Trocando meses por chave geral
        for mes in meses:
            f = re.sub(mes, " __mes__ ", f, flags=flags)

        # Removendo numeração de capitulos, artigos, paragrafros etc
        f = re.sub(r"artigo \d+", " ", f, flags=flags)
        f = re.sub(r"par.gr.fo \d+", " ", f, flags=flags)

        # Substituindo instancias de CNPJ por chave geral
        f = re.sub(r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}", " __CNPJ__ ", f, flags=flags)
        # f = re.sub('\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}', retornar_cnpjs, f)

        # Substituindo instancias de porcentagem
        f = re.sub(r"\d+[,\.]?\d* ?%", self.__retornar_porcentagens, f, flags=flags)
        # f = re.sub('\d+[,\.]?\d* ?%',' __NPORCENT__ ',f)

        # Subst data
        f = re.sub(r"\d{1,2}\/\d{1,2}\/\d{1,4}", " __DATA__ ", f, flags=flags)
        f = re.sub(r"\d{2}\.\d{2}\.\d{4}", " __DATA__ ", f, flags=flags)

        # Subst numeros finaceiros R$ 1000 etc
        f = re.sub(r"r\$ \d+[\d+\.\,]{0,15}", " __numfin__ ", f, flags=flags)

        # Substituindo D+1 para __ddig__
        f = re.sub(r"d\+\d+", " __ddig__ ", f, flags=flags)

        # Substituindo ceps
        f = re.sub(r"\d{5}-\d{3}", " __ncep__ ", f, flags=flags)

        # Substituindo número de telefones
        f = re.sub(
            r"(?:\(\d{1,3}\))?.?\d{4,5}-?\d{4}", " __ntelefone__ ", f, flags=flags
        )

        # Subst websites, urls
        f = re.sub(r"[^\s]*www[^\s]+", " __website__ ", f, flags=flags)

        # Subst e-mails
        f = re.sub(r"[^\s]+@[^\s]+\.com[^\s]*", " __email__ ", f, flags=flags)

        # f = re.sub('www\.[a-z0-9]+\.com(?:.br)?','__website__',f)

        # Tira pontos tipo 4.444 para 4444
        f = re.sub(r"([^\s])\.([^\s])", r"\1\2", f, flags=flags)

        # f = re.sub('\d+',' __NUMEROGERAL__ ',f)

        # Removendo pontuação
        # f = re.sub(r'\W', ' ',f)
        # f = re.sub(r'[\(\).,:;-]',' ',f)
        f = re.sub(r"[^a-zA-Z0-9_À-ÿ]", " ", f, flags=flags)

        # Removendo letras de len = 1
        # f = re.sub(r'(?:^|\s+)[a-zA-ZÀ-ÿ]\s+',' ',f)

        # Removendo espacos duplos
        f = re.sub(r"\s+", " ", f, flags=flags)

        f = f.strip()

        if f != "":
            return f
        else:
            return "__vazio__"

    def __query_bm25_basica(
        self,
        lstquery: Iterable[str],
        topn: int | Iterable[int] = 3,
        retirar_relevancia_zero: bool = False,
        get_scores: bool = False,
    ) -> List[Tuple[np.ndarray, np.ndarray] | np.ndarray]:
        """
        Gera os índices das palavras com maior semelhança à query por frase pelo BM25. Método auxiliar,
        é chamado por query_bm25_indices, que efetivamente leva os vizinhos em consideração.

        Args:
            lstquery (Iterable[str]): lista com as frases a serem analisadas
            top_n (int | Iterable[int]): quantidade de índices a serem considerados. Default: 3
            retirar_relevancia_zero (bool): indica se deve retirar da análise dados com pontuação 0. Default: False
            get_scores (bool): indica se deve obter os scores do BM25 para análise. Default: False

        Returns:
            List[Tuple[np.ndarray, np.ndarray] | np.ndarray]: lista com os índices das palavras relevantes ao
            contexto dado (e suas pontuações, caso get_scores seja True).
        """

        # Inicializa o BM25 com o corpus do documento
        bm25 = rank_bm25.BM25Okapi(self.__corpus_contexto)

        # Divide as queries em vetores de palavras por query, após o pré-processamento do texto das queries
        querypreproc = [self.__funcao_preprocessar(q).split() for q in lstquery]

        lst_indices = []

        # Determina as top N a serem procuradas
        if isinstance(topn, (int, float)):
            topn = [topn] * len(querypreproc)

        # Procura os índices das frases mais parecidas a partir do score do BM25
        for num_results, query in zip(topn, querypreproc):
            # Faz a consulta ao BM25
            scores = bm25.get_scores(query)

            if retirar_relevancia_zero is True:
                mask = scores != 0.0
                filtered_scores = scores[mask]

                # Ordena os resultados pelo score filtrado
                top_nonzero_results = np.argsort(filtered_scores)[::-1][:num_results]

                # Obtendo os índices originais da máscara
                original_indices = np.nonzero(mask)[0]

                # Indexando o resultado com os índices originais
                top_results = original_indices[top_nonzero_results]
                top_scores = scores[top_results]
            else:
                # Ordena os resultados pelo score
                top_results = np.argsort(scores)[::-1][:num_results]
                top_scores = scores[top_results]

            if get_scores is True:
                lst_indices.append((top_results, top_scores))
            else:
                lst_indices.append(top_results)

        return lst_indices

    def getListaFrases(self) -> List[str]:
        """
        Returns:
            List[str]: a lista com as frases que compõem o contexto.
        """
        return self.__frases_contexto

    def query_bm25_indices(
        self,
        lstquery: Iterable[str],
        topn: int | Iterable[int] = 3,
        n_vizinhos: int = 0,
        retirar_relevancia_zero: bool = False,
        get_scores: bool = False,
    ) -> List[Tuple[List[int], List[float]] | List[int]]:
        """
        Processa as frases recebidas por parâmetro para obter os índices das relevantes e, se pedido, os scores
        de acordo com o BM25. Também considera os vizinhos.

        Args:
            lstquery (Iterable[str]): lista com as frases a serem analisadas
            top_n (int | Iterable[int]): quantidade de índices a serem considerados. Pode conter múltiplas quantidades,
            a depender do campo. Default: 3
            n_vizinhos (int): quantidade de vizinhos dos índices a serem levados em consideração. Default: 0
            retirar_relevancia_zero (bool): indica se deve retirar da análise dados com pontuação 0. Default: False
            get_scores (bool): indica se deve obter os scores do BM25 para análise. Default: False

        Returns:
            List[Tuple[List[int], List[float]] | List[int]]: lista com os índices das palavras relevantes ao
            contexto dado (e suas pontuações, caso get_scores seja True).
        """

        # Identifica os índices das palavras com maior semelhança à query por frase pelo BM25
        lista_top_n = self.__query_bm25_basica(
            lstquery=lstquery,
            topn=topn,
            retirar_relevancia_zero=retirar_relevancia_zero,
            get_scores=get_scores,
        )

        # Inicializa a lista de índices e adiciona os índices e seus N vizinhos
        lst_indices = []
        for top_n in lista_top_n:
            if n_vizinhos > 0 and get_scores is False:
                lista_indices_ext = self.__adicionar_n_vizinhos_de_lista(
                    top_n=top_n,
                    n_vizinhos=n_vizinhos,
                    len_lista_original=len(self.__frases_contexto),
                )
                lst_indices.append(lista_indices_ext)
            elif get_scores is True:
                lst_indices.append((list(top_n[0]), list(top_n[1])))
            else:
                lst_indices.append(list(top_n))

        return lst_indices

    def get_vizinhos(self, lst_indices: List[int], n_vizinhos: int) -> List[int]:
        """
        Obtém os vizinhos dos índices recebidos por parâmetro. Encapsula __adicionar_n_vizinhos_de_lista.

        Args:
            lst_indices (List[int]): lista com os índices originais.
            n_vizinhos (int): quantidade de vizinhos a serem levados em consideração.

        Returns:
            List[int]: lista dos índices atualizada com os vizinhos.
        """
        return self.__adicionar_n_vizinhos_de_lista(
            top_n=lst_indices,
            n_vizinhos=n_vizinhos,
            len_lista_original=len(self.__frases_contexto),
        )
