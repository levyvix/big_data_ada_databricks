# Projeto Big Data usando AWS e Databricks

## Descrição
Este repositório contém um projeto de Big Data desenvolvido utilizando AWS e Databricks. O objetivo é demonstrar o uso dessas tecnologias para o processamento e análise de grandes volumes de dados.

## Estrutura do Projeto
- **notebooks/**: Contém os notebooks Jupyter usados para a análise e visualização de dados.
- **src/**: Código-fonte do projeto, incluindo scripts de ETL (Extract, Transform, Load).
- **tests/**: Testes automatizados para garantir a qualidade do código.
- **.gitignore**: Arquivo que especifica quais arquivos ou diretórios devem ser ignorados pelo Git.
- **LICENSE**: Licença do projeto.
- **README.md**: Este arquivo.

## Tecnologias Utilizadas
- **AWS**: Para armazenamento e processamento de dados na nuvem.
- **Databricks**: Plataforma unificada de análise de dados.
- **Python**: Linguagem de programação utilizada nos scripts e notebooks.


## Arquitetura

### Medallion Architecture

![architecture](images/architecture.jpeg)

A arquitetura 'Medalion' ou Medalhão, é uma arquitetura de dados que combina os recursos da AWS e da Databricks para fornecer uma solução completa para o processamento e análise de grandes volumes de dados.

É um padrão de design de dados, criado pelo Databricks, usado para organizar logicamente os dados em um LakeHouse, com o objetivo de melhorar incrementalmente a qualidade dos dados à medida que eles fluem por varias camadas.

Esta arquitetura consiste em três camadas - bronze (bruto), prata (validado) e ouro (enriquecido) - cada uma representa niveis progressivamente mais altos de qualidade.

### Estágios do 'Medallion'

### 🥉Bronze

A camada bronze serve como o ponto inicial para a ingestão e armazenamento de dados. Os dados são salvos sem processamento ou transformação. Isso pode incluir o salvamento de logs de uma aplicação em um sistema de arquivos distribuído ou eventos de streaming do Kafka.

### 🥈Prata

A camada prata é onde as tabelas são limpas, filtradas ou transformadas em um formato mais utilizável. As transformações nesta etapa devem ser modificações leves, não agregações ou enriquecimentos. No nosso exemplo inicial, esses logs podem ser analisados para extrair informações úteis — como desaninhamento de estruturas ou eliminação de abreviações. Os eventos podem ser padronizados para unificar convenções de nomenclatura ou dividir um único fluxo em várias tabelas.


### 🥇Ouro

Finalmente, na etapa ouro, os dados são refinados para atender a requisitos específicos de negócios e análises. Isso pode significar agregar dados em uma granularidade específica, como diária ou horária, ou enriquecer os dados com informações de fontes externas. Após a etapa ouro, os dados devem estar prontos para serem consumidos por equipes downstream, como análises, ciência de dados ou operações de Machine Learning.

## Tecnologias

### AWS S3


<img src="images/s3.png" width="100">

O Amazon S3 (Simple Storage Service) é um serviço de armazenamento de objetos oferecido pela AWS (Amazon Web Services). Ele permite que os usuários armazenem e recuperem qualquer quantidade de dados a qualquer momento, de qualquer lugar na web. Os dados são armazenados em "buckets" (baldes), que são repositórios de armazenamento com um nome exclusivo dentro da AWS. Cada objeto dentro de um bucket é identificado por uma chave única (um nome) e pode conter até 5 TB de dados.

### Principais características do Amazon S3

- **Escalabildiade**: O S3 é altamente escalável, suportando um volume massivo de dados e um número muito grande de solicitações simultâneas.

- **Durabilidade**: Os dados são replicados automaticamente em múltiplas regiões, garantindo uma durabilidade de 99,999999999% (11 noves).

- **Segurança**: O S3 oferece várias opções de segurança, incluindo criptografia de dados em repouso e em trânsito, além de controles de acesso granular por meio de políticas de bucket e listas de controle de acesso (ACLs).

- **Custo-beneficio**: O S3 opera com um modelo de pagamento conforme o uso, onde você paga apenas pelo armazenamento e transferência de dados que realmente utiliza.

- **Integração**: O S3 se integra facilmente com outros serviços da AWS, como Lambda, EMR, Athena, e muitos outros, facilitando a criação de soluções robustas e complexas.

### Uso do Amazon S3 em uma arquitetura de LakeHouse

- **Armazenamento Centralizado de Dados Brutos**: O S3 é usado para armazenar grandes volumes de dados brutos provenientes de várias fontes (bases de dados, logs, streams de eventos, etc.). Esses dados são armazenados em seu formato original e não estruturado, permitindo uma ingestão rápida e eficiente.

- **Camada de Dados Curados**: Após o processamento e a limpeza dos dados brutos, os dados curados são armazenados novamente no S3 em formatos otimizados para consulta, como Parquet ou ORC. Isso facilita consultas rápidas e eficientes, aproveitando ferramentas de processamento distribuído.

- **Integração com Ferramentas de Análise e BI**: Ferramentas como AWS Athena, que permite consultas SQL diretamente sobre os dados armazenados no S3, ou AWS Glue, que facilita a catalogação e transformação de dados, podem ser usadas para acessar e analisar os dados armazenados no S3 sem a necessidade de mover os dados para outro repositório.

- **Data Lake com Governança e Segurança**: Com o uso de AWS Lake Formation, é possível implementar governança de dados sobre o S3, definindo políticas de acesso e monitorando o uso dos dados, garantindo conformidade com regulamentos e práticas de segurança.

- **Custo e Eficiência**: O S3 permite o armazenamento escalável e econômico de dados, com a possibilidade de configurar diferentes classes de armazenamento (Standard, Intelligent-Tiering, Glacier) conforme a frequência de acesso e necessidade de recuperação de dados.

## Databricks
<img src="images/databricks logo.png" width="150">

O *Databricks* é uma plataforma de dados unificada que combina engenharia de dados, ciência de dados, e análise de dados, facilitando a criação e gestão de soluções de big data e inteligência artificial. Foi criado pelos fundadores do Apache Spark e é amplamente utilizado para processar e analisar grandes volumes de dados de maneira eficiente.

### Principais características do Databricks:

1. **Apache Spark Simplificado**: O Databricks oferece uma interface simplificada para trabalhar com o Apache Spark, facilitando o desenvolvimento e a execução de pipelines de dados e análises complexas.

2. **Colaboração em Equipe**: Com recursos integrados de colaboração, como notebooks compartilhados e controle de versão, o Databricks permite que equipes colaborem de forma eficaz em projetos de análise de dados.

3. **Escalabilidade e Desempenho**: O Databricks é altamente escalável e oferece um desempenho excepcional para processamento de grandes volumes de dados, graças ao seu suporte ao Apache Spark distribuído.

4. **Integração com Ecossistema de Big Data**: Além do Apache Spark, o Databricks se integra facilmente com outros componentes do ecossistema de big data, como o Delta Lake, para armazenamento de dados, e o MLflow, para gerenciamento de fluxos de trabalho de machine learning.

### Uso do Databricks em uma arquitetura de Lakehouse:

1. **Processamento de Dados em Larga Escala**: O Databricks é utilizado para processar grandes volumes de dados em um ambiente distribuído, aproveitando a capacidade de processamento do Apache Spark.

2. **Preparação e Limpeza de Dados**: Equipes de dados utilizam o Databricks para preparar e limpar dados brutos antes de armazená-los no Data Lake. Isso inclui transformações de dados, deduplicação, e outras operações de limpeza.

3. **Análise e Exploração de Dados**: Cientistas de dados e analistas utilizam o Databricks para realizar análises exploratórias sobre os dados armazenados no Data Lake, utilizando recursos como SQL, Python, e R.

4. **Treinamento de Modelos de Machine Learning**: O Databricks oferece suporte para treinamento de modelos de machine learning em larga escala, utilizando o Apache Spark e integrando-se com bibliotecas populares de machine learning, como o TensorFlow e o PyTorch.

5. **Gerenciamento de Metadados e Governança**: O Databricks fornece recursos para gerenciamento de metadados, rastreamento de proveniência e governança de dados, ajudando as organizações a garantir a qualidade e a segurança dos dados armazenados no Data Lake.

## Python

<img src="images/python logo.png" width="100">

### Por que o Python é utilizado como ingestão em uma arquitetura de Lakehouse:

- **Flexibilidade**: Python é uma linguagem de programação extremamente flexível, o que a torna adequada para lidar com uma variedade de fontes de dados e formatos de dados diferentes.

- **Ecossistema de Bibliotecas**: Python possui um vasto ecossistema de bibliotecas para manipulação, processamento e ingestão de dados. Isso inclui bibliotecas como Pandas, NumPy, SQLAlchemy, e muitas outras, que facilitam a manipulação de dados em diferentes formatos.

- **Integração com Serviços de Nuvem**: Python oferece suporte a várias bibliotecas e SDKs para integração com serviços de nuvem, como AWS, Google Cloud e Azure. Isso permite que os desenvolvedores construam pipelines de ingestão de dados que se integram facilmente com serviços de armazenamento em nuvem, como Amazon S3, Google Cloud Storage e Azure Data Lake Storage.

- **Facilidade de Desenvolvimento**: Python é conhecido por sua sintaxe simples e legível, o que facilita o desenvolvimento e a manutenção de pipelines de ingestão de dados. Além disso, existem frameworks como Apache Airflow e Prefect que podem ser usados para orquestrar e agendar pipelines de ingestão de dados de forma eficiente.

- **Comunidade Ativa**: Python possui uma comunidade de desenvolvedores muito ativa, o que significa que há uma grande quantidade de recursos disponíveis online, incluindo tutoriais, documentação e fóruns de discussão, que podem ajudar os desenvolvedores a resolver problemas e aprender novas técnicas de ingestão de dados.

- **Portabilidade**: Python é uma linguagem de programação portátil, o que significa que os pipelines de ingestão de dados desenvolvidos em Python podem ser executados em uma variedade de ambientes, incluindo localmente em máquinas de desenvolvimento, em servidores de produção e em ambientes de nuvem.


## Como Executar
1. Clone o repositório:
    ```sh
    git clone https://github.com/levyvix/big_data_ada_databricks.git
    ```
2. Navegue até o diretório do projeto:
    ```sh
    cd big_data_ada_databricks
    ```
3. Instale as dependências usando `poetry`:
    ```sh
    poetry install
    ```
4. Renomeie o arquivo `example.env` para `.env` e Preencha o arquivo `.env` com suas informações.
5. Execute o código principal para carregar o arquivo `.csv` na sua pasta S3:
    ```sh
    python src/main.py
    ```
6. Execute os notebooks na sua instância do Databricks.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença
Este projeto está licenciado sob a Licença Apache 2.0. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato
Para dúvidas ou sugestões, abra uma issue no repositório ou entre em contato diretamente.

---

Explore o código, faça experimentos e aprenda mais sobre Big Data com AWS e Databricks. Boa sorte!
