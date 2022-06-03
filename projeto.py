# -*- coding: utf-8 -*-
"""Projeto.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WrMItrKQkaUuxwYmUdMSgch891tFTpv-

Projeto da disciplina de Ciência de dados

Utilizaremos para esse notebook o dataset Brazilian E-Commerce Public Dataset by Olist, disponível no site Kaggle, ele é dividido em 9 arquivos csv que contém informmações sobre o e-commerce brasileiro, informações como estado, preço, frete entre outras que serão trabalhas no notebook. A primeira parte do trabalho foi juntar todos os arquivos, deixamos essa parte fora desse notebook para não deixa-ló pesado na hora de executar. Utilizamos o método merge do pandas com a chave referente a coluna que queremos casar as informações. Após esse passo dividimos nossa analise em quatro partes, a primeira é a analise das vendas por estado, a segunda parte é a analise dos métodos de pagamento, a terceira parte é a azalise das compras por estado e a quarta parte é a analise das datas. Para começar essas analises tiramos as colunas que não seriam necessárias para nossas analises. Após todos esses passos passamos para a EDA, onde ele mostra todo as analises que fizemos com poucas linhas de código.
"""

# Commented out IPython magic to ensure Python compatibility.
#Importações das bibliotecas que utilizaremos no projeto
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
plt.style.use('classic')
# %matplotlib inline

import panel as pn
pn.extension()

from google.colab import drive
drive.mount('/content/drive')

#Leitura do arquivo csv
olist_dataset = pd.read_csv('/content/drive/MyDrive/Projeto_de_ciencia_de_dados/my_dataset.csv')

#Dataset original
olist_dataset.head()

#Retirando as colunas que não serão necessárias.
olist_dataset = olist_dataset.drop(columns = ['Unnamed: 0', 'order_item_id',
                                              'order_id', 'product_id', 'seller_zip_code_prefix',
                                              'seller_id', 'seller_city', 'product_name_lenght',
                                              'product_description_lenght',
                                              'payment_sequential', 'payment_installments'])

#Retirando as colunas que não serão necessárias.
olist_dataset = olist_dataset.drop(columns = ['review_id', 'review_score', 'review_comment_title',
                                              'review_comment_message', 'customer_zip_code_prefix',
                                              'review_creation_date', 'customer_city',
                                              'review_answer_timestamp',
                                              'customer_unique_id', 'customer_id', 'ano_envio', 'mes_envio'])

#Dataset limpo
olist_dataset.head()

#Quantidade de dados faltando por coluna
df_missing = olist_dataset.isnull().sum()
df_missing

#EDA para data missing
import missingno as msno
msno.matrix(olist_dataset)

"""Começamos a analíse do dataset respondendo algumas perguntas que achamos pertimentes.
1. Qual o valor total, o mínimo e máximo, o médio e o total de frete nas vendas de cada estado?
2. Quantidade de vendas e compras em cartão de crédito ou débito, boleto e voucher por estado?
3. Qual o valor total, o mínimo e máximo, o médio e o total de frete nas compras de cada estado?
4. Quanto tempo um pedido demora para ser finalizado?

"""

#Anlise nas vendas de cada estado
df = olist_dataset['seller_state'].value_counts().sort_values(ascending=False)
df1 = olist_dataset.groupby('seller_state').price.sum().sort_values(ascending=False)
df2 = olist_dataset.groupby('seller_state').price.min().sort_values(ascending=False)
df3 = olist_dataset.groupby('seller_state').price.max().sort_values(ascending=False)
df4 = olist_dataset.groupby('seller_state').price.mean().sort_values(ascending=False)
df5 = olist_dataset.groupby('seller_state').freight_value.sum().sort_values(ascending=False)
df6 = olist_dataset.groupby('seller_state').freight_value.mean().sort_values(ascending=False)

