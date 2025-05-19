# embedding_prompts
Repositório para implementação de Information Retrieval (a priori, usando BM25) para geração de RAG de prompts de geração de ontologias.

## Como executar

Instale o poetry:

`pip install poetry`

Daí, execute os seguintes comandos: `poetry lock` e `poetry install`. Isso deve instalar todas as dependências necessárias. Ajuste o que precisar no arquivo `pyproject.toml`, na seção `[tool.poetry.dependencies]`.

### Para rodar normalmente

Basta rodar `poetry run py -m BM25.main` do repositório raiz para testar.

### Para utilizar o notebook disponibilizado

Execute `poetry run pip install jupyter`, daí `poetry add notebook --group dev`, para permitir que o poetry rode os notebooks no environment gerado.

Por fim, basta `poetry run jupyter notebook`.