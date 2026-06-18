# Python ETL Pipeline

Pipeline ETL (Extract, Transform, Load) simples em Python para processar arquivos Excel, extrair dados de múltiplas fontes, padronizar colunas e gerar saídas em formato Excel e CSV.

> **Nota:** Este é um projeto com fins educacionais, criado para demonstrar conceitos de ETL e manipulação de dados com Python.

## Estrutura do Projeto

```
python-etl-pipeline/
├── .python-version           # Versão do Python (3.14.4)
├── pyproject.toml           # Configuração do projeto e dependências
├── uv.lock                  # Lockfile do uv
├── README.md                # Este arquivo
└── src/
    ├── main.py              # Código principal do pipeline
    └── data/
        ├── raw/             # Arquivos Excel de entrada (.xlsx)
        └── ready/           # Arquivos processados de saída
```

## Dependências

| Biblioteca    | Versão      | Descrição |
|---------------|-------------|-----------|
| `pandas`      | >=3.0.3     | Manipulação e análise de dados tabulares (DataFrames) |
| `openpyxl`    | >=3.1.5     | Leitura e escrita de arquivos Excel (.xlsx) |
| `xlsxwriter`  | >=3.2.9     | Motor de escrita para arquivos Excel com suporte a formatação |

## Como Funciona o Pipeline

O arquivo `src/main.py` executa as seguintes etapas:

### 1. Importação de Bibliotecas

```python
import pandas as pd
import os
import glob
```

- `pandas`: Para manipulação de DataFrames e operações de dados tabulares.
- `os`: Para manipulação de caminhos de arquivos.
- `glob`: Para listar arquivos com padrão curinga.

### 2. Definição do Caminho dos Arquivos

```python
folder_path = 'src/data/raw'
```

Define a pasta onde estão os arquivos Excel de entrada.

### 3. Listagem dos Arquivos Excel

```python
excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))
```

Busca todos os arquivos `.xlsx` na pasta definida. Retorna uma lista vazia se nenhum arquivo for encontrado.

### 4. Processamento de Cada Arquivo

Para cada arquivo encontrado, o pipeline:

- **Lê o arquivo Excel** em um DataFrame:
  ```python
  df = pd.read_excel(file)
  ```

- **Adiciona a coluna `file`** com o nome do arquivo:
  ```python
  df['file'] = file_name
  ```

- **Adiciona a coluna `location`** baseada no nome do arquivo:
  ```python
  if 'brasil' in file_name.lower():
      df['location'] = 'br'
  elif 'france' in file_name.lower():
      df['location'] = 'fr'
  elif 'italian' in file_name.lower():
      df['location'] = 'it'
  ```
  - Arquivos com `brasil` no nome recebem `br`
  - Arquivos com `france` no nome recebem `fr`
  - Arquivos com `italian` no nome recebem `it`

- **Extrai a campanha do link UTM** adicionando a coluna `campaign`:
  ```python
  df['campaign'] = df['utm_link'].str.extract(r"utm_campaign=(.*)")
  ```
  Utiliza regex para extrair o valor do parâmetro `utm_campaign` da coluna `utm_link`.

### 5. Concatenação dos DataFrames

```python
result = pd.concat(df_list, ignore_index=True)
```

Une todos os DataFrames processados em um único DataFrame final.

### 6. Geração dos Arquivos de Saída

```python
output_file = os.path.join('src', 'data', 'ready', 'cleaned_data.xlsx')
output_csv = os.path.join('src', 'data', 'ready', 'cleaned_data.csv')

writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
result.to_excel(writer, index=False)
result.to_csv(output_csv, index=False)
writer.close()
```

Gera dois arquivos na pasta `src/data/ready/`:
- `cleaned_data.xlsx` - Saída em formato Excel
- `cleaned_data.csv` - Saída em formato CSV

### 7. Tratamento de Exceções

```python
except FileNotFoundError as e:
    print(e)
```

- `FileNotFoundError`: Exibe mensagem caso nenhum arquivo seja encontrado na pasta.
- `ValueError`: Exibe mensagem caso um arquivo não contenha indicador de localização reconhecido (`brasil`, `france`, `italian`).

## Arquivos de Entrada

Os arquivos devem estar na pasta `src/data/raw/` com a extensão `.xlsx`. O nome do arquivo **deve conter** um dos indicadores de localização:

| Indicador no Nome | Valor da Coluna `location` |
|-------------------|----------------------------|
| `brasil`          | `br`                       |
| `france`          | `fr`                       |
| `italian`         | `it`                       |

**Exemplos de nomes de arquivos válidos:**
```
netflix_202401_brasil.xlsx
netflix_202401_france.xlsx
netflix_202401_italian.xlsx
```

Os arquivos devem conter pelo menos uma coluna chamada `utm_link` para extração da campanha.

## Saída

Após a execução, serão gerados dois arquivos em `src/data/ready/`:

| Arquivo | Descrição |
|---------|-----------|
| `cleaned_data.xlsx` | Dados consolidados em formato Excel |
| `cleaned_data.csv` | Dados consolidados em formato CSV |

Os arquivos conterão todas as colunas originais dos arquivos de entrada, acrescidas das colunas:
- `file` - Nome do arquivo de origem
- `location` - Código do país (`br`, `fr`, `it`)
- `campaign` - Valor extraído do parâmetro `utm_campaign` do link

## Instalação e Execução

### Usando `uv` (recomendado)

`uv` é o gerenciador de dependências utilizado pelo projeto.

```bash
# Instala as dependências
uv sync

# Executa o pipeline
uv run python src/main.py
```

### Usando `pip`

```bash
# Criar ambiente virtual (opcional mas recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instalar dependências
pip install -e .

# Executar o pipeline
python src/main.py
```

Ou instalar as dependências diretamente:

```bash
pip install pandas openpyxl xlsxwriter
python src/main.py
```

## Requisitos

- Python >= 3.14.4
- pandas >= 3.0.3
- openpyxl >= 3.1.5
- xlsxwriter >= 3.2.9