df7 = pd.merge(df, df1, on=df.index)
df8 = pd.merge(df7, df2, left_on='key_0', right_on='seller_state')
df9 = pd.merge(df8, df3, left_on='key_0', right_on='seller_state')
df10 = pd.merge(df9, df4, left_on='key_0', right_on='seller_state')
df11 = pd.merge(df10, df5, left_on='key_0', right_on='seller_state')
df12 = pd.merge(df11, df6, left_on='key_0', right_on='seller_state')
df12.set_axis(['Estado', 'Quantidade', 'Preço_total', 'Preço_min', 'Preço_max',
               'Preço_médio', 'Frete_total', 'Frete_médio'], axis='columns', inplace=True)
df12

plt.figure(figsize=(12,6))
plt.bar(df12.Estado, df12.Quantidade)

plt.figure(figsize=(12,6))
plt.bar(df12.Estado, df12.Preço_total)

plt.figure(figsize=(12,6))
plt.bar(df12.Estado, df12.Preço_médio)

plt.figure(figsize=(12,6))
plt.bar(df12.Estado, df12.Frete_médio)

#Dados estatisticos sobre a analise das vendas por estado.
std_quant = df12['Quantidade'].std()
std_pt = df12['Preço_total'].std()
std_pmin = df12['Preço_min'].std()
std_pmax = df12['Preço_max'].std()
std_pm = df12['Preço_médio'].std()
std_ft = df12['Frete_total'].std()
std_fm = df12['Frete_médio'].std()

print(f"O desvio padrão da quantidade: {std_quant}")
print(f"O desvio padrão do preço total: {std_pt}")
print(f"O desvio padrão do preço minimo: {std_pmin}")
print(f"O desvio padrão do preço máximo: {std_pmax}")
print(f"O desvio padrão do preço médio: {std_pm}")
print(f"O desvio padrão do frete total: {std_ft}")
print(f"O desvio padrão do frete médio: {std_fm}")

"""Analisando a tabela de vendas vemos que o desvio padrão não é um bom parametro para realizar analises. Não que os resultados obtidos estejam errados, mas porque a diferença entre os estados são grandes, assim os desvios também serão grandes."""

#Função Densidade de Probabilidade para o preço total
import scipy.stats

hist = np.histogram(df12['Preço_total'], bins=10)
hist_dist = scipy.stats.rv_histogram(hist)

X = np.linspace(-1.0, 1.0, 100)
plt.title("PDF do Preço total por estado")
plt.hist(df12['Preço_total'], density=True, bins=100)
plt.plot(X, hist_dist.pdf(X), label='PDF')
plt.plot(X, hist_dist.cdf(X), label='CDF')
plt.show()

#Métodos de pagamento (melhorar essa parte)
df_vt = olist_dataset.groupby('seller_state').payment_type.value_counts().sort_values(ascending=False)
df_ct = olist_dataset.groupby('customer_state').payment_type.value_counts().sort_values(ascending=False)

resultado = pd.concat([df_vt, df_ct], axis=1, join='outer')
resultado.fillna(value=0, inplace=True)
resultado.columns = ['Vendas', 'Compras']
resultado.rename_axis(index=["Estado", "Metodo"], inplace=True)
resultado

select = pn.widgets.Select(name='Select', options=['RR','AP','AM','PA','AC','RO',
                                                   'TO','MA','PI','CE','RN','PB',
                                                   'PE','AL','SE','BA','MT','DF',
                                                   'GO','MS','MG','ES','RJ','SP',
                                                   'PR','SC','RS'])

select

pd_test = pd.MultiIndex.to_frame(resultado.index)
result = pd.concat([resultado, pd_test], axis=1, join='outer')
result.set_axis(['Vendas', 'Compras', 'Estados', 'Metodos'], axis='columns', inplace=True)
compras = result.groupby(['Metodos','Estados']).Compras.sum()
vendas = result.groupby(['Metodos', 'Estados']).Vendas.sum()

df_geral = pd.merge(compras, vendas, left_index=True, right_index=True)
df_estado = df_geral.xs(select.value, level="Estados")

#Plot da porcentagem de cada método de venda por estado 
plt.title(select.value, fontsize=15)
plt.pie(df_estado['Vendas'], labels=df_estado.index, autopct='%1.2f%%')

