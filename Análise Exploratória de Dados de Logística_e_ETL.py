{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "KJqp9AANOCtf"
   },
   "source": [
    "\n",
    "# Análise Exploratória de Dados de Logística + ETL\n",
    "\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Kaggle\n",
    "\n",
    "https://www.kaggle.com/code/richardgomes/an-lise-explorat-ria-de-dados-de-log-stica-e-etl"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "d9jDtUbDOE1-"
   },
   "source": [
    "# **Tópicos**\n",
    "\n",
    "<ol type=\"1\">\n",
    "  <li>Manipulação;</li>\n",
    "  <li>Visualização;</li>\n",
    "  <li>Storytelling.</li>\n",
    "</ol>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "SmoHgt-lwkpD"
   },
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "GABI6OW8OfQ2"
   },
   "source": [
    "# **Exercícios**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "muD1vxozykSC"
   },
   "source": [
    "Este *notebook* deve servir como um guia para **você continuar** a construção da sua própria análise exploratória de dados. Fique a vontate para copiar os códigos da aula mas busque explorar os dados ao máximo. Por fim, publique seu *notebook* no [Kaggle](https://www.kaggle.com/)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "zMN1Q3jdwoJm"
   },
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "QRcqbpLpFK5o"
   },
   "source": [
    "# **Análise Exploratória de Dados de Logística**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "6-CvdKwqFPiW"
   },
   "source": [
    "## 1\\. Contexto"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "O Loggi Benchmark for Urban Deliveries (BUD) é um repositório do GitHub ([link](https://github.com/loggi/loggibud)) com dados e códigos para problemas típicos que empresas de logística enfrentam: otimização das rotas de entrega, alocação de entregas nos veículos da frota com capacidade limitada, etc. Os dados são sintetizados de fontes públicas (IBGE, IPEA, etc.) e são representativos dos desafios que a startup enfrenta no dia a dia, especialmente com relação a sua escala. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "XRURE1uUFXGw"
   },
   "source": [
    "O **dado bruto** é um arquivo do tipo `JSON` com uma lista de instâncias de entregas. Cada instância representa um conjunto de **entregas** que devem ser realizadas pelos **veículos** do **hub** regional."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "QxukLHaqFnkU"
   },
   "source": [
    "## 2\\. Pacotes e bibliotecas"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "id": "VXUEW0VrF7XW"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: geopy in /home/richard/anaconda3/lib/python3.12/site-packages (2.4.1)\n",
      "Requirement already satisfied: geographiclib<3,>=1.52 in /home/richard/anaconda3/lib/python3.12/site-packages (from geopy) (2.0)\n",
      "Requirement already satisfied: geopandas in /home/richard/anaconda3/lib/python3.12/site-packages (1.0.1)\n",
      "Requirement already satisfied: numpy>=1.22 in /home/richard/anaconda3/lib/python3.12/site-packages (from geopandas) (1.26.4)\n",
      "Requirement already satisfied: pyogrio>=0.7.2 in /home/richard/anaconda3/lib/python3.12/site-packages (from geopandas) (0.10.0)\n",
      "Requirement already satisfied: packaging in /home/richard/anaconda3/lib/python3.12/site-packages (from geopandas) (23.2)\n",
      "Requirement already satisfied: pandas>=1.4.0 in /home/richard/anaconda3/lib/python3.12/site-packages (from geopandas) (2.2.2)\n",
      "Requirement already satisfied: pyproj>=3.3.0 in /home/richard/anaconda3/lib/python3.12/site-packages (from geopandas) (3.7.0)\n",
      "Requirement already satisfied: shapely>=2.0.0 in /home/richard/anaconda3/lib/python3.12/site-packages (from geopandas) (2.0.6)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in /home/richard/anaconda3/lib/python3.12/site-packages (from pandas>=1.4.0->geopandas) (2.9.0.post0)\n",
      "Requirement already satisfied: pytz>=2020.1 in /home/richard/anaconda3/lib/python3.12/site-packages (from pandas>=1.4.0->geopandas) (2024.1)\n",
      "Requirement already satisfied: tzdata>=2022.7 in /home/richard/anaconda3/lib/python3.12/site-packages (from pandas>=1.4.0->geopandas) (2023.3)\n",
      "Requirement already satisfied: certifi in /home/richard/anaconda3/lib/python3.12/site-packages (from pyogrio>=0.7.2->geopandas) (2024.8.30)\n",
      "Requirement already satisfied: six>=1.5 in /home/richard/anaconda3/lib/python3.12/site-packages (from python-dateutil>=2.8.2->pandas>=1.4.0->geopandas) (1.16.0)\n"
     ]
    }
   ],
   "source": [
    "!pip install geopy\n",
    "!pip3 install geopandas;\n",
    "\n",
    "\n",
    "import json\n",
    "import pandas as pd\n",
    "import sqlite3\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import seaborn as sns \n",
    "import matplotlib.pyplot as plt\n",
    "import geopy\n",
    "from geopy.geocoders import Nominatim\n",
    "\n",
    "\n",
    "import geopandas\n",
    "from geopy.extra.rate_limiter import RateLimiter"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "irQxHW1zGkdZ"
   },
   "source": [
    "## 3\\. Exploração de dados"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Processamos o **dado bruto** e construímos o DataFrame Pandas `deliveries_df` através de operações como achatamento (`flatten`) e explosão (``explode``) de colunas:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "id": "lxLj8e0GHAnr"
   },
   "outputs": [],
   "source": [
    "# - coleta de dados;\n",
    "\n",
    "\n",
    "!wget -q \"https://raw.githubusercontent.com/andre-marcos-perez/ebac-course-utils/main/dataset/deliveries.json\" -O deliveries.json "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "list"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# dado bruto em um dict\n",
    "\n",
    "with open('deliveries.json', mode='r', encoding='utf8') as file:\n",
    "  data = json.load(file)\n",
    "\n",
    "\n",
    "type(data)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>name</th>\n",
       "      <th>region</th>\n",
       "      <th>origin</th>\n",
       "      <th>vehicle_capacity</th>\n",
       "      <th>deliveries</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>{'lng': -48.05498915846707, 'lat': -15.8381445...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': '313483a19d2f8d65cd5024c8d215cfbd', 'p...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>cvrp-2-df-73</td>\n",
       "      <td>df-2</td>\n",
       "      <td>{'lng': -48.05498915846707, 'lat': -15.8381445...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': 'bf3fc630b1c29601a4caf1bdd474b85', 'po...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>cvrp-2-df-20</td>\n",
       "      <td>df-2</td>\n",
       "      <td>{'lng': -48.05498915846707, 'lat': -15.8381445...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': 'b30f1145a2ba4e0b9ac0162b68d045c3', 'p...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>cvrp-1-df-71</td>\n",
       "      <td>df-1</td>\n",
       "      <td>{'lng': -47.89366206897872, 'lat': -15.8051175...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': 'be3ed547394196c12c7c27c89ac74ed6', 'p...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>cvrp-2-df-87</td>\n",
       "      <td>df-2</td>\n",
       "      <td>{'lng': -48.05498915846707, 'lat': -15.8381445...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': 'a6328fb4dc0654eb28a996a270b0f6e4', 'p...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "           name region                                             origin  \\\n",
       "0  cvrp-2-df-33   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   \n",
       "1  cvrp-2-df-73   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   \n",
       "2  cvrp-2-df-20   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   \n",
       "3  cvrp-1-df-71   df-1  {'lng': -47.89366206897872, 'lat': -15.8051175...   \n",
       "4  cvrp-2-df-87   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   \n",
       "\n",
       "   vehicle_capacity                                         deliveries  \n",
       "0               180  [{'id': '313483a19d2f8d65cd5024c8d215cfbd', 'p...  \n",
       "1               180  [{'id': 'bf3fc630b1c29601a4caf1bdd474b85', 'po...  \n",
       "2               180  [{'id': 'b30f1145a2ba4e0b9ac0162b68d045c3', 'p...  \n",
       "3               180  [{'id': 'be3ed547394196c12c7c27c89ac74ed6', 'p...  \n",
       "4               180  [{'id': 'a6328fb4dc0654eb28a996a270b0f6e4', 'p...  "
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# wrangling da estrutura;\n",
    "\n",
    "# dado bruto no pandas\n",
    "\n",
    "deliveries_df = pd.DataFrame(data)\n",
    "\n",
    "deliveries_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Index(['name', 'region', 'origin', 'vehicle_capacity', 'deliveries'], dtype='object')\n"
     ]
    }
   ],
   "source": [
    "print(deliveries_df.columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 199 entries, 0 to 198\n",
      "Data columns (total 5 columns):\n",
      " #   Column            Non-Null Count  Dtype \n",
      "---  ------            --------------  ----- \n",
      " 0   name              199 non-null    object\n",
      " 1   region            199 non-null    object\n",
      " 2   origin            199 non-null    object\n",
      " 3   vehicle_capacity  199 non-null    int64 \n",
      " 4   deliveries        199 non-null    object\n",
      "dtypes: int64(1), object(4)\n",
      "memory usage: 7.9+ KB\n"
     ]
    }
   ],
   "source": [
    "deliveries_df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>name</th>\n",
       "      <th>region</th>\n",
       "      <th>origin</th>\n",
       "      <th>vehicle_capacity</th>\n",
       "      <th>deliveries</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>{'lng': -48.05498915846707, 'lat': -15.8381445...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': '313483a19d2f8d65cd5024c8d215cfbd', 'p...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>cvrp-2-df-73</td>\n",
       "      <td>df-2</td>\n",
       "      <td>{'lng': -48.05498915846707, 'lat': -15.8381445...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': 'bf3fc630b1c29601a4caf1bdd474b85', 'po...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>cvrp-2-df-20</td>\n",
       "      <td>df-2</td>\n",
       "      <td>{'lng': -48.05498915846707, 'lat': -15.8381445...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': 'b30f1145a2ba4e0b9ac0162b68d045c3', 'p...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>cvrp-1-df-71</td>\n",
       "      <td>df-1</td>\n",
       "      <td>{'lng': -47.89366206897872, 'lat': -15.8051175...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': 'be3ed547394196c12c7c27c89ac74ed6', 'p...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>cvrp-2-df-87</td>\n",
       "      <td>df-2</td>\n",
       "      <td>{'lng': -48.05498915846707, 'lat': -15.8381445...</td>\n",
       "      <td>180</td>\n",
       "      <td>[{'id': 'a6328fb4dc0654eb28a996a270b0f6e4', 'p...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "           name region                                             origin  \\\n",
       "0  cvrp-2-df-33   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   \n",
       "1  cvrp-2-df-73   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   \n",
       "2  cvrp-2-df-20   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   \n",
       "3  cvrp-1-df-71   df-1  {'lng': -47.89366206897872, 'lat': -15.8051175...   \n",
       "4  cvrp-2-df-87   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   \n",
       "\n",
       "   vehicle_capacity                                         deliveries  \n",
       "0               180  [{'id': '313483a19d2f8d65cd5024c8d215cfbd', 'p...  \n",
       "1               180  [{'id': 'bf3fc630b1c29601a4caf1bdd474b85', 'po...  \n",
       "2               180  [{'id': 'b30f1145a2ba4e0b9ac0162b68d045c3', 'p...  \n",
       "3               180  [{'id': 'be3ed547394196c12c7c27c89ac74ed6', 'p...  \n",
       "4               180  [{'id': 'a6328fb4dc0654eb28a996a270b0f6e4', 'p...  "
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "deliveries_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0    {'lng': -48.05498915846707, 'lat': -15.8381445...\n",
      "1    {'lng': -48.05498915846707, 'lat': -15.8381445...\n",
      "2    {'lng': -48.05498915846707, 'lat': -15.8381445...\n",
      "3    {'lng': -47.89366206897872, 'lat': -15.8051175...\n",
      "4    {'lng': -48.05498915846707, 'lat': -15.8381445...\n",
      "Name: origin, dtype: object\n",
      "[<class 'dict'>]\n"
     ]
    }
   ],
   "source": [
    "print(deliveries_df['origin'].head())\n",
    "print(deliveries_df['origin'].apply(type).unique())\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "# coluna origin\n",
    "\n",
    "\n",
    "hub_origin_df = pd.json_normalize(deliveries_df['origin'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "deliveries_df = pd.merge(left=deliveries_df, right=hub_origin_df, how='inner', left_index=True, right_index=True)\n",
    "deliveries_df = deliveries_df.drop(\"origin\", axis=1)\n",
    "deliveries_df = deliveries_df[[\"name\", \"region\", \"lng\", \"lat\", \"vehicle_capacity\", \"deliveries\"]]\n",
    "deliveries_df.rename(columns={\"lng\": \"hub_lng\", \"lat\": \"hub_lat\"}, inplace=True)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "# coluna deliveries\n",
    "\n",
    "deliveries_exploded_df = deliveries_df[[\"deliveries\"]].explode(\"deliveries\")\n",
    "\n",
    "deliveries_normalized_df = pd.concat([\n",
    "  pd.DataFrame(deliveries_exploded_df[\"deliveries\"].apply(lambda record: record[\"size\"])).rename(columns={\"deliveries\": \"delivery_size\"}),\n",
    "  pd.DataFrame(deliveries_exploded_df[\"deliveries\"].apply(lambda record: record[\"point\"][\"lng\"])).rename(columns={\"deliveries\": \"delivery_lng\"}),\n",
    "  pd.DataFrame(deliveries_exploded_df[\"deliveries\"].apply(lambda record: record[\"point\"][\"lat\"])).rename(columns={\"deliveries\": \"delivery_lat\"}),\n",
    "], axis= 1)\n",
    "\n",
    "deliveries_df = deliveries_df.drop(\"deliveries\", axis=1)\n",
    "deliveries_df = pd.merge(left=deliveries_df, right=deliveries_normalized_df, how='right', left_index=True, right_index=True)\n",
    "deliveries_df.reset_index(inplace=True, drop=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>name</th>\n",
       "      <th>region</th>\n",
       "      <th>hub_lng</th>\n",
       "      <th>hub_lat</th>\n",
       "      <th>vehicle_capacity</th>\n",
       "      <th>delivery_size</th>\n",
       "      <th>delivery_lng</th>\n",
       "      <th>delivery_lat</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>180</td>\n",
       "      <td>9</td>\n",
       "      <td>-48.116189</td>\n",
       "      <td>-15.848929</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>180</td>\n",
       "      <td>2</td>\n",
       "      <td>-48.118195</td>\n",
       "      <td>-15.850772</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>180</td>\n",
       "      <td>1</td>\n",
       "      <td>-48.112483</td>\n",
       "      <td>-15.847871</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>180</td>\n",
       "      <td>2</td>\n",
       "      <td>-48.118023</td>\n",
       "      <td>-15.846471</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>180</td>\n",
       "      <td>7</td>\n",
       "      <td>-48.114898</td>\n",
       "      <td>-15.858055</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "           name region    hub_lng    hub_lat  vehicle_capacity  delivery_size  \\\n",
       "0  cvrp-2-df-33   df-2 -48.054989 -15.838145               180              9   \n",
       "1  cvrp-2-df-33   df-2 -48.054989 -15.838145               180              2   \n",
       "2  cvrp-2-df-33   df-2 -48.054989 -15.838145               180              1   \n",
       "3  cvrp-2-df-33   df-2 -48.054989 -15.838145               180              2   \n",
       "4  cvrp-2-df-33   df-2 -48.054989 -15.838145               180              7   \n",
       "\n",
       "   delivery_lng  delivery_lat  \n",
       "0    -48.116189    -15.848929  \n",
       "1    -48.118195    -15.850772  \n",
       "2    -48.112483    -15.847871  \n",
       "3    -48.118023    -15.846471  \n",
       "4    -48.114898    -15.858055  "
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "deliveries_df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "98hexQTyJS9I"
   },
   "source": [
    "## 4\\. Manipulação"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### **Enriquecimento** "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- **Geocodificação reversa do hub**\n",
    "\n",
    "\n",
    "A **geocodificação** é o processo que transforma uma localização descrita por um texto (endereço, nome do local, etc.) em sua respectiva coodernada geográfica (latitude e longitude). A **geocodificação reversa** faz o oposto, transforma uma coordenada geográfica de um local em suas respectivas descrições textuais."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "id": "DXU4Ee0QJS9Q"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<bound method DataFrame.__len__ of        region    hub_lng    hub_lat\n",
      "0        df-2 -48.054989 -15.838145\n",
      "1        df-2 -48.054989 -15.838145\n",
      "2        df-2 -48.054989 -15.838145\n",
      "3        df-2 -48.054989 -15.838145\n",
      "4        df-2 -48.054989 -15.838145\n",
      "...       ...        ...        ...\n",
      "636144   df-2 -48.054989 -15.838145\n",
      "636145   df-2 -48.054989 -15.838145\n",
      "636146   df-2 -48.054989 -15.838145\n",
      "636147   df-2 -48.054989 -15.838145\n",
      "636148   df-2 -48.054989 -15.838145\n",
      "\n",
      "[636149 rows x 3 columns]>\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>region</th>\n",
       "      <th>hub_lng</th>\n",
       "      <th>hub_lat</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  region    hub_lng    hub_lat\n",
       "0   df-2 -48.054989 -15.838145\n",
       "1   df-2 -48.054989 -15.838145\n",
       "2   df-2 -48.054989 -15.838145\n",
       "3   df-2 -48.054989 -15.838145\n",
       "4   df-2 -48.054989 -15.838145"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# faça o código de manipulação de dados:\n",
    "#\n",
    "\n",
    "# - controle de qualidade;\n",
    "# - etc.\n",
    "\n",
    "\n",
    "hub_df = deliveries_df[[\"region\", \"hub_lng\", \"hub_lat\"]]\n",
    "print(hub_df.__len__)\n",
    "hub_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 636149 entries, 0 to 636148\n",
      "Data columns (total 3 columns):\n",
      " #   Column   Non-Null Count   Dtype  \n",
      "---  ------   --------------   -----  \n",
      " 0   region   636149 non-null  object \n",
      " 1   hub_lng  636149 non-null  float64\n",
      " 2   hub_lat  636149 non-null  float64\n",
      "dtypes: float64(2), object(1)\n",
      "memory usage: 14.6+ MB\n"
     ]
    }
   ],
   "source": [
    "hub_df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<bound method DataFrame.__len__ of   region    hub_lng    hub_lat\n",
      "0   df-0 -47.802665 -15.657014\n",
      "1   df-1 -47.893662 -15.805118\n",
      "2   df-2 -48.054989 -15.838145>\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>region</th>\n",
       "      <th>hub_lng</th>\n",
       "      <th>hub_lat</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>df-0</td>\n",
       "      <td>-47.802665</td>\n",
       "      <td>-15.657014</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>df-1</td>\n",
       "      <td>-47.893662</td>\n",
       "      <td>-15.805118</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  region    hub_lng    hub_lat\n",
       "0   df-0 -47.802665 -15.657014\n",
       "1   df-1 -47.893662 -15.805118\n",
       "2   df-2 -48.054989 -15.838145"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "hub_df = hub_df.drop_duplicates().sort_values(by=\"region\").reset_index(drop=True)\n",
    "print(hub_df.__len__)\n",
    "hub_df.head()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 3 entries, 0 to 2\n",
      "Data columns (total 3 columns):\n",
      " #   Column   Non-Null Count  Dtype  \n",
      "---  ------   --------------  -----  \n",
      " 0   region   3 non-null      object \n",
      " 1   hub_lng  3 non-null      float64\n",
      " 2   hub_lat  3 non-null      float64\n",
      "dtypes: float64(2), object(1)\n",
      "memory usage: 204.0+ bytes\n"
     ]
    }
   ],
   "source": [
    "hub_df.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Empresas como Google, Bing e Yahoo! fornecem **geocodificação** como serviço (e cobram por isso). Existe uma projeto *open source* chamado de [OpenStreetMap](https://www.openstreetmap.org/) que mantem um serviço gratuito de geocodificação chamado [Nominatim](https://nominatim.org/), serviço este que apresenta como limitação a quantia de [uma única consuta por segundo](https://operations.osmfoundation.org/policies/nominatim/). Vamos utilizá-lo através do pacote Python `geopy` para fazer a operação reversa e enriquecer o nosso DataFrame principal."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{\n",
      "  \"place_id\": 14345465,\n",
      "  \"licence\": \"Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright\",\n",
      "  \"osm_type\": \"way\",\n",
      "  \"osm_id\": 240210480,\n",
      "  \"lat\": \"-15.656916027876347\",\n",
      "  \"lon\": \"-47.80264463632131\",\n",
      "  \"class\": \"highway\",\n",
      "  \"type\": \"secondary\",\n",
      "  \"place_rank\": 26,\n",
      "  \"importance\": 0.053411383993285995,\n",
      "  \"addresstype\": \"road\",\n",
      "  \"name\": \"Rua 7\",\n",
      "  \"display_name\": \"Rua 7, Quadra 2, Sobradinho, Região Geográfica Imediata do Distrito Federal, Região Integrada de Desenvolvimento do Distrito Federal e Entorno, Região Geográfica Intermediária do Distrito Federal, Distrito Federal, Região Centro-Oeste, 73015-202, Brasil\",\n",
      "  \"address\": {\n",
      "    \"road\": \"Rua 7\",\n",
      "    \"residential\": \"Quadra 2\",\n",
      "    \"suburb\": \"Sobradinho\",\n",
      "    \"town\": \"Sobradinho\",\n",
      "    \"municipality\": \"Região Geográfica Imediata do Distrito Federal\",\n",
      "    \"county\": \"Região Integrada de Desenvolvimento do Distrito Federal e Entorno\",\n",
      "    \"state_district\": \"Região Geográfica Intermediária do Distrito Federal\",\n",
      "    \"state\": \"Distrito Federal\",\n",
      "    \"ISO3166-2-lvl4\": \"BR-DF\",\n",
      "    \"region\": \"Região Centro-Oeste\",\n",
      "    \"postcode\": \"73015-202\",\n",
      "    \"country\": \"Brasil\",\n",
      "    \"country_code\": \"br\"\n",
      "  },\n",
      "  \"boundingbox\": [\n",
      "    \"-15.6572841\",\n",
      "    \"-15.6565043\",\n",
      "    \"-47.8047361\",\n",
      "    \"-47.8007862\"\n",
      "  ]\n",
      "}\n"
     ]
    }
   ],
   "source": [
    "# - enriquecimento dos dados\n",
    "\n",
    "geolocator = Nominatim(user_agent=\"ebac_geocoder\")\n",
    "location = geolocator.reverse(\"-15.657013854445248, -47.802664728268745\")\n",
    "\n",
    "print(json.dumps(location.raw, indent=2, ensure_ascii=False))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'geopy.geocoders.nominatim.Nominatim'>\n"
     ]
    }
   ],
   "source": [
    "print(type(geolocator))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'geopy.location.Location'>\n"
     ]
    }
   ],
   "source": [
    "print(type(location))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Vamos então aplicar a geocodificação nas coordenadas das três regiões e extrair informações de **cidade** e **bairro**."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "#from geopy.extra.rate_limiter import RateLimiter\n",
    "\n",
    "geocoder = RateLimiter(geolocator.reverse, min_delay_seconds=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>region</th>\n",
       "      <th>hub_lng</th>\n",
       "      <th>hub_lat</th>\n",
       "      <th>coordinates</th>\n",
       "      <th>geodata</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>df-0</td>\n",
       "      <td>-47.802665</td>\n",
       "      <td>-15.657014</td>\n",
       "      <td>-15.657013854445248, -47.802664728268745</td>\n",
       "      <td>(Rua 7, Quadra 2, Sobradinho, Região Geográfic...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>df-1</td>\n",
       "      <td>-47.893662</td>\n",
       "      <td>-15.805118</td>\n",
       "      <td>-15.80511751066334, -47.89366206897872</td>\n",
       "      <td>(SQS 303, Asa Sul, Brasília, Plano Piloto, Reg...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>-15.83814451122274, -48.05498915846707</td>\n",
       "      <td>(Armazém do Bolo, lote 4/8, CSB 4/5, Taguating...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  region    hub_lng    hub_lat                               coordinates  \\\n",
       "0   df-0 -47.802665 -15.657014  -15.657013854445248, -47.802664728268745   \n",
       "1   df-1 -47.893662 -15.805118    -15.80511751066334, -47.89366206897872   \n",
       "2   df-2 -48.054989 -15.838145    -15.83814451122274, -48.05498915846707   \n",
       "\n",
       "                                             geodata  \n",
       "0  (Rua 7, Quadra 2, Sobradinho, Região Geográfic...  \n",
       "1  (SQS 303, Asa Sul, Brasília, Plano Piloto, Reg...  \n",
       "2  (Armazém do Bolo, lote 4/8, CSB 4/5, Taguating...  "
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "hub_df[\"coordinates\"] = hub_df[\"hub_lat\"].astype(str)  + \", \" + hub_df[\"hub_lng\"].astype(str) \n",
    "hub_df[\"geodata\"] = hub_df[\"coordinates\"].apply(geocoder)\n",
    "hub_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.series.Series'>\n",
      "Armazém do Bolo, lote 4/8, CSB 4/5, Taguatinga, Região Geográfica Imediata do Distrito Federal, Região Integrada de Desenvolvimento do Distrito Federal e Entorno, Região Geográfica Intermediária do Distrito Federal, Distrito Federal, Região Centro-Oeste, 72015-030, Brasil\n"
     ]
    }
   ],
   "source": [
    "print(type(hub_df['geodata']))\n",
    "print(hub_df['geodata'][2])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>place_id</th>\n",
       "      <th>licence</th>\n",
       "      <th>osm_type</th>\n",
       "      <th>osm_id</th>\n",
       "      <th>lat</th>\n",
       "      <th>lon</th>\n",
       "      <th>class</th>\n",
       "      <th>type</th>\n",
       "      <th>place_rank</th>\n",
       "      <th>importance</th>\n",
       "      <th>...</th>\n",
       "      <th>address.state</th>\n",
       "      <th>address.ISO3166-2-lvl4</th>\n",
       "      <th>address.region</th>\n",
       "      <th>address.postcode</th>\n",
       "      <th>address.country</th>\n",
       "      <th>address.country_code</th>\n",
       "      <th>address.neighbourhood</th>\n",
       "      <th>address.city</th>\n",
       "      <th>address.shop</th>\n",
       "      <th>address.house_number</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>14345465</td>\n",
       "      <td>Data © OpenStreetMap contributors, ODbL 1.0. h...</td>\n",
       "      <td>way</td>\n",
       "      <td>240210480</td>\n",
       "      <td>-15.656916027876347</td>\n",
       "      <td>-47.80264463632131</td>\n",
       "      <td>highway</td>\n",
       "      <td>secondary</td>\n",
       "      <td>26</td>\n",
       "      <td>0.053411</td>\n",
       "      <td>...</td>\n",
       "      <td>Distrito Federal</td>\n",
       "      <td>BR-DF</td>\n",
       "      <td>Região Centro-Oeste</td>\n",
       "      <td>73015-202</td>\n",
       "      <td>Brasil</td>\n",
       "      <td>br</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>14374196</td>\n",
       "      <td>Data © OpenStreetMap contributors, ODbL 1.0. h...</td>\n",
       "      <td>way</td>\n",
       "      <td>66353368</td>\n",
       "      <td>-15.805172753950067</td>\n",
       "      <td>-47.89372354453109</td>\n",
       "      <td>highway</td>\n",
       "      <td>residential</td>\n",
       "      <td>26</td>\n",
       "      <td>0.053411</td>\n",
       "      <td>...</td>\n",
       "      <td>Distrito Federal</td>\n",
       "      <td>BR-DF</td>\n",
       "      <td>Região Centro-Oeste</td>\n",
       "      <td>70336-000</td>\n",
       "      <td>Brasil</td>\n",
       "      <td>br</td>\n",
       "      <td>SQS 303</td>\n",
       "      <td>Brasília</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>11624107</td>\n",
       "      <td>Data © OpenStreetMap contributors, ODbL 1.0. h...</td>\n",
       "      <td>node</td>\n",
       "      <td>6249717596</td>\n",
       "      <td>-15.8384371</td>\n",
       "      <td>-48.0552917</td>\n",
       "      <td>shop</td>\n",
       "      <td>pastry</td>\n",
       "      <td>30</td>\n",
       "      <td>0.000051</td>\n",
       "      <td>...</td>\n",
       "      <td>Distrito Federal</td>\n",
       "      <td>BR-DF</td>\n",
       "      <td>Região Centro-Oeste</td>\n",
       "      <td>72015-030</td>\n",
       "      <td>Brasil</td>\n",
       "      <td>br</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Armazém do Bolo</td>\n",
       "      <td>lote 4/8</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>3 rows × 31 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "   place_id                                            licence osm_type  \\\n",
       "0  14345465  Data © OpenStreetMap contributors, ODbL 1.0. h...      way   \n",
       "1  14374196  Data © OpenStreetMap contributors, ODbL 1.0. h...      way   \n",
       "2  11624107  Data © OpenStreetMap contributors, ODbL 1.0. h...     node   \n",
       "\n",
       "       osm_id                  lat                 lon    class         type  \\\n",
       "0   240210480  -15.656916027876347  -47.80264463632131  highway    secondary   \n",
       "1    66353368  -15.805172753950067  -47.89372354453109  highway  residential   \n",
       "2  6249717596          -15.8384371         -48.0552917     shop       pastry   \n",
       "\n",
       "   place_rank  importance  ...     address.state address.ISO3166-2-lvl4  \\\n",
       "0          26    0.053411  ...  Distrito Federal                  BR-DF   \n",
       "1          26    0.053411  ...  Distrito Federal                  BR-DF   \n",
       "2          30    0.000051  ...  Distrito Federal                  BR-DF   \n",
       "\n",
       "        address.region address.postcode address.country address.country_code  \\\n",
       "0  Região Centro-Oeste        73015-202          Brasil                   br   \n",
       "1  Região Centro-Oeste        70336-000          Brasil                   br   \n",
       "2  Região Centro-Oeste        72015-030          Brasil                   br   \n",
       "\n",
       "  address.neighbourhood address.city     address.shop address.house_number  \n",
       "0                   NaN          NaN              NaN                  NaN  \n",
       "1               SQS 303     Brasília              NaN                  NaN  \n",
       "2                   NaN   Taguatinga  Armazém do Bolo             lote 4/8  \n",
       "\n",
       "[3 rows x 31 columns]"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "hub_geodata_df = pd.json_normalize(hub_df[\"geodata\"].apply(lambda data: data.raw))\n",
    "hub_geodata_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "pandas.core.frame.DataFrame"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "type(hub_geodata_df)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>hub_suburb</th>\n",
       "      <th>hub_city</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Sobradinho</td>\n",
       "      <td>Sobradinho</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Asa Sul</td>\n",
       "      <td>Brasília</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   hub_suburb    hub_city\n",
       "0  Sobradinho  Sobradinho\n",
       "1     Asa Sul    Brasília\n",
       "2  Taguatinga  Taguatinga"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "hub_geodata_df = hub_geodata_df[[\"address.town\", \"address.suburb\", \"address.city\"]]\n",
    "hub_geodata_df.rename(columns={\"address.town\": \"hub_town\", \"address.suburb\": \"hub_suburb\", \"address.city\": \"hub_city\"}, inplace=True)\n",
    "hub_geodata_df[\"hub_city\"] = np.where(hub_geodata_df[\"hub_city\"].notna(), hub_geodata_df[\"hub_city\"], hub_geodata_df[\"hub_town\"])\n",
    "hub_geodata_df[\"hub_suburb\"] = np.where(hub_geodata_df[\"hub_suburb\"].notna(), hub_geodata_df[\"hub_suburb\"], hub_geodata_df[\"hub_city\"])\n",
    "hub_geodata_df = hub_geodata_df.drop(\"hub_town\", axis=1)\n",
    "hub_geodata_df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "O DataFrame `hub_geodata_df` com as informações de **cidade** e **bairro** é então combinado ao DataFrame principal `deliveries_df`, enriquecendo assim o dado."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>region</th>\n",
       "      <th>hub_suburb</th>\n",
       "      <th>hub_city</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>df-0</td>\n",
       "      <td>Sobradinho</td>\n",
       "      <td>Sobradinho</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>df-1</td>\n",
       "      <td>Asa Sul</td>\n",
       "      <td>Brasília</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>df-2</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  region  hub_suburb    hub_city\n",
       "0   df-0  Sobradinho  Sobradinho\n",
       "1   df-1     Asa Sul    Brasília\n",
       "2   df-2  Taguatinga  Taguatinga"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "hub_df = pd.merge(left=hub_df, right=hub_geodata_df, left_index=True, right_index=True)\n",
    "hub_df = hub_df[[\"region\", \"hub_suburb\", \"hub_city\"]]\n",
    "hub_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>name</th>\n",
       "      <th>region</th>\n",
       "      <th>hub_lng</th>\n",
       "      <th>hub_lat</th>\n",
       "      <th>hub_city</th>\n",
       "      <th>hub_suburb</th>\n",
       "      <th>vehicle_capacity</th>\n",
       "      <th>delivery_size</th>\n",
       "      <th>delivery_lng</th>\n",
       "      <th>delivery_lat</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>9</td>\n",
       "      <td>-48.116189</td>\n",
       "      <td>-15.848929</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>2</td>\n",
       "      <td>-48.118195</td>\n",
       "      <td>-15.850772</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>1</td>\n",
       "      <td>-48.112483</td>\n",
       "      <td>-15.847871</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>2</td>\n",
       "      <td>-48.118023</td>\n",
       "      <td>-15.846471</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>7</td>\n",
       "      <td>-48.114898</td>\n",
       "      <td>-15.858055</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "           name region    hub_lng    hub_lat    hub_city  hub_suburb  \\\n",
       "0  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "1  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "2  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "3  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "4  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "\n",
       "   vehicle_capacity  delivery_size  delivery_lng  delivery_lat  \n",
       "0               180              9    -48.116189    -15.848929  \n",
       "1               180              2    -48.118195    -15.850772  \n",
       "2               180              1    -48.112483    -15.847871  \n",
       "3               180              2    -48.118023    -15.846471  \n",
       "4               180              7    -48.114898    -15.858055  "
      ]
     },
     "execution_count": 28,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "deliveries_df = pd.merge(left=deliveries_df, right=hub_df, how=\"inner\", on=\"region\")\n",
    "deliveries_df = deliveries_df[[\"name\", \"region\", \"hub_lng\", \"hub_lat\", \"hub_city\", \"hub_suburb\", \"vehicle_capacity\", \"delivery_size\", \"delivery_lng\", \"delivery_lat\"]]\n",
    "deliveries_df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "KSgjP--1JS9R"
   },
   "source": [
    "## 5\\. Visualização"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "replace ./maps/ASB_Cemiterio_A.dbf? [y]es, [n]o, [A]ll, [N]one, [r]ename: ^C\n"
     ]
    }
   ],
   "source": [
    "!wget -q \"https://geoftp.ibge.gov.br/cartas_e_mapas/bases_cartograficas_continuas/bc100/go_df/versao2016/shapefile/bc100_go_df_shp.zip\" -O distrito-federal.zip\n",
    "!unzip -q distrito-federal.zip -d ./maps\n",
    "!cp ./maps/LIM_Unidade_Federacao_A.shp ./distrito-federal.shp\n",
    "!cp ./maps/LIM_Unidade_Federacao_A.shx ./distrito-federal.shx"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>geometry</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>POLYGON Z ((-47.31048 -16.03602 0, -47.31057 -...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                            geometry\n",
       "0  POLYGON Z ((-47.31048 -16.03602 0, -47.31057 -..."
      ]
     },
     "execution_count": 30,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mapa = geopandas.read_file(\"distrito-federal.shp\")\n",
    "mapa = mapa.loc[[0]]\n",
    "mapa.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>region</th>\n",
       "      <th>hub_lng</th>\n",
       "      <th>hub_lat</th>\n",
       "      <th>geometry</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>POINT (-48.05499 -15.83814)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>df-1</td>\n",
       "      <td>-47.893662</td>\n",
       "      <td>-15.805118</td>\n",
       "      <td>POINT (-47.89366 -15.80512)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>df-0</td>\n",
       "      <td>-47.802665</td>\n",
       "      <td>-15.657014</td>\n",
       "      <td>POINT (-47.80266 -15.65701)</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  region    hub_lng    hub_lat                     geometry\n",
       "0   df-2 -48.054989 -15.838145  POINT (-48.05499 -15.83814)\n",
       "1   df-1 -47.893662 -15.805118  POINT (-47.89366 -15.80512)\n",
       "2   df-0 -47.802665 -15.657014  POINT (-47.80266 -15.65701)"
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "hub_df = deliveries_df[[\"region\", \"hub_lng\", \"hub_lat\"]].drop_duplicates().reset_index(drop=True)\n",
    "geo_hub_df = geopandas.GeoDataFrame(hub_df, geometry=geopandas.points_from_xy(hub_df[\"hub_lng\"], hub_df[\"hub_lat\"]))\n",
    "geo_hub_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>name</th>\n",
       "      <th>region</th>\n",
       "      <th>hub_lng</th>\n",
       "      <th>hub_lat</th>\n",
       "      <th>hub_city</th>\n",
       "      <th>hub_suburb</th>\n",
       "      <th>vehicle_capacity</th>\n",
       "      <th>delivery_size</th>\n",
       "      <th>delivery_lng</th>\n",
       "      <th>delivery_lat</th>\n",
       "      <th>geometry</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>9</td>\n",
       "      <td>-48.116189</td>\n",
       "      <td>-15.848929</td>\n",
       "      <td>POINT (-48.11619 -15.84893)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>2</td>\n",
       "      <td>-48.118195</td>\n",
       "      <td>-15.850772</td>\n",
       "      <td>POINT (-48.11819 -15.85077)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>1</td>\n",
       "      <td>-48.112483</td>\n",
       "      <td>-15.847871</td>\n",
       "      <td>POINT (-48.11248 -15.84787)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>2</td>\n",
       "      <td>-48.118023</td>\n",
       "      <td>-15.846471</td>\n",
       "      <td>POINT (-48.11802 -15.84647)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>cvrp-2-df-33</td>\n",
       "      <td>df-2</td>\n",
       "      <td>-48.054989</td>\n",
       "      <td>-15.838145</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>Taguatinga</td>\n",
       "      <td>180</td>\n",
       "      <td>7</td>\n",
       "      <td>-48.114898</td>\n",
       "      <td>-15.858055</td>\n",
       "      <td>POINT (-48.1149 -15.85805)</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "           name region    hub_lng    hub_lat    hub_city  hub_suburb  \\\n",
       "0  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "1  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "2  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "3  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "4  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   \n",
       "\n",
       "   vehicle_capacity  delivery_size  delivery_lng  delivery_lat  \\\n",
       "0               180              9    -48.116189    -15.848929   \n",
       "1               180              2    -48.118195    -15.850772   \n",
       "2               180              1    -48.112483    -15.847871   \n",
       "3               180              2    -48.118023    -15.846471   \n",
       "4               180              7    -48.114898    -15.858055   \n",
       "\n",
       "                      geometry  \n",
       "0  POINT (-48.11619 -15.84893)  \n",
       "1  POINT (-48.11819 -15.85077)  \n",
       "2  POINT (-48.11248 -15.84787)  \n",
       "3  POINT (-48.11802 -15.84647)  \n",
       "4   POINT (-48.1149 -15.85805)  "
      ]
     },
     "execution_count": 32,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "geo_deliveries_df = geopandas.GeoDataFrame(deliveries_df, geometry=geopandas.points_from_xy(deliveries_df[\"delivery_lng\"], deliveries_df[\"delivery_lat\"]))\n",
    "geo_deliveries_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/tmp/ipykernel_15761/1610039930.py:18: MatplotlibDeprecationWarning: The legendHandles attribute was deprecated in Matplotlib 3.7 and will be removed two minor releases later. Use legend_handles instead.\n",
      "  for handle in lgnd.legendHandles:\n"
     ]
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAABj0AAAOgCAYAAABmx7SqAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8fJSN1AAAACXBIWXMAAA9hAAAPYQGoP6dpAAEAAElEQVR4nOzdeXxU5dk//s+ZSSaThJAJiYCasCu40AQE60IlGEWtrSn8niqPdQs2rY9i40KLlrpBqRutRn2o3yeW4FIrrQWjdlNSgqK2YjGxLrggaFIVJGYmy0wymTn374/JOZzZl8zMmeXzfr3yGpiZc+aemTNnkvu6r+uShBACREREREREREREREREac6g9wCIiIiIiIiIiIiIiIjigUEPIiIiIiIiIiIiIiLKCAx6EBERERERERERERFRRmDQg4iIiIiIiIiIiIiIMgKDHkRERERERERERERElBEY9CAiIiIiIiIiIiIioozAoAcREREREREREREREWUEBj2IiIiIiIiIiIiIiCgjMOhBREREREREREREREQZgUEPIiIiIqIMt2nTJkiShCuuuELvoQAAbr/9dkiShNtvv13voaSMK664ApIkYdOmTXoPJSxJkiBJkt7DIIT/LK1evRolJSX45je/iS+//BIAsGzZMlxwwQVJHCURERFRcjHoQURERJRkU6ZMUScNQ/3Ea/Lz/vvvx+233w6r1RqX/VFyKZOa2h+z2YyJEydi7ty5+MEPfoBnnnkGbrc74WNpa2vD7bffjra2toTsf//+/bj99tuTPvFfXV0d9vN43XXXJXVMpK9Anzuj0YiysjIsWrQITU1NkGVZ72GG1N7ejl/84hcYN24cXnzxRZx55pl47bXX8Nprr2HmzJl6D4+IiIgoYXL0HgARERFRtjrmmGMwfvz4oLdPmDAhLo9z//3345NPPsEVV1wBi8USl31S8o0dOxazZ88GAMiyDKvVivfeew9vvvkmmpqaMGXKFGzatAkLFy7027a4uBgzZ87EkUceOaoxtLW14Y477gDgCRTEqqysDDNnzkRZWZnX9fv378cdd9yBhQsX6pKVUlFRgUmTJgW8bdq0aUkeDaUC7edueHgY+/btQ1tbG9ra2vDMM8+gpaUFOTn6/Vkd7LMEAK+88goKCwvx3nvv4fXXX8eFF16I0047DePGjcMPf/hDHUZLRERElBwM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XosdO3ao17344osAPLX8p06d6rfNsmXLcPXVV8PhcATcZ19fH5566ins3LkTn3/+ORwOB4QQGBoaAgB0dHR43b+iogLvv/8+fv/73wd8jWJRVVWFefPm+V2v1PP/+OOPva5/4YUXAADXXnut3zaSJOFHP/oRfvjDH+KFF17AmjVr4jJGrcLCQvXffX19GDt2bMj7V1RUYO/evXjxxRdx9tlnx3Usl112WVz3BwDvvfceOjs7YTabUV9f73f70Ucfjf/v//v/8Lvf/Q4vvPACzjzzzKj2X1FRgUmTJvldf+SRR6r/VhpXBzvGzj33XJhMJrz66qtwuVzIycnByy+/DLvdjsmTJ+O8887z26a2thZHH300/vOf/3hd/8knn2D37t0YP348LrjggoCPd8EFF+CXv/wlduzYgVtuucXv9nDvQ7Sfs9G68sorYTab/a6/+uqrsWXLFvztb39Tr4vH+z3a41DpL+Pr+OOPx4MPPojZs2d7XR/r8TE4OIhjjjkGp59+ut82yjl03759UY//73//O5577jl88MEH6OvrgyzLAACbzQa73Y4PP/wQxx13HABPfx+73Y5JkyYF/C6YP38+Tj31VLz22mt48cUXMX369KjHQ0RERJQMDHoQERER6eSnP/1p0CBCKMEmmo444gh0dnaiv78/pqDHMcccA6PR6Hf9Bx98gMHBQZhMJnzzm98MuK0QAgC8Jm0//PBDAMDXvva1gNuYzWYcc8wxeOutt/xue/PNN/Gtb30Ln332WdDx+jbive6667Bt2zbU19fjl7/8Jc455xwsWLAAixYtiun1AIK/1kqwStuA2mq14ssvvwTgmRAN5IQTTgDgeU0TQTuecAEPALj++utxzTXXYPHixTjppJNw1llnYcGCBVi4cCGKiopGNRZlIjWelNdt0qRJXgEerdG8xsuXL/drCK3V39+vNq7+wQ9+EHJfg4OD6O7uxoQJE9SxzJo1K+AEusFgwLHHHusX9Pj3v/+t7mvBggVBHweA37aKUO9DLJ+z0Qo2HuX6AwcOoLe3F2PHjo3L+z3a43Ds2LFqYKOvr089Hx599NGYO3eu131jPT7CnSsBT2A7mqCH0+nERRddFLJBPOD9/oY7TgHP6/3aa68l7BxGREREFA8MehARERGlmWCTfwaDAcDhAES89muz2QB4JtFeeeWVkPtQJmABYGBg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vPnmm0IIIbZv3y4AiIULF4Yc95YtW0RBQYEAIMxms6iqqhInn3yyqKioUPe/atUqr206OzvFpEmTBACRm5sr5s6dK2bOnCkAiAsuuECcccYZAoB46aWXvLZbuXKlus9JkyaJk046SeTn54vc3Fzx61//WgAQkydP9tqmuLhYABB5eXnixBNPFPPnzxdHHnmkup9bbrkl5PPTam5uFgDE5ZdfHvD2UK/Zhg0bhCRJAoCYMGGCmD9/vrBYLOrYnn/++YjHIYQQt912mwAgxo4dqx4bp556qjj++OOF2WxWn9/UqVP9XsdQz6enp0fdtrCwUFRWVop58+aJsrIyAUBIkiSampq89mOz2URJSYkAII488khx+umni4ULF4o777xTvU+w4zDQc7rtttv8bjvzzDMFAFFUVCS+/vWvi4ULF4qLLrpIvV2WZXHxxRerY58xY4aYO3euMJlM6vGyd+/eyF7cEQsXLgw6nkB27typvk65ubli9uzZ4utf/7qYNm2a+t5rxyyEEH19feKkk05SX9vZs2eLE088UUiSJObOnSuWLVsmAIjm5ma/x3vooYeE0WhUX5eTTjpJzJs3T0yYMEF9HX796197bRPufCFEbJ+zSPftS3mN16xZI0wmkygqKhLz5s0TRx11lLq/e+65x2+7WN/vWMaopRyjoc6LVqtVFBUVCQBi69at6vWxHB82m01UVVUJAMJgMIivfe1rYvbs2UKSJDFv3jz1+HjssccCjtP32H3jjTdEXl6eeu446aST1Nf60ksvVd+P7du3e21nt9vFokWL1Nfv+OOPF5WVlerxV1lZKQ4dOhTLS0pERESUNMz0ICIiItLJhx9+iFdeeSXoz8cffxyXx7n00kvR2NiIr33ta9i7dy927NiBHTt2+K1ADmfJkiV499130dDQgClTpuD999/Hu+++i4KCAixZsgSPPvoobrrpJq9tysvL8frrr+MHP/gBSktL8c4770CWZaxZswZPP/007HY7AP+muPfccw/uv/9+zJo1C1988QU++eQTnHXWWXj55Zdx7rnnBhzfo48+ih/84Ac45phj8Nlnn+Gtt95Sx7Zjxw6sWbMmqucbq//5n//Byy+/jO985zuQZRnt7e0oKCjAJZdcgt27d8fUbwPwZGYox8bu3btx6NAhHHfccfj+97+PZ555Bh9++CG+8Y1vRLy/oqIiPP7447j00ktRUVGB/fv345133sG4ceNwySWX4M0338T3v/99r23Gjh2LF154Aeeddx6Ghobw2muvYceOHdizZ09MzymQJ598EldccQXGjh2Lf/3rX9ixYwf+8Y9/qLdLkoQnnngCjz32GL7xjW/g4MGDeOeddzB58mT8+Mc/xu7du9WMlEQ5/fTT8e6772L16tU4/vjjsW/fPrz11lswGAw499xzsWHDBjQ2NnptM2bMGLS1tWHVqlWYNGkS3n//ffT19eH666/Hjh07AvbVUFxzzTVob2/H97//fRxxxBF455138OGHH6KsrAz//d//jT/84Q+47LLLon4esXzORusb3/gGXn75ZSxYsAAfffQRenp6cMopp2DLli1qVodWKrzfwRQXF6ul5H7xi1+o18dyfIwdOxYvvfQSVq5cifLycuzZswe9vb24/vrrsX37djXDJ9IG4ieddBJeeuklnH322ZBlGXv27MH48ePxwAMP4NFHHw26XX5+Pv72t7+hsbER8+bNwyeffIIPPvgAxx9/PH7+85/j1VdfRWlpabQvFREREVFSSUIE6VBGRERERJRAsixj3LhxsNls+Oqrr1BSUqL3kIgoQaqrq7Fjxw5s374d1dXVeg8n7cyePRtvv/023nzzTVRVVek9HCIiIqKUxkwPIiIiItLFli1bYLPZcPzxxzPgQUQUxK5du/D222/DYrHghBNO0Hs4RERERCmPQQ8iIiIiSpgDBw7gnnvuQXd3t9f1f/3rX3HVVVcBgHpJRJTNfvrTn+I///mP13Wvv/46LrzwQgDA8uXLo25oTkRERJSNWN6KiIiIiBJm//79mDp1KiRJQnl5OSZOnIiuri58/vnnAIDzzz8fLS0tMBqNOo+UiBKJ5a3CkyQJADBx4kRUVFTg4MGD+OSTTwAA8+bNw/bt2zFmzBg9h0hERESUFpjpQUREREQJM378eNx22204+eSTMTQ0hPb2dtjtdpx++ul4+OGH8cwzzzDgQUQE4O6778bChQsBAB0dHeju7sZJJ52Eu+++Gzt27GDAg4iIiChCzPQgIiIiIiIiIiIiIqKMwEwPIiIiIiIiIiIiIiLKCDl6D0APsizjs88+Q1FRkVo3lYiIiIiIiIiIiIiIUpMQAn19fTjqqKNgMATP58jKoMdnn32GiooKvYdBRERERERERERERERR6OzsRHl5edDbszLoUVRUBMDz4owdO1bn0RARERERERERERERUSi9vb2oqKhQ5/eDycqgh1LSauzYsQx6EBERERERERERERGliXAtK9jInIiIiIiIiIiIiIiIMgKDHkRERERERERERERElBEY9CAiIiIiIiIiIiIioozAoAcREREREREREREREWUEBj2IiIiIiIiIiIiIiCgjMOhBREREREREREREREQZIUfvARARERERERERERERxUoIgeHhYciyrPdQKEIGgwG5ubmQJCnu+2bQg4iIiIiIiIiIiIjSjtPpxMGDB2G32+F2u/UeDkXJaDSioKAA48ePh8lkitt+GfQgIiIiIiIiIiIiorRit9vR2dkJo9GIkpIS5Ofnw2g0JiRzgOJLCAG32w2HwwGbzYb9+/ejvLwcBQUFcdk/gx5ERERERERERERElFYOHTqE3NxcTJ48GUajUe/hUAzGjBmDcePG4ZNPPsGhQ4cwadKkuOyXjcyJiIiIiIiIiIiIKG24XC4MDAxg3LhxDHikOaPRiHHjxmFgYAAulysu+2TQg4iIiIiIiIiIiIjShjI5npeXp/NIKB6U95FBDyIiIiIiIiIiIiLKWuzfkRni/T4y6EFERERERERERERERBmBQQ8iIiIiIiIiIiIiIsoIDHoQEREREREREREREVFGYNCDiIiIiIiIiIiIiCiDXXHFFZAkCW1tbV7X/+53v8NJJ52EgoICSJKEKVOmRLQ/q9WK6667DpMnT0ZeXh4mT56MhoYGWK3WuI89Wjl6D4CIiIiIiIiIiIiIiJJr165duOSSS2A2m7F48WJYLBaUlZWF3a67uxunnnoqPvzwQ0ybNg3f+c538M477+CBBx7An//8Z/zjH/9AaWlpEp5BYAx6EBERERERERERERFlmeeeew6yLOPBBx/E8uXLI97u+uuvx4cffoilS5di8+bNyMnxhBl+9KMf4cEHH8QNN9yARx99NFHDDovlrYiIiIiIiIiIiIiIskxXVxcAYNq0aRFv88UXX+C3v/0tcnNzsWHDBjXgAQD33nsvjjjiCPz2t7/FgQMH4j7eSDHoQUREREREREREREQUjsMBHDjguUxRf/zjH3HyyScjPz8fEyZMwGWXXYbPPvvM6z6bNm2CJElobm4GACxatAiSJEGSJGzatCnk/v/yl79AlmWcccYZmDBhgtdteXl5+Pa3vw23242//OUvcX1e0WDQg4iIiIiIiIiIiIgomJ07gaVLgTFjgIkTPZdLlwKvvKL3yLw89NBD+K//+i/s3r0bp512Gqqrq7Ft2zaccsop6O7uVu83Y8YMXH755Zg+fToA4JxzzsHll1+Oyy+/HDNmzAj5GB0dHQCAuXPnBrxduV65nx7Y04OIiIiIiIiIiIiIKJBf/xq45hrAaARk2XOdLAPPPQc88wywYQNw1VW6DhEA9u/fj5UrVyIvLw9//etfUV1dDQCw2+34zne+g+eff16974IFC7BgwQJcccUV2Lt3L2666Sb1/uF8+umnAIDy8vKAtyvXK/fTAzM9iIiIiIiIiIiIiIh87dzpCXgIAbhc3re5XJ7rr746JTI+Nm7ciKGhIVx22WVeAYyCggI8+OCDkCQpLo/T39+v7jeQwsJCr/vpgUEPIiIiIiIiIiIiIiJfv/qVJ8MjFKMRuO++5IwnhJ07dwIALrzwQr/bZs6ciTlz5sTlcYQQABA0iKLcrieWtyIiIiIiIiIiIiIi0nI4gJaWwyWtgnG5gK1bPffPz0/O2AJQmpVPmjQp4O2TJk3C7t27w+7nkUceUQMoirKyMqxfvx4AUFRUBAAYGBgIuL3dbgcAjBkzJrKBJwCDHkREREREREREREREWr294QMeCln23F/HoEe4DIxI7dy5E48++qjXdZMnT1aDHkpQpaurK+D2yvXBgi/JwPJWRERERERERERERERaY8cChginzw0Gz/11dNRRRwEAPvnkk4C3R9pYfNOmTRBCeP3s379fvb2yshIAgmaNKNd/7Wtfi3ToccegBxERERERERERERGRVn4+UFsL5IQplpSTAyxZomuWBwAsWLAAAPCHP/zB77YPPvgA7e3tcXmcc889FwaDAS+//DIOHjzoddvQ0BCee+45GAwGnHfeeXF5vFgw6EFERERERERERERE5OuGGwC3O/R93G7g+uuTM54Q6urqYDKZ8Nhjj+Hll19Wr3c4HGhoaIAcaamuMI488kj893//N5xOJ66++mq4XC71tp/85Cf48ssvcfHFF2PixIlxebxYMOhBRERERERERERERORrwQJgwwZAkvwzPnJyPNdv2ACcfro+49OYNm0a7r77bgwODmLRokU466yzsGzZMsyYMQNvv/02vvWtb8Xtse6//35Mnz4df/zjHzFr1iwsW7YM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sQX/7+d9pq/vtq/fl/z7G188Zfr6qtW/e+aLeHfpGj7QuBl//fmvZ7z+l/97HM/+4Nv4Tx//Zfz7f91T/gGWIN+2lYPNZjPsroL064YgCEUHPLTE4/GUoISRY9ej80S/YcsSBTGZkbSz9UP456vv4KNtN+JXbt4D/+vfxuAn+nBv152Gra8WrcefU0RE69X27TZcuSJg61YZb78dz/8BIiIioipg9LxJLWCmB5mqmLu/q93ffOFPy7q+j7Ztwz9fvYyPtm1LuVudUg1+si9597jWfuq/9S7033qXBSMrXb5tqzZmXzes/kVgS+PmZHbF/MoiQrEIREEAIGDfjk/hwjuTWAwHsn5eFARIsow6uxN7btqFVy79A/bt+BT+8N/9l5T37a/S47nc1uPPKSKi9erLXwaOHwceflioid+ZiIiIiKg0zPRgpgcRERERERERERERUUXTO6/PWyCJiIiIiIiIiIiIiKgmMOhBREREREREREREREQ1gUEPIiIiIiIiIiIiIiKqCQx6EBERERERERERERFRTWDQg4iIiIiIiIiIiIiIagKDHkREREREREREREREVBMY9CAiIiIiIiIiIiIioprAoAcREREREREREREREdUEBj2IiIiIiIiIiIiIiKgmMOhBREREREREREREREQ1gUEPIiIiIiIiIiIiIiKqCQx6EBERERERERERERFRTWDQg4iIiIiIiIiIiIiIagKDHkREREREREREREREVBMY9CAiIiIiIiIiIiIioprAoAcREREREREREREREdUEBj2IiIiIiIiIiIiIiKgmMOhBREREREREREREREQ1gUEPIiIiIiIiIiIiIiKqCQx6EBERERERERERERFRTWDQg4iIiIiIiIiIiIiIagKDHkREREREREREREREVBMY9CAiIiIiIiIiIiIioprAoAcREREREREREREREdUEBj2IiIiIiIiIiIiIiKgmMOhBREREREREREREREQ1gUEPIiIiIiIiIiIiIiKqCQx6EBERERERERERERFRTWDQg4iIiIiIiIiIiIiIagKDHkREREREREREREREVBMY9CAiIiIiIiIiIiIioprAoAcREREREREREREREdUEBj2IiIiIiIiIiIiIiKgmMOhBREREREREREREREQ1gUEPIiIiIiIiIiIiIiKqCXarB2AFWZYBAIuLixaPhIiIiIiIiIiIiIiI8lHm85X5/WzWZdBjaWkJANDR0WHxSIiIiIiIiIiIiIiISK+lpSU0NTVlfV2Q84VFapAkSfjpT3+KxsZGCIJg9XCIympxcREdHR2YmprCxo0brR4OEdUoXmuIqFx4vSGicuH1hojKhdcbIm2yLGNpaQkf/OAHIYrZO3esy0wPURTR3t5u9TCILLVx40b+4CQi0/FaQ0TlwusNEZULrzdEVC683hBlypXhoWAjcyIiIiIiIiIiIiIiqgkMehARERERERERERERUU1g0INonXG5XPjKV74Cl8tl9VCIqIbxWkNE5cLrDRGVC683RFQuvN4QlWZdNjInIiIiIiIiIiIiIqLaw0wPIiIiIiIiIiIiIiKqCQx6EBERERERERERERFRTWDQg4iIiIiIiIiIiIiIagKDHkREREREREREREREVBMY9CAiIiIiIiIiIiIioprAoAdRjQqHw+jq6oIgCJiYmEh57Qc/+AF6enrQ3NwMj8eDffv2ZbxH7fr163jooYewY8cONDQ0YOvWrfgv/+W/YGFhwdyNIKKqYOT1RlneQw89hM2bN8PtdqO3txfT09PmbQARVYVs15pnn30WgiBo/pmZmcm6vPfeew+/8Ru/gS1btsDtduPWW2/FX/7lX5ZhS4io0hl9vQGA7373u9i7dy/cbjeam5uxZ88erKysmLwlRFTpzLjeAIAsy/jFX/xFCIKAv/qrvzJvA4gqFIMeRDXqS1/6Ej74wQ9mPL+0tIS77roLW7duxfe+9z383d/9HTZu3Ii77roL0WhUc1k//elP8dOf/hQnTpzAW2+9hWeffRYvv/wyPv/5z5u9GURUBYy83gDAF7/4Rbz00ks4ffo0/u7v/g7Ly8v4d//u3yEej5u5GURU4bJda/bv349333035c9dd92FX/iFX0Bra2vW5f3Gb/wGLl26hLGxMbz11lu45557sH//fvzjP/6jmZtBRFXA6OvNd7/7Xdx9993Yt28fvv/97+MHP/gBHnzwQYgip2SI1jujrzeKr3/96xAEwYwhE1UHmYhqzne+8x15586d8g9/+EMZgPyP//iPydd+8IMfyADkK1euJJ/73//7f8sA5B//+Me61/HNb35TdjqdcjQaNXLoRFRljL7ezM/Pyw6HQz59+nTyuZ/85CeyKIryyy+/bNp2EFFly3WtSTczMyM7HA75+eefz7lMt9ud8Z5NmzbJTz/9tBFDJqIqZcb15pOf/KT8yCOPGDxSIqp2ZlxvZFmWJyYm5Pb2dvndd9+VAcgvvfSScYMmqhK8rYCoxly9ehVDQ0P48z//czQ0NGS8vmPHDmzevBnPPPMMIpEIVlZW8Mwzz+Dmm2/Ghz70Id3rWVhYwMaNG2G3240cPhFVETOuN2+88Qai0Sj27duXfO6DH/wgfu7nfg4XLlwwbVuIqHLlu9ake/7559HQ0IB//+//fc73/Zt/829w5swZXL9+HZIk4fTp0wiHw9izZ49BIyeiamPG9WZmZgbf+9730Nrait27d6OtrQ2/8Au/gL/7u78zcuhEVGXM+v0mGAziP/yH/4Ann3wSW7ZsMWq4RFWHQQ+iGiLLMv7Tf/pPOHjwIHbt2qX5nsbGRpw7dw6nTp1CfX09NmzYgL/5m7/Bd77zHd0BjNnZWRw7dgxf+MIXjBw+EVURs6437733HpxOJzweT8rzbW1teO+99wzfDiKqbHquNelGRkZw4MAB1NfX53zfmTNnEIvF0NLSApfLhS984Qt46aWXsH37diOGTkRVxqzrzeXLlwEAv/u7v4uhoSG8/PLLuPXWW9HT04Mf/ehHhoydiKqLmb/fHD58GLt370ZfX58RQyWqWgx6EFWB3/3d383awEr58/rrr+Mb3/gGFhcX8eUvfznrslZWVjA4OIif//mfxz/8wz/g7//+73HzzTfjM5/5jK5GeouLi/ilX/olfPSjH8VXvvIVIzeTiCpAJV1v1GRZZk1aohpi5LVG7bvf/S7++Z//WVffsUceeQRzc3P427/9W7z++uv4r//1v+LXfu3X8NZbb5W6eURUQay+3kiSBAD4whe+gIGBAXzsYx/DE088gR07dmBkZKTk7SOiymH19WZsbAyvvfYavv71rxuwNUTVTZBlWbZ6EESU27Vr13Dt2rWc7/nwhz+M/v5+fPvb306ZGIzH47DZbPj1X/91PPfcc3jmmWfw3/7bf8O7776bbJwXiUTg8XjwzDPPoL+/P+s6lKbEDQ0N+Ou//mvU1dUZs4FEVDGsvt689tpr6OnpwfXr11OyPTo7O/Erv/Ir+L3f+z2DtpSIrGTktUbt85//PN588828zcjffvtt3HTTTfinf/on3HzzzcnnP/3pT+Omm27CU089VcRWEVElsvp6884772Dbtm348z//c9x3333J5/fv3w+73Y6/+Iu/KGKriKgSWX29+eIXv4g/+ZM/Sf7fS1muKIr4t//23+LcuXOFbxRRlWIxfqIqsHnzZmzevDnv+/7kT/4Ejz32WPLfP/3pT3HXXXfhzJkz+OQnPwkgUd9RFMWUH67Kv5W7kLQsLi7irrvugsvlwtjYGAMeRDXK6uvNbbfdBofDgVdffRX33nsvAODdd9/FP/3TP+FrX/taKZtGRBXEyGuNYnl5Gd/85jfx1a9+Ne9yg8EgAKRMCgCAzWbL+fsQEVUfq683H/7wh/HBD34Qly5dSnn+X/7lX/CLv/iLOreCiKqB1debhx9+GPfff3/Kc7fccgueeOIJ/PIv/7LOrSCqDQx6ENWQrVu3pvx7w4YNAIDt27ejvb0dAHDnnXfit37rt/DAAw/goYcegiRJOH78OOx2O7q7uwEAP/nJT9DT04Pnn38en/jEJ7C0tIR9+/YhGAzi1KlTWFxcxOLiIgDghhtugM1mK+NWElElMOt609TUhM9//vP4zd/8TbS0tGDTpk04cuQIbrnlFnz6058u70YSkeX0XGsUSo+OX//1X89YTvq1ZufOnbjpppvwhS98ASdOnEBLSwv+6q/+Cq+++ir++q//2rwNIqKKZdb1RhAE/NZv/Ra+8pWvoLOzE11dXXjuuedw8eJF/OVf/qV5G0REFcus682WLVs0m5dv3boVN954o4FbQFT5GPQgWmd27tyJb3/72/i93/s93H777RBFER/72Mfw8ssv4wMf+AAAIBqN4tKlS8m7IN944w1873vfAwDcdNNNKct755138OEPf7is20BE1aGY6w0APPHEE7Db7bj33nuxsrKCnp4ePPvsswywElFOzzzzDO65556U0niK9GuNw+HAd77zHTz88MP45V/+ZSwvL+Omm27Cc889h8985jPlHjoRVZlCrjdAouRMKBTC4cOHcf36dXR2duLVV1/F9u3byzlsIqpChV5viCiBPT2IiIiIiIiIiIiIiKgmiPnfQkREREREREREREREVPkY9CAiIiIiIiIiIiIioprAoAcREREREREREREREdUEBj2IiIiIiIiIiIiIiKgmMOhBREREREREREREREQ1gUEPIiIiIiIiIiIiIiKqCQx6EBERERERERERERFRTWDQg4iIiIiIiIiIiIiIagKDHkREREREREREREREVBMY9CAiIiIiIiIiIiIioprAoAcREREREREREREREdWE/z+8qH+NWlCoSAAAAABJRU5ErkJggg==",
      "text/plain": [
       "<Figure size 1968.5x1968.5 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# plot vazio\n",
    "fig, ax = plt.subplots(figsize = (50/2.54, 50/2.54))\n",
    "\n",
    "# plot mapa do distrito federal\n",
    "mapa.plot(ax=ax, alpha=0.4, color=\"lightgrey\")\n",
    "\n",
    "# plot das entregas\n",
    "geo_deliveries_df.query(\"region == 'df-0'\").plot(ax=ax, markersize=1, color=\"red\", label=\"df-0\")\n",
    "geo_deliveries_df.query(\"region == 'df-1'\").plot(ax=ax, markersize=1, color=\"blue\", label=\"df-1\")\n",
    "geo_deliveries_df.query(\"region == 'df-2'\").plot(ax=ax, markersize=1, color=\"seagreen\", label=\"df-2\")\n",
    "\n",
    "# plot dos hubs\n",
    "geo_hub_df.plot(ax=ax, markersize=30, marker=\"x\", color=\"black\", label=\"hub\")\n",
    "\n",
    "# legenda\n",
    "plt.title(\"Entregas no Distrito Federal por Região\", fontdict={\"fontsize\": 16})\n",
    "lgnd = plt.legend(prop={\"size\": 15})\n",
    "for handle in lgnd.legendHandles:\n",
    "    handle.set_sizes([50])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>region</th>\n",
       "      <th>vehicle_capacity</th>\n",
       "      <th>proportion</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>df-1</td>\n",
       "      <td>180</td>\n",
       "      <td>0.478988</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>df-2</td>\n",
       "      <td>180</td>\n",
       "      <td>0.410783</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>df-0</td>\n",
       "      <td>180</td>\n",
       "      <td>0.110229</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  region  vehicle_capacity  proportion\n",
       "0   df-1               180    0.478988\n",
       "1   df-2               180    0.410783\n",
       "2   df-0               180    0.110229"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data = pd.DataFrame(deliveries_df[['region', 'vehicle_capacity']].value_counts(normalize=True)).reset_index()\n",
    "data.rename(columns={0: \"region_percent\"}, inplace=True)\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [],
   "source": [
    "data = (\n",
    "    deliveries_df[['region', 'vehicle_capacity']]\n",
    "    .value_counts(normalize=True)\n",
    "    .reset_index(name=\"region_percent\")\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [],
   "source": [
    "assert \"region_percent\" in data.columns, \"A coluna region_percent não foi criada!\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [],
   "source": [
    "data = data[['region', 'region_percent']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/tmp/ipykernel_15338/2111424512.py:2: FutureWarning: \n",
      "\n",
      "The `ci` parameter is deprecated. Use `errorbar=None` for the same effect.\n",
      "\n",
      "  grafico = sns.barplot(data=data, x=\"region\", y=\"region_percent\", ci=None, palette=\"pastel\")\n",
      "/tmp/ipykernel_15338/2111424512.py:2: FutureWarning: \n",
      "\n",
      "Passing `palette` without assigning `hue` is deprecated and will be removed in v0.14.0. Assign the `x` variable to `hue` and set `legend=False` for the same effect.\n",
      "\n",
      "  grafico = sns.barplot(data=data, x=\"region\", y=\"region_percent\", ci=None, palette=\"pastel\")\n"
     ]
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAjcAAAHFCAYAAAAOmtghAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8fJSN1AAAACXBIWXMAAA9hAAAPYQGoP6dpAAA8T0lEQVR4nO3dfXzO9f////scM4bJ2kjm5J3pmGYHNhRNiLyxTpzl3UpkRBF9Qm+EnEUTjcJ7ZYnKe40icrLepPQuhCYKybt0poyd0zbZduz1+6Pfjm+HDTs5OObldr1cdqnjuefr9Xq8Ds/tuO/5OvMwDMMQAACASVRxdwEAAACuRLgBAACmQrgBAACmQrgBAACmQrgBAACmQrgBAACmQrgBAACmQrgBAACmQrgBAACmQrjBVeO9995TUFCQ4ys4OFidOnXSM888o1OnTrm7vMvujTfeUGhoqKKiovTzzz9rxIgRWr9+/RXZdlBQkBYvXnxFtlUep06d0uLFi3XkyBF3lwIX69q1qyZNmuTU9sMPP6hbt27q0qWLEhMTtXnzZg0ePNhNFaIy8nR3AUBZRUdHq2nTpvrjjz+UlJSkpUuXau/evdq4caNq1Kjh7vIum2XLlmny5Mk6evSo+vbtqyZNmqhr167uLqtSSElJ0ZIlSxQQEKBbbrnF3eXAhZYsWaJatWo5ta1bt04hISHq2LGjXn75ZWVkZGju3LluqhCVEeEGV52bb75ZNptNktS+fXvZ7XbFxsZq27Ztuu+++0pc5uzZs/L29r6SZV5Sfn6+PDw85OlZuh/DHTt2OP5/6tSpl6usa0JlHA+VyR9//KFq1arJw8OjVP3LOpbLIjg4uFjb+PHjHf8/YMAAl28TVz8OS+Gq17p1a0nSiRMnJEmTJk1SaGiojh49qqFDhyo0NFRDhgyRJGVlZWnGjBm64447FBISom7dumnhwoXKy8tzWmdQUJBmzZqlVatWqUePHgoJCVFERIQ2b95cbPv/+9//NHLkSLVr1042m029e/fWunXrnPrs2bNHQUFBWr9+vebOnas77rhDNptNP//8syTp008/1SOPPKI2bdqoVatW6tWrl5YuXepY/uDBgxo7dqy6du2qli1bqmvXrho3bpx+++23ctVzIdnZ2Zo6dapuu+02hYaGatiwYfrxxx9L7PvTTz9p/Pjx6tChg0JCQtSrVy/Fx8eXajuGYSg+Pl69e/dWy5Yt1a5dOz355JM6fvy4U79Bgwbpnnvu0ddff62HHnpIrVq1Urdu3RQXF6fCwkLHe3v//fdLkp555hnHYcuiw2gXGw95eXmKjY1Vz549FRISovbt2+uZZ55RRkaGUx15eXmaO3euwsPD1apVKw0cOFCHDh0qdsgkIyNDM2bMUEREhEJDQ9WhQwcNHjxYSUlJxd6Dt99+W/fdd59CQ0MVGhqqnj17asGCBRd933799VcFBQXptdde0yuvvKIuXbrIZrOpX79++vzzz4v1T0pK0iOPPKLQ0FC1atVKkZGR+uSTT5z6FB3u3bFjh5555hm1b99erVq1KvYzUeRSY3nXrl165JFHFBYW5thmSbVt27ZN9957r+Pn8M0339TixYsVFBTk1O/89/jcuXOaO3euevfurTZt2ujWW2/VAw88oG3bthXbxrlz5xQTE6OuXbsqJCREd9xxh2bOnKkzZ85c9H3G1Y+ZG1z1in6pXn/99Y62/Px8jRw5UpGRkRo+fLjsdrvOnTunwYMH6/jx4xozZoyCgoKUlJSkuLg4HTlyRHFxcU7r/fjjj7Vnzx49+eST8vb21ttvv61x48bJYrGoZ8+ekv489h8ZGSk/Pz9NmTJFvr6+2rBhgyZNmqS0tDQNHz7caZ0LFixQ69atNXPmTFWpUkV+fn5699139eyzz6pdu3aaOXOm/Pz89OOPP+q7775zLPfbb7/ppptu0t13363rrrtOqampSkhI0P3336/Nmzc79r2s9fyVYRgaNWqU9u/fryeeeEI2m01ffvllict8//33ioyM1I033qiJEyeqbt262rFjh2bPnq3MzEyNHj36ov9m06ZN07p16zRo0CA9/fTTOn36tP71r38pMjJS77//vvz9/R19U1NT9c9//lNRUVEaPXq0PvzwQ8XExKhevXrq06ePWrRooejoaD3zzDMaOXKkunTpIkmqX7/+RcdDYWGhRo0apX379mnYsGEKCwvTb7/9psWLF+vrr7/W2rVrVb16dUl/hqbExEQ9+uijat++vb7//nuNHj1a2dnZTvuVlZUlSRo9erT8/f2Vm5urDz/8UIMGDdIbb7yh2267TZK0efNmzZw5U4MGDdLEiRNVpUoV/fzzz/r+++8v+r4ViY+PV4MGDTR58mQVFhZq2bJlGj58uFauXKnQ0FBJ0t69ezV06FBZrVbNmTNHXl5eSkhI0OOPP64FCxYoIiLCaZ2TJ09Wly5dNG/ePJ09e/aSszAljeX3339fEydOVLdu3fTCCy/I09NTq1ev1rBhw/T666+rQ4cOkv4M82PGjFHbtm310ksvqaCgQMuXL1daWtol9z0vL0+nT5/W0KFDdcMNNyg/P1+7du3SmDFjFB0drT59+kj6f+N59+7dGjFihNq2baujR49q8eLFOnDggFavXi0vL69Svd+4ChnAVWLt2rWG1Wo1Dhw4YOTn5xvZ2dnG9u3bjfbt2xuhoaFGamqqYRiGMXHiRMNqtRpr1qxxWj4hIcGwWq1GYmKiU3tcXJxhtVqNHTt2ONqsVqvRsmVLxzoNwzAKCgqMnj17Gt27d3e0jR071ggJCTFOnDjhtM5HH33UaNWqlXHmzBnDMAxj9+7dhtVqNQYOHOjULzs72wgLCzMefPBBo7CwsNTvRUFBgZGTk2O0bt3aePPNN8tcT0n++9//Glar1Wl9hmEYr7zyimG1Wo1FixY52oYOHWp06tTJ+P333536zpo1y7DZbEZWVtYFt7N//37DarUay5cvd2pPTk42WrZsacybN8/R9vDDDxtWq9X46quvnPpGREQYQ4cOdbz++uuvDavVaqxdu7bY9i40HjZt2mRYrVZjy5YtTu1F64qPjzcMwzC+++47w2q1GvPnzy9x+YkTJ15wXwsKCoz8/HzjkUceMZ544glH+6xZs4y2bdtecLkLOX78uGG1Wo2OHTsaf/zxh6P9999/N2699VZjyJAhjrZ//OMfRocOHYzs7Gyneu655x6jU6dOjvFW9HM1YcKEUtVwobGcm5tr3HrrrcZjjz3m1G6324377rvPuP/++x1t/fv3Nzp37mycO3fO0ZadnW3ceuuthtVqdVr+zjvvLNV7PHnyZKNPnz6O9k8//dSwWq3Ga6+95tR/8+bNhtVqNVavXl2q/cXVicNSuOr84x//UIsWLRQWFqbHHntM/v7+eu2115z+2pekHj16OL3evXu3atSo4Zh1KdKvXz9JKjZ13qFDB6d1WiwWRURE6Oeff9bJkycd6+zQoYNuvPFGp2X79u2rs2fPav/+/U7tf//7351e79+/X9nZ2XrooYcuen5DTk6O5s+fr+7duys4OFjBwcEKDQ1Vbm6ujh075rSPZannr/bs2SNJuvfee53a77nnHqfX586d0+7du9W9e3dVr15dBQUFjq9OnTrp3LlzOnDgwAW3s337dnl4eOi+++5zWtbf31/NmzfX3r17nfrXrVtXLVu2dGoLCgpyHIYsrfPHw/bt21W7dm3deeedTnXccsstqlu3rqOOov/26tWr2PpKmt1ISEhQ3759ZbPZFBwcrBYtWujzzz93+ney2Ww6c+aMxo0bp23bthU7DHYpf//731WtWjXH61q1aunOO+/UF198IbvdrtzcXH311Vfq0aOHatas6ehnsVh033336eTJk/rhhx+KrbOsNfzV/v37lZWVpb59+zq9n4WFhbrjjjt08OBB5ebmKjc3V4cOHdJdd93lNHNSs2bNUp8g/8EHHygyMlKhoaGO93jNmjXFfhak//fzXaRXr16qUaNGiYfKYB4clsJV54UXXlBgYKA8PT3l5+enevXqFevj7e1d7AqLrKws+fv7FwsRfn5+8vT0dBxSKHJ+WPprW1ZWlurXr6+srCzVrVu3WL+ims5f5/l9iz7U/noIpSTjx4/X7t27NWrUKNlsNtWsWVMeHh4aMWKEzp0757SPZannr7KysuTp6SlfX9+L1pyVlaWCggKtXLlSK1euLHFdmZmZF9xOenq6DMPQ7bffXuL3GzVq5PS6Tp06xfp4eXk57fellDQe0tPTdebMGYWEhJS4TNE+FL1n548HT0/PYrWtWLFCc+fOVWRkpP7v//5Pvr6+qlKlil5++WWnMNGnTx/Z7Xa9++67evLJJ1VYWCibzaannnpK4eHhl9yfC43N/Px85ebmKicnR4ZhVGhsXsr5/YsOKT355JMXXOb06dPy8PCQYRjy8/Mr9v2S2s63detWPfXUU+rZs6ceffRR+fv7y2KxKCEhQWvXrnX0KxrPfz1cLUkeHh7y9/e/6M8Crn6EG1x1AgMDHVdLXUhJsyB16tTRV199JcMwnL6fnp6ugoKCYh/qJR3/L2or+lCrU6eOUlNTi/VLSUmRpGLrPL+uol+8RTNBJfn999/1ySefaPTo0RoxYoSjvejcg/P3sSz1nL9sQUGBMjMznfqdv77atWvLYrGod+/eeuihh0pcV8OGDS+4HV9fX3l4eCg+Pr7Ecx4ux3kQJY0HX19f1alTR8uWLStxmaIZj6J/67S0NN1www2O7xcUFBT7gNywYYNuvfVWzZw506k9Jyen2Pr79++v/v37Kzc3V1988YUWL16sxx57TFu2bFFAQMBF9+dCY7Nq1aqqUaOGLBaLqlSpUqGxeSnn9y9a37PPPqtWrVqVuIyfn58KCgrk4eGh9PT0EvfhUjZs2KCGDRvqpZdecqrhzTffdOpXNJ4zMjKcAo5hGEpLS7vk7xBc3TgshWtGhw4dlJubW+yqiqIb4RWd7Fjk888/d/pla7fblZiYqMaNGztmWjp06KDdu3cXu4ng+++/L29vb8eVXBcSGhoqHx8frVq1SoZhlNin6C/d8z/03333Xdnt9mL7WN56ik523bhxo1P7pk2bnF57e3vrtttu0zfffKOgoCDZbLZiXxcLUV26dJFhGDp16lSJy55/tUxpFL03f/zxR6mX6dKli7KyshyzJud/NW3aVJLUrl07SVJiYqLT8lu2bFFBQYFTm4eHR7F/p2+//faih+lq1Kihzp076/HHH1d+fn6pTireunWr08xVdna2tm/frrZt28pisahGjRpq1aqVPvzwQ6f3pLCwUBs2bFD9+vV10003XXI7ZREWFqbatWvr+++/L/H9tNls8vLyUo0aNRQSEqJt27Y5XZGVk5Oj7du3X3I7Hh4eqlq1qlOwSU1N1UcffeTUr+jnecOGDU7tW7ZsUW5ubrGfd5gLMze4ZvTp00fx8fGaOHGifvvtN1mtVu3bt09Lly5V586dix0m8fX11SOPPKJRo0Y5rpb64YcftHDhQkefJ554Qtu3b9fgwYP1xBNP6LrrrtPGjRv1ySef6J///Kd8fHwuWlPNmjU1ceJETZ06VUOGDNE//vEP+fn56ZdfftG3336radOmqVatWmrXrp1ef/11+fr6KiAgQHv37tWaNWtUu3Ztp/VVpJ6OHTuqXbt2mj9/vs6ePauQkBB9+eWXev/994v1nTJlih566CENHDhQDz74oAICApSTk6NffvlFH3/8sd56660LbqdNmzZ64IEHNHnyZB06dEjt2rWTt7e3UlNTtW/fPlmt1gvOCF1I48aNVb16dW3cuFGBgYGqUaOG6tWr5zTTcr67775bGzdu1IgRIzRo0CC1bNlSVatW1cmTJ7Vnzx5169ZN3bt3180336x77rlHK1askMViUfv27fXdd99pxYoV8vHxcfqQ7dKli2JjY7Vo0SK1a9dOP/74o2JjY9WwYUOnIDp16lRVr15dYWFhqlu3rlJTUxUXFycfH59SzShYLBZFRUUpKipKhYWFeu2115Sdna0xY8Y4+owbN05Dhw7V4MGDNXToUFWtWlVvv/22vvvuOy1YsKDMMzWXUrNmTU2dOlWTJk3S6dOn1aNHD/n5+SkjI0PffvutMjIyHDNaTz75pB577DENGzZMjzzyiOx2u15//XXVrFmz2Gzk+bp06aKtW7dqxowZ6tGjh06ePKnY2FjVq1dPP/30k6NfeHi4OnbsqBdffFHZ2dkKCwvT0aNHtWjRIgUHB6t3794u3X9ULoQbXDOqVaumt956SwsXLtSyZcuUmZmpG264QUOHDi3x0uWuXbuqWbNmeumll5ScnKxGjRrpxRdfdLqEtmnTplq1apUWLFigWbNm6Y8//lBgYKCio6OLnch4IQMGDFC9evW0bNky/fOf/5TdblezZs0cl7RKUkxMjObMmaP58+eroKBAYWFhWrFihR577DGndVWknipVquiVV15RdHS0li1bpvz8fIWFhSkuLq7YybTNmjXTe++9p9jYWL300kvKyMiQj4+PmjRpos6dO19yn2fNmqVWrVpp9erVSkhIUGFhoerVq6ewsLBiJw+Xhre3t55//nktWbJEw4YNU35+vkaPHu30YX8+i8WiV155RW+99Zbef/99xcXFyWKxqH79+mrXrp2sVqujb3R0tOrWras1a9bojTfe0C233KKXXnpJjz76qFPAfPzxx3X27FmtWbNGy5YtU7NmzTRjxgxt27bN6UTptm3b6r333tMHH3yg06dPy9fXV23atNELL7xQ7ByRkgwcOFDnzp3T7NmzlZ6erptvvllLly5VmzZtHH1uvfVWvfHGG1q8eLGeeeYZFRYWqnnz5nrllVd05513lvUtLpXevXurQYMGWrZsmaZPn66cnBxdf/31uuWWW9S3b19Hv06dOmnx4sV6+eWX9dRTT6lu3bp68MEHlZKSUmym5Xz9+/dXenq6Vq1apbVr16pRo0YaMWKETp48qSVLljj6eXh4KDY2VosXL9Z7772nV199VXXq1FHv3r01btw4LgM3OQ/jQnPhwDUsKChIAwcO1LRp0674tgcPHqwnn3xSbdu2veLbRul9+eWXevDBB/Xiiy8Wu8Lscvn111/VrVs3TZgwQcOGDbsi27xS8vPz1adPH91www1avny5u8vBVY6ZG6CS2LNnjywWiwzD0JYtWwg3lcjOnTu1f/9+hYSEqFq1ajp69Kji4uL0t7/9rcyXUONPkydPVnh4uOrWrau0tDQlJCTo2LFjmjJlirtLgwkQboBK4t1339V//vMf1atXT//3f//n7nLwF7Vq1dLOnTv11ltvKScnR76+vurUqZPGjRvndL8ZlF5OTo5eeOEFZWRkqGrVqgoODlZcXNwFbxEAlAWHpQAAgKlwKTgAADAVwg0AADAVt4eb+Ph4de3aVTabTf369VNSUtIF++7Zs0dBQUHFvv76PBEAAHBtc+sJxYmJiYqOjtb06dMVFhamVatWafjw4dq8ebMaNGhwweX+85//OD0npjT3hShSWFiogoICValSxeU3sQIAAJeHYRgqLCyUp6enqlS5+NyMW8PNihUr1L9/fw0YMEDSn3c93bFjhxISEjR+/PgLLufn51fszqylVVBQoIMHD5ZrWQAA4F5Fj/K4GLeFm7y8PB0+fNjpQYDSn7fM3r9//0WX7dOnj/Ly8hQYGKiRI0eqffv2pd5uUdoLDg6WxWIpe+EAAOCKs9vt+uabby45ayO5MdxkZmbKbrcXe8S9v79/iU+ylaS6devqueeeU4sWLZSXl6f3339fQ4YM0cqVKx0Pt7uUokNR33zzTcV2AAAAXHGlOaXE7TfxO79IwzAuWHjTpk0dT+qV/nyi8smTJ/X666+XOtwUsdlszNwAAHCVsNvtpT6txG3hxtfXVxaLRWlpaU7t6enp8vf3L/V6WrVqdckHrZXEYrEQbgAAMCG3XQru5eWlFi1aaOfOnU7tu3btUmhoaKnXc+TIEdWtW9fV5QEAgKuUWw9LRUVFacKECQoJCVFoaKhWr16t5ORkRUZGSpJiYmJ06tQpzZs3T5L0xhtvqGHDhmrWrJny8/O1YcMGbdmyRYsXL3bnbgAAgErEreEmIiJCmZmZio2NVUpKiqxWq+Li4hQQECBJSk1NVXJysqN/fn6+XnjhBZ06dUrVq1dXs2bNFBcXp86dO7trFwAAQCVzzT04026368CBA2rdujXn3AAAcJUoy+e32x+/AAAA4EqEGwAAYCqEGwAAYCqEGwAAYCqEGwAAYCqEGwAAYCqEGwAAYCqEGwAAYCqEGwAAYCqEm3K6xm7sjEtgPABA5eHWZ0tdzTw8PLTn2Bn9ftbu7lLgZj7eFt0WWNvdZQAA/n+Emwr4/axdWbkF7i4DAAD8BYelAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAACAqRBuAJMwjEJ3l4BKhjGBa5WnuwsA4BoeHlWU89UWFeZkursUVAJVavqqZqse7i4DcAvCDWAihTmZsp9JdXcZAOBWbj8sFR8fr65du8pms6lfv35KSkoq1XL79u1TcHCwevfufZkrBAAAVxO3hpvExERFR0dr5MiRWr9+vdq0aaPhw4frxIkTF13u999/18SJE9WhQ4crVCkAALhauDXcrFixQv3799eAAQMUGBioKVOmqH79+kpISLjoctOmTdM999yj1q1bX5lCAQDAVcNt4SYvL0+HDx9Wx44dndrDw8O1f//+Cy63du1a/fLLLxo9evTlLhEAAFyF3HZCcWZmpux2u/z8/Jza/f39lZpa8gmRP/30k2JiYhQfHy9Pz4qVbrfbK7S8xWKp0PIwn4qOqYpiTKIk7h6XgKuUZSy7/WopDw8Pp9eGYRRrk/7cqfHjx2vMmDG66aabKrzdgwcPlntZb29vBQcHV7gGmMvRo0d19uxZt2ybMYkLcee4BNzFbeHG19dXFotFaWlpTu3p6eny9/cv1j8nJ0eHDh3SkSNH9Nxzz0mSCgsLZRiGgoOD9frrr5fpBGObzcZfunCpoKAgd5cAFMO4hFnY7fZST0y4Ldx4eXmpRYsW2rlzp7p37+5o37Vrl7p161asf61atbRx40antrffflu7d+/WokWL1LBhwzJt32KxEG7gUownVEaMS1yL3HpYKioqShMmTFBISIhCQ0O1evVqJScnKzIyUpIUExOjU6dOad68eapSpYqsVqvT8n5+fqpWrVqxdgAAcO1ya7iJiIhQZmamYmNjlZKSIqvVqri4OAUEBEiSUlNTlZyc7M4SAQDAVcbDMAzD3UVcSXa7XQcOHFDr1q0rPF277VCmsnILXFQZrlZ1anjqrhBfd5chSfp91yoevwBJkqV2XfncHunuMgCXKcvnt9sfvwAAAOBKhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqhBsAAGAqbg838fHx6tq1q2w2m/r166ekpKQL9k1KSlJkZKRuu+02tWzZUj179tQbb7xx5YoFAACVnqc7N56YmKjo6GhNnz5dYWFhWrVqlYYPH67NmzerQYMGxfrXqFFDDz/8sIKCguTt7a19+/Zp+vTp8vb21gMPPOCGPQAAAJWNW2duVqxYof79+2vAgAEKDAzUlClTVL9+fSUkJJTYPzg4WPfcc49uvvlmNWzYUL1791bHjh0vOtsDAACuLW6bucnLy9Phw4c1YsQIp/bw8HDt37+/VOv45ptvtH//fj311FNl3r7dbi/zMn9lsVgqtDzMp6JjqqIYkyiJu8cl4CplGctuCzeZmZmy2+3y8/Nzavf391dqaupFl+3UqZMyMjJkt9s1evRoDRgwoMzbP3jwYJmXKeLt7a3g4OByLw9zOnr0qM6ePeuWbTMmcSHuHJeAu7j1nBtJ8vDwcHptGEaxtvPFx8crNzdXX331lWJiYtSkSRPdc889ZdquzWbjL124VFBQkLtLAIphXMIs7HZ7qScm3BZufH19ZbFYlJaW5tSenp4uf3//iy7bqFEjSX/+0KalpWnx4sVlDjcWi4VwA5diPKEyYlziWuS2E4q9vLzUokUL7dy506l9165dCg0NLfV6DMNQfn6+q8sDAABXqQrP3BiGIan44aXSiIqK0oQJExQSEqLQ0FCtXr1aycnJioyMlCTFxMTo1KlTmjdvnqQ/D0fdeOONatq0qSRp3759Wr58uR5++OGK7gYAADCJcoeb9evX6/XXX9dPP/0kSfrb3/6mYcOGqU+fPqVeR0REhDIzMxUbG6uUlBRZrVbFxcUpICBAkpSamqrk5GRH/8LCQi1YsEC//vqrLBaLGjdurPHjxzvCEAAAgIdRNPVSBitWrNDLL7+sgQMHKiwsTIZh6Msvv9Tbb7+tp556SkOGDLkMpbqG3W7XgQMH1Lp16wofi952KFNZuQUuqgxXqzo1PHVXiK+7y5Ak/b5rlexnLn61Ia4Nltp15XM7f/jBPMry+V2umZuVK1dqxowZTrM0d911l26++WYtXry4UocbAABgbuU6oTg1NbXEk35DQ0MveY8aAACAy6lc4aZJkyb64IMPirUnJibqb3/7W0VrAgAAKLdyHZYaM2aMxo4dqy+++EJhYWHy8PDQvn37tHv3br300ksuLhEAAKD0yjVz06NHD73zzjvy9fXVRx99pA8//FC+vr5699131b17d1fXCAAAUGrlvhQ8JCREL774oitrAQAAqLAK38Tvjz/+UEGB8+XQtWrVquhqAQAAyqVc4ebs2bOaP3++PvjgA2VlZRX7/pEjRypaFwAAQLmU+pybXr166eWXX5YkzZs3T7t379b06dPl5eWl2bNna8yYMapXr55eeOGFy1YsAADApZQ63CxfvlyJiYmSpO3bt2v69Onq2bOnLBaL2rZtq1GjRmns2LHauHHjZSsWAADgUkodbsaOHauRI0dKkk6fPq2GDRtK+vP8mtOnT0uS2rRpo6SkpMtQJgAAQOmUOtxkZWXpwIEDkqSGDRvqt99+kyQ1a9bMcUO/7du3y8fHx/VVAgAAlFKpw827776rO++8U5LUv39/ffvtt5KkESNG6O2331ZISIiio6M1bNiwy1MpAABAKZT6aikfHx917txZkpwejNm+fXt98MEHOnTokBo3bqzmzZu7vEgAAIDSqvB9biSpQYMGatCggStWBQAAUCHlevzC7Nmz9dZbbxVr//e//605c+ZUuCgAAIDyKle42bJli8LCwoq1h4WF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jElciDvHJeAubgs3vr6+slgsSktLc2pPT0+Xv7//RZdNTEzUlClT9PLLL+v2228v1/ZtNht/6cKlgoKC3F0CUAzjEmZht9tLPTHhtnDj5eWlFi1aaOfOnerevbujfdeuXerWrdsFl9u0aZMmT56sBQsWqEuXLuXevsViIdzApRhPqIwYl7gWufWwVFRUlCZMmKCQkBCFhoZq9erVSk5OVmRkpCQpJiZGp06d0rx58yT9GWwmTpyoyZMnq1WrVo5zc6pXry4fHx+37QcAAKg83BpuIiIilJmZqdjYWKWkpMhqtSouLk4BAQGSpNTUVCUnJzv6r169WgUFBZo1a5ZmzZrlaO/bt6/mzp17xesHAACVj9tPKB44cKAGDhxY4vfODywrV668EiUBAICrWJkevwAAAFDZEW4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAICpEG4AAJdNoWG4uwRUIldqPHheka0AAK5JVTw89NHJz5WVd8bdpcDN6njVVrf6Ha7Itgg3AIDLKivvjNLOZbq7DFxD3H5YKj4+Xl27dpXNZlO/fv2UlJR0wb4pKSkaP368evTooebNm2vOnDlXsFIAAHA1cGu4SUxMVHR0tEaOHKn169erTZs2Gj58uE6cOFFi/7y8PPn6+mrkyJFq3rz5Fa4WAABcDdwablasWKH+/ftrwIABCgwM1JQpU1S/fn0lJCSU2L9hw4aaOnWq+vTpIx8fnytcLQAAuBq47ZybvLw8HT58WCNGjHBqDw8P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jpbdbtf333+vyZMnq23btlqwYIG7ywNwFeOwFAC38fLyUt26dVW/fn117NhRERERTk9JXrt2rXr16iWbzaaePXsqPj7eafkvv/xSvXv3ls1mU79+/bRt2zYFBQXpyJEjkooflsrMzNS4cePUqVMntWrVSvfee682bdrktM68vDzNnj1bHTp0kM1m04MPPqivv/76Mr8TAFyJB2cCqBSOHz+uzz77TJ6ef/5aeuedd7Ro0SJNmzZNt9xyi44cOaJnn31WNWrUUN++fZWdna2RI0eqU6dOiomJ0W+//abnn3/+otvIy8tTixYtNHz4cNWqVUuffPKJJkyYoEaNGqlVq1aSpHnz5mnLli2aO3euAgICtGzZMj366KPaunWr6tSpc7nfBgAuQLgB4DaffPKJQkNDZbfbde7cOUnSM888I0mKjY3VpEmT9Pe//12S1KhRI33//fdavXq1+vbtq40bN0qSZs+erWrVqqlZs2ZKSUnR1KlTL7i9G264QcOGDXO8HjRokD777DP95z//UatWrZSbm6tVq1YpOjpanTt3liQ999xz2rlzp9asWaNHH330srwPAFyLcAPAbW677TbNmDFDZ8+e1Zo1a/Tjjz/q4YcfVkZGhpKTkzVlyhQ9++yzjv4FBQXy8fGRJP34448KCgpStWrVHN+32WwX3Z7dbldcXJwSExOVkpKivLw85eXlydvbW5L0yy+/KD8/X2FhYY5lqlatqpYtW+rYsWOu3HUAlxHhBoDbeHt7q0mTJpKkqVOnatCgQVqyZIkefvhhSX/OmhQdLipSpcqfpwoahuG4Aqq0li9frjfeeEOTJ09WUFCQvL299fzzzys/P9+p3/nrLc+2ALgPJxQDqDRGjx6t5cuXy26364YbbtDx48fVpEkTp69GjRpJkpo2baqjR48qLy/PsfzBgwcvuv59+/apW7du6t27t5o3b65GjRrpp59+cny/cePGqlq1qvbt2+doy8/P16FDhxQYGOjanQVw2TBzA6DSuO2229SsWTMtXbpUY8aM0ezZs1WrVi116tRJeXl5OnTokM6cOaOoqCjde++9eumll/Tss89qxIgROnHihJYvXy6p+MxLkcaNG2vr1q368ssvdd1112nFihVKS0tzBJcaNWrowQcf1Lx583TdddepQYMGWrZsmf744w/df//9V+x9AFAxzNwAqFSioqL0zjvvqGPHjpo9e7bWrVune++9V4MGDdK6devUsGFDSVKtWrX0yiuv6MiRI+rdu7cWLlyoJ554QtKfl5iXZNSoUQoODtawYcM0aNAg+fv766677nLq8/TTT6tHjx6aMGGC+vbtq59//lnLli1z2Y0FAVx+3MQPgGls2LBBkydPVlJSkqpXr+7ucgC4CYelAFy11q9fr4YNG+qGG27Q0aNH9eKLL6pnz54EG+AaR7gBcNVKTU3VokWLlJqaqrp166pnz54aO3asu8sC4GYclgIAAKbCCcUAAMBUCDcAAMBUCDcAAMBUCDcAAMBUCDcAAMBUCDcAAMBUCDcAAMBUCDcAAMBUCDcAAMBU/j/eMESt93u+rAAAAABJRU5ErkJggg==",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "with sns.axes_style('whitegrid'):\n",
    "  grafico = sns.barplot(data=data, x=\"region\", y=\"region_percent\", ci=None, palette=\"pastel\")\n",
    "  grafico.set(title='Proporção de entregas por região', xlabel='Região', ylabel='Proporção');"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "1. As **entregas** estão corretamente alocadas aos seus respectivos **hubs**;\n",
    "1. Os **hubs** das regiões 0 e 2 fazem **entregas** em locais distantes do centro e entre si, o que pode gerar um tempo e preço de entrega maior."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Após essa primeira análise, decidi transformar os dados do JSON para um banco de dados como parte de um processo de ETL "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Extração: Carregando o JSON\n",
    "with open('deliveries.json', 'r') as file:\n",
    "    data = json.load(file)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Transformação: Estruturando os dados em tabelas\n",
    "hubs = []\n",
    "deliveries = []\n",
    "\n",
    "for hub in data:\n",
    "    hubs.append({\n",
    "        \"name\": hub[\"name\"],\n",
    "        \"region\": hub[\"region\"],\n",
    "        \"origin_lng\": hub[\"origin\"][\"lng\"],\n",
    "        \"origin_lat\": hub[\"origin\"][\"lat\"],\n",
    "        \"vehicle_capacity\": hub[\"vehicle_capacity\"],\n",
    "    })\n",
    "    for delivery in hub[\"deliveries\"]:\n",
    "        deliveries.append({\n",
    "            \"hub_name\": hub[\"name\"],\n",
    "            \"delivery_id\": delivery[\"id\"],\n",
    "            \"delivery_lng\": delivery[\"point\"][\"lng\"],\n",
    "            \"delivery_lat\": delivery[\"point\"][\"lat\"],\n",
    "            \"delivery_size\": delivery[\"size\"],\n",
    "        })\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convertendo para DataFrames\n",
    "df_hubs = pd.DataFrame(hubs)\n",
    "df_deliveries = pd.DataFrame(deliveries)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 199 entries, 0 to 198\n",
      "Data columns (total 5 columns):\n",
      " #   Column            Non-Null Count  Dtype  \n",
      "---  ------            --------------  -----  \n",
      " 0   name              199 non-null    object \n",
      " 1   region            199 non-null    object \n",
      " 2   origin_lng        199 non-null    float64\n",
      " 3   origin_lat        199 non-null    float64\n",
      " 4   vehicle_capacity  199 non-null    int64  \n",
      "dtypes: float64(2), int64(1), object(2)\n",
      "memory usage: 7.9+ KB\n"
     ]
    }
   ],
   "source": [
    "df_hubs.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 636149 entries, 0 to 636148\n",
      "Data columns (total 5 columns):\n",
      " #   Column         Non-Null Count   Dtype  \n",
      "---  ------         --------------   -----  \n",
      " 0   hub_name       636149 non-null  object \n",
      " 1   delivery_id    636149 non-null  object \n",
      " 2   delivery_lng   636149 non-null  float64\n",
      " 3   delivery_lat   636149 non-null  float64\n",
      " 4   delivery_size  636149 non-null  int64  \n",
      "dtypes: float64(2), int64(1), object(2)\n",
      "memory usage: 24.3+ MB\n"
     ]
    }
   ],
   "source": [
    "df_deliveries.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "636149"
      ]
     },
     "execution_count": 43,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Carregamento: Salvando os dados em um banco SQLite\n",
    "conn = sqlite3.connect('logistics.db')\n",
    "\n",
    "df_hubs.to_sql('hubs', conn, if_exists='replace', index=False)\n",
    "df_deliveries.to_sql('deliveries', conn, if_exists='replace', index=False)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "           name region  origin_lng  origin_lat  vehicle_capacity\n",
      "0  cvrp-2-df-33   df-2  -48.054989  -15.838145               180\n",
      "1  cvrp-2-df-73   df-2  -48.054989  -15.838145               180\n",
      "2  cvrp-2-df-20   df-2  -48.054989  -15.838145               180\n",
      "3  cvrp-1-df-71   df-1  -47.893662  -15.805118               180\n",
      "4  cvrp-2-df-87   df-2  -48.054989  -15.838145               180\n",
      "       hub_name                       delivery_id  delivery_lng  delivery_lat  \\\n",
      "0  cvrp-2-df-33  313483a19d2f8d65cd5024c8d215cfbd    -48.116189    -15.848929   \n",
      "1  cvrp-2-df-33  320c94b17aa685c939b3f3244c3099de    -48.118195    -15.850772   \n",
      "2  cvrp-2-df-33  3663b42f4b8decb33059febaba46d5c8    -48.112483    -15.847871   \n",
      "3  cvrp-2-df-33   e11ab58363c38d6abc90d5fba87b7d7    -48.118023    -15.846471   \n",
      "4  cvrp-2-df-33  54cb45b7bbbd4e34e7150900f92d7f4b    -48.114898    -15.858055   \n",
      "\n",
      "   delivery_size  \n",
      "0              9  \n",
      "1              2  \n",
      "2              1  \n",
      "3              2  \n",
      "4              7  \n"
     ]
    }
   ],
   "source": [
    "# Verificando os dados salvos\n",
    "print(pd.read_sql(\"SELECT * FROM hubs LIMIT 5;\", conn))\n",
    "print(pd.read_sql(\"SELECT * FROM deliveries LIMIT 5;\", conn))\n",
    "\n",
    "conn.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "           name region  origin_lng  origin_lat  vehicle_capacity\n",
      "0  cvrp-2-df-33   df-2  -48.054989  -15.838145               180\n",
      "1  cvrp-2-df-73   df-2  -48.054989  -15.838145               180\n",
      "2  cvrp-2-df-20   df-2  -48.054989  -15.838145               180\n",
      "3  cvrp-1-df-71   df-1  -47.893662  -15.805118               180\n",
      "4  cvrp-2-df-87   df-2  -48.054989  -15.838145               180\n",
      "       hub_name                       delivery_id  delivery_lng  delivery_lat  \\\n",
      "0  cvrp-2-df-33  313483a19d2f8d65cd5024c8d215cfbd    -48.116189    -15.848929   \n",
      "1  cvrp-2-df-33  320c94b17aa685c939b3f3244c3099de    -48.118195    -15.850772   \n",
      "2  cvrp-2-df-33  3663b42f4b8decb33059febaba46d5c8    -48.112483    -15.847871   \n",
      "3  cvrp-2-df-33   e11ab58363c38d6abc90d5fba87b7d7    -48.118023    -15.846471   \n",
      "4  cvrp-2-df-33  54cb45b7bbbd4e34e7150900f92d7f4b    -48.114898    -15.858055   \n",
      "\n",
      "   delivery_size  \n",
      "0              9  \n",
      "1              2  \n",
      "2              1  \n",
      "3              2  \n",
      "4              7  \n"
     ]
    }
   ],
   "source": [
    "conn = sqlite3.connect('logistics.db')\n",
    "print(pd.read_sql(\"SELECT * FROM hubs LIMIT 5;\", conn))\n",
    "print(pd.read_sql(\"SELECT * FROM deliveries LIMIT 5;\", conn))\n",
    "conn.close()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Próxima análises \n",
    " \n",
    "\n",
    "1. **Otimização de Rotas e Hubs**:  \n",
    "   - Analisar se a redistribuição dos hubs pode reduzir o tempo e custo das entregas.  \n",
    "   - Aplicar algoritmos de roteamento, como o problema do caixeiro-viajante (TSP) ou o algoritmo de Clarke-Wright.  \n",
    "\n",
    "2. **Eficiência Operacional**:  \n",
    "   - Comparar o desempenho entre os hubs (tempo médio de entrega, custo por entrega, etc.).  \n",
    "   - Identificar gargalos ou padrões de atrasos.  \n",
    "\n",
    "3. **Análise Geográfica**:  \n",
    "   - Mapear as entregas para visualizar zonas de alta demanda.  \n",
    "   - Usar clustering (como K-Means) para identificar agrupamentos de entregas e sugerir possíveis novos hubs.  \n",
    "\n",
    "4. **Impacto Financeiro**:  \n",
    "   - Avaliar o custo por quilômetro rodado e sua variação entre os hubs.  \n",
    "   - Estimar o impacto financeiro de uma melhor alocação de rotas e hubs.  \n",
    "\n",
    "5. **Predição e Planejamento**:  \n",
    "   - Construir modelos para prever o tempo de entrega com base na distância, volume de pedidos e localização.  \n",
    "   - Estimar a demanda futura em diferentes regiões usando séries temporais.  \n",
    "\n",
    "6. **Satisfação do Cliente**:  \n",
    "   - Relacionar o tempo de entrega e a distância com reclamações ou devoluções.  \n",
    "   - Identificar padrões em feedbacks para melhorar o serviço.  \n",
    "\n"
   ]
  }
 ],
 "metadata": {
  "colab": {
   "authorship_tag": "ABX9TyO58SjEKvZru6fhTie9JEM/",
   "collapsed_sections": [],
   "name": "module_17_exercise.ipynb",
   "provenance": [],
   "toc_visible": true
  },
  "kernelspec": {
   "display_name": "base",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
