# Requisitos necessários

Para executar o código, é necessário ter instalado o **python 3** e o **git**

# Instruções.

1 - Clone o projeto: no terminal, digite o seguinte comando: `git clone https://github.com/lucaslop/projetoseguranca` <br>
2 - Entre na pasta do projeto. `cd projetoseguranca` <br>
3 - Instale as depedências `https://github.com/lucaslop/projetoseguranca` <br>


## Coleta de dados na google play store

1 - Definir Apps que serão coletados: No arquivo `lista-android-apps.txt`, está o **nome** do aplicativo seguido pelo seu **id**. Insira por linha, o nome e o id aplicativo que deseja coletar os dados <br>

2 - Coleta: Para coletar os dados da google play store, digite o comando: `python3 android.py`. <br>

3 - Dados: Será gerado dois arquivos para cada aplicativo. Um em formato CSV e outro no formato JSON <br>




## Coleta de dados na apple store

1 - Definir Apps que serão coletados: No arquivo `lista-android-ios.txt`, está o **nome** do aplicativo seguido pelo seu **id**. Insira por linha, o nome e o id aplicativo que deseja coletar os dados <br>

2 - Coleta: Para coletar os dados da google play store, digite o comando: `python3 apple.py`. <br>

3 - Dados: Será gerado dois arquivos para cada aplicativo. Um em formato CSV e outro no formato JSON <br>