#Plot da porcentagem de cada método de compra por estado 
plt.title(select.value, fontsize=15)
plt.pie(df_estado['Compras'], labels=df_estado.index, autopct='%1.2f%%')

#Anlise nas compras de cada estado
df20 = olist_dataset['customer_state'].value_counts().sort_values(ascending=False)
df21 = olist_dataset.groupby('customer_state').price.sum().sort_values(ascending=False)
df22 = olist_dataset.groupby('customer_state').price.min().sort_values(ascending=False)
df23 = olist_dataset.groupby('customer_state').price.max().sort_values(ascending=False)
df24 = olist_dataset.groupby('customer_state').price.mean().sort_values(ascending=False)
df25 = olist_dataset.groupby('customer_state').freight_value.sum().sort_values(ascending=False)
df26 = olist_dataset.groupby('customer_state').freight_value.mean().sort_values(ascending=False)

df27 = pd.merge(df20, df21, on=df20.index)
df28 = pd.merge(df27, df22, left_on='key_0', right_on='customer_state')
df29 = pd.merge(df28, df23, left_on='key_0', right_on='customer_state')
df30 = pd.merge(df29, df24, left_on='key_0', right_on='customer_state')
df31 = pd.merge(df30, df25, left_on='key_0', right_on='customer_state')
df32 = pd.merge(df31, df26, left_on='key_0', right_on='customer_state')

df32.set_axis(['Estado', 'Quantidade', 'Preço_total', 'Preço_min', 'Preço_max',
               'Preço_médio', 'Frete_total', 'Frete_médio'], axis='columns', inplace=True)
df32

plt.figure(figsize=(12,6))
plt.bar(df32.Estado, df32.Quantidade)

plt.figure(figsize=(12,6))
plt.bar(df32.Estado, df32.Preço_total)

plt.figure(figsize=(12,6))
plt.bar(df32.Estado, df32.Preço_médio)

plt.figure(figsize=(12,6))
plt.bar(df32.Estado, df32.Frete_médio)

"""Iremos fazer a partir desse ponto uma analise sobre os prazos de entrega, se foi cumprido a dara estimada de entrega, quanto tempo levou da aprovação do pedido até a entrega ao ciente.
Começaremos convertendo as colunas que representam datas para o formato datetime, assim teremos um controle maior sobre as informações dessas colunas.
"""

df_date_approved = olist_dataset['order_approved_at'] = pd.to_datetime(olist_dataset['order_approved_at']).to_frame()
df_date_delivered = olist_dataset['order_delivered_customer_date'] = pd.to_datetime(olist_dataset['order_delivered_customer_date']).to_frame()
df_date_estimated = olist_dataset['order_estimated_delivery_date'] = pd.to_datetime(olist_dataset['order_estimated_delivery_date']).to_frame()

df50 = pd.merge(df_date_approved, df_date_delivered, left_index=True, right_index=True)
df51 = pd.merge(df50, df_date_estimated, left_index=True, right_index=True)
df51['Tempo_de_Entrega'] = df51['order_delivered_customer_date'] - df51['order_approved_at']
df51['Tempo_estimado'] = df51['order_estimated_delivery_date'] - df51['order_approved_at']
df51['Dentro_do_tempo'] = df51['Tempo_de_Entrega'] <= df51['Tempo_estimado']
plt.figure(figsize=(12,6))
df51['Dentro_do_tempo'].value_counts().plot(kind='bar')
df51.head(20)

"""Dentro da nossa analise do tempo de entrega temos alguns valores faltantes dentro de ambas as colunas, na coluna order_approved_at temos 15 valores faltantes, que representa 0,0127%, e na coluna order_delivered_customer_date temos 2471 valores faltantes, que representa 2,106%.
Baseado nessas porcentagens podemos despreza os valores faltantes para a nossa analise.
"""

import pandas as pd

import seaborn.apionly as sns
sns.get_dataset_names()
df = sns.load_dataset('car_crashes')

! pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip

from pandas_profiling import ProfileReport
profile = ProfileReport(df12, title="Pandas Profiling Report")
profile

from pandas_profiling import ProfileReport
profile = ProfileReport(df32, title="Pandas Profiling Report")
profile