import re
from typing import List, Tuple

import nltk


class ProcessaTexto:
    """
    Classe com métodos para separar um texto em uma lista com frases tratadas para BM25.
    """

    @classmethod
    def __procurar_separador(
        cls, texto: str, separador: str, meio: int = 0
    ) -> List[str] | bool:
        """
        Encontra separadores para conseguir quebrar uma frase grande em menores. O candidato a divisor deve estar
        entre 25% e 75% do comprimento da frase.

        Args:
            texto (str): frase a ser analisada.
            separador (str): separados a ser buscado no texto (geralmente um caracter apenas).
            meio (int): índice indicando o meio da busca no texto (default: 0).

        Returns:
            List[str] | bool: lista com a frase dividida em duas partes, em torno do divisor encontrado.
            Caso o divisor esteja muito próximo das extremidades do texto (i.e. antes de 25% ou depois de 75%),
            retorna False.

        """
        tamanho = len(texto)
        inicio = texto[:meio]
        fim = texto[meio:]

        search = re.search(rf"{separador}", fim)
        if search is not None:
            ipartefinal = search.span()[0] + 1 + meio
        else:
            ipartefinal = len(fim) + meio

        listafind = [e for e in re.finditer(separador, inicio)]
        if len(listafind) > 0:
            iparteinicial = listafind[-1].start() + 1
        else:
            iparteinicial = 0

        if iparteinicial == 0 and ipartefinal == tamanho:
            return False
        else:
            d1 = meio - iparteinicial
            d2 = ipartefinal

            if d1 < d2:
                divisor = iparteinicial
                porcentagem = (tamanho - divisor) / tamanho
            else:
                divisor = ipartefinal + meio
                porcentagem = (tamanho - divisor) / tamanho

        if porcentagem > 0.25 and porcentagem < 0.75:
            return [texto[:divisor], texto[divisor:]]
        else:
            return False

    @classmethod
    def __divide_frases_grandes(
        cls,
        lista_frases: List[str],
        nmax: int = 700,
        l_separadores: Tuple[str] = (
            r"\.",
            r";",
            r"(?:\s|^|\()\d{1,2}\)",
            r"(?:\s|^|\()[a-z]{1,2}\)",
            r",",
            r" ",
        ),
    ) -> List[str]:
        """
        Recursivamente quebra frases grandes, que tenham length maior que nmax.
        Tenta quebrar na ordem dos separadores (tem que seguir o padrão regex),
        iniciando pelo meio, até todas as frases estarem menores que nmax. Na hora
        de quebrar a frase, além da ordem dos separadores, também é considerado que
        uma boa divisão não deixa uma proporção mais extrema que 25% - 75%.

        Args:
            lista_frases (List[str]): lista com as frases a serem analisadas.
            nmax (int): tamanho máximo de uma frase (em caracteres).
            l_separadores (Tuple[str]): tupla com as possibilidades de padrões regex para os separadores.
            Por default, os separadores mais comuns são utilizados.

        Returns:
            List[str]: lista com as frases, após as frases grandes terem sido quebradas em componentes menores.
        """

        lst_res = []

        for frase in lista_frases:
            tam = len(frase)
            if tam < nmax:
                lst_res.append(frase)
                continue  # se a frase for menor que nmax ela é somente adicionada a lista final

            # se não tento dividir adicionalmente
            i_meio = tam // 2

            sucesso = False
            for sep in l_separadores:
                listadivisao = cls.__procurar_separador(frase, sep, meio=i_meio)
                if listadivisao:
                    listafrasesquebradas = cls.__divide_frases_grandes(listadivisao)
                    sucesso = True
                    break
            if sucesso:
                lst_res.extend(listafrasesquebradas)
            else:
                lst_res.append(frase)

        return lst_res

    @classmethod
    def separaFrases(cls, texto: str, lang: str) -> List[str]:
        """
        Quebra o texto em uma lista de frases. Frases grandes (mais de 900 caracteres) são quebradas.

        Args:
            texto (str): string com o texto na íntegra a ser quebrado.
            lang (str): string com a língua a ser utilizada para tokenização do nltk.
        Returns:
            List[str]: lista com as frases tratadas.
        """
        try:
            frases_nltk = nltk.sent_tokenize(texto, language=lang)
        except Exception:
            nltk.download("punkt_tab")
            frases_nltk = nltk.sent_tokenize(texto, language=lang)

        return cls.__divide_frases_grandes(frases_nltk, nmax=900)
