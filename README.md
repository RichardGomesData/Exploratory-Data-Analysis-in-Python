# Exploratory Data Analysis in Python
 Exploratory Data Analysis in Python




# Análise Exploratória de Dados de Logística + ETL


---

### Kaggle

https://www.kaggle.com/code/richardgomes/an-lise-explorat-ria-de-dados-de-log-stica-e-etl


# **Tópicos**

<ol type="1">
  <li>Manipulação;</li>
  <li>Visualização;</li>
  <li>Storytelling.</li>
</ol>


# **Análise Exploratória de Dados de Logística**


## Contexto


O Loggi Benchmark for Urban Deliveries (BUD) é um repositório do GitHub ([link](https://github.com/loggi/loggibud)) com dados e códigos para problemas típicos que empresas de logística enfrentam: otimização das rotas de entrega, alocação de entregas nos veículos da frota com capacidade limitada, etc. Os dados são sintetizados de fontes públicas (IBGE, IPEA, etc.) e são representativos dos desafios que a startup enfrenta no dia a dia, especialmente com relação a sua escala. 

O **dado bruto** é um arquivo do tipo `JSON` com uma lista de instâncias de entregas. Cada instância representa um conjunto de **entregas** que devem ser realizadas pelos **veículos** do **hub** regional.


## Pacotes e bibliotecas


!pip install geopy
!pip3 install geopandas;


import json
import pandas as pd
import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
import geopy
from geopy.geocoders import Nominatim


import geopandas
from geopy.extra.rate_limiter import RateLimiter



## Próxima análises 
 

1. **Otimização de Rotas e Hubs**:  
   - Analisar se a redistribuição dos hubs pode reduzir o tempo e custo das entregas.  
   - Aplicar algoritmos de roteamento, como o problema do caixeiro-viajante (TSP) ou o algoritmo de Clarke-Wright.  

2. **Eficiência Operacional**:  
   - Comparar o desempenho entre os hubs (tempo médio de entrega, custo por entrega, etc.).  
   - Identificar gargalos ou padrões de atrasos.  

3. **Análise Geográfica**:  
   - Mapear as entregas para visualizar zonas de alta demanda.  
   - Usar clustering (como K-Means) para identificar agrupamentos de entregas e sugerir possíveis novos hubs.  

4. **Impacto Financeiro**:  
   - Avaliar o custo por quilômetro rodado e sua variação entre os hubs.  
   - Estimar o impacto financeiro de uma melhor alocação de rotas e hubs.  

5. **Predição e Planejamento**:  
   - Construir modelos para prever o tempo de entrega com base na distância, volume de pedidos e localização.  
   - Estimar a demanda futura em diferentes regiões usando séries temporais.  

6. **Satisfação do Cliente**:  
   - Relacionar o tempo de entrega e a distância com reclamações ou devoluções.  
   - Identificar padrões em feedbacks para melhorar o serviço.  

