
# Projeto Aplicado: Melhoria do Fluxo de Trabalho para o Tratamento de Lesões Cerebrais Traumáticas Utilizando Big Data

## Descrição

Este repositório contém todo o material relacionado ao Projeto Aplicado desenvolvido como parte da conclusão do curso de pós-graduação (MBA) em Ciência de Dados pela XP Educação. O projeto, intitulado "Melhoria do Fluxo de Trabalho para o Tratamento de Lesões Cerebrais Traumáticas Utilizando Big Data", tem como objetivo aprimorar o diagnóstico, tratamento e prognóstico de pacientes com lesões cerebrais traumáticas (TBI) através da aplicação de técnicas avançadas de análise de dados.

## Objetivo

O principal objetivo deste projeto é desenvolver uma plataforma integrada para a visualização e análise de dados clínicos e experimentais relacionados a TBI, utilizando Big Data, aprendizado de máquina e inteligência artificial para melhorar a qualidade e eficiência do tratamento de pacientes.

## Estrutura do Repositório

O repositório está organizado da seguinte maneira:

```
Projeto-Aplicado-TBI/
│
├── README.md                      # Descrição do projeto
├── docs/                          # Documentação e recursos visuais
│   ├── Relatorio_Projeto_Aplicado.pdf
│   ├── CANVAS_Projeto.png
│   ├── Matriz_CSD.png
│   ├── Matriz_BASICO.png
│   ├── Backlog_Trello.png
│   └── Outros_Graficos/
│       ├── Grafico_Hospitalizacoes_Ano.png
│       ├── Numero_Mortes_vs_Hospitalizacoes.png
│       └── Analise_Cosinor_Animal7.png
│
├── notebooks/                     # Notebooks Jupyter com análises e modelos
│   ├── Sprint1_AnaliseExploratoria.ipynb
│   ├── Sprint2_ModelagemCircadiana.ipynb
│   └── Sprint3_VisualizacaoDados.ipynb
│
└── src/                           # Código-fonte dos scripts Python
    ├── pre_processamento_dados.py
    ├── dashboard_visualizacao.py
    └── modelagem_cosinor.py
```

### Documentação

- **Relatorio_Projeto_Aplicado.pdf**: Documento completo do projeto aplicado, contendo todo o contexto, metodologia, resultados e considerações finais.
- **CANVAS_Projeto.png**: Representação visual do CANVAS do projeto, destacando o desafio, solução, benefícios e justificativas.
- **Matriz_CSD.png**: Matriz Certezas, Suposições e Dúvidas (CSD) utilizada para análise do contexto do problema.
- **Matriz_BASICO.png**: Matriz de priorização BASICO, detalhando as ideias e suas respectivas avaliações.
- **Backlog_Trello.png**: Imagem do backlog de produto gerenciado no Trello.
- **Outros_Graficos/**: Contém gráficos gerados durante as análises e modelagens, como hospitalizações por ano, mortes vs hospitalizações, e análise de Cosinor.

### Notebooks

- **Sprint1_AnaliseExploratoria.ipynb**: Notebook contendo a análise exploratória inicial dos dados, incluindo coleta e visualização preliminar.
- **Sprint2_ModelagemCircadiana.ipynb**: Notebook que implementa a modelagem circadiana utilizando o modelo Cosinor para analisar os dados de temperatura de animais com lesões cerebrais.
- **Sprint3_VisualizacaoDados.ipynb**: Notebook que demonstra a visualização dos dados finais na plataforma desenvolvida.

### Código Fonte

- **pre_processamento_dados.py**: Script responsável pelo pré-processamento dos dados, incluindo limpeza e normalização.
- **dashboard_visualizacao.py**: Script que gera o dashboard interativo para visualização dos principais indicadores sobre os tratamentos.
- **modelagem_cosinor.py**: Script que implementa a modelagem circadiana usando o método Cosinor para análise dos ritmos circadianos.

## Instalação e Execução

1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/Projeto-Aplicado-TBI.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd Projeto-Aplicado-TBI
   ```

3. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv env
   source env/bin/activate  # No Windows: env\Scripts\activate
   ```

4. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

5. Execute os notebooks Jupyter ou scripts Python conforme a necessidade.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias ou correções.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
