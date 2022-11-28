import pandas as pd
import multiprocessing
import nltk
import numpy as np
import re
import time
from multiprocessing import pool
from nltk.corpus import brown

nltk.download('brown')
# Esta función toma cada frase del corpus "brown" y genera una permutación aletoria
# de sus palabras generando como resultado una frase en otro orden distinto al original
# Las frases generadas se devuelven en una lista.
def construye_textos():
    return [" ".join(np.random.permutation(sents)) for sents in brown.sents()]

# Esta función reemplaza las comillas `` por ""
def reemplazar_comillas(texto):
    return texto.apply(lambda text: text.replace("``", '"'))
    
# Esta función convierte todas las palabras a minúsculas
def to_lowercase(texto):
    return texto.apply(lambda text: text.lower())

# Esta función cuenta las palabras de cada fila en el Dataframe
# Para ello, utiliza la librería re de expresiones regulares y la función split
# para separar cada línea en base a cierto patrón. La función re.split() devuelve
# una lista, para obtener el número de palabras usaremos len() sobre dicha lista
def contar_palabras(texto):
    pattern = r"(?:\s+)|(?:,)|(?:\-)"
    return texto.apply(lambda x: len(re.split(pattern, x)))

# Esta función se encarga de procesar el Dataframe en base a las funciones definidas
# previamente
def process_df(df):
    # Generamos una copia del DataFrame para no modificarlo
    res_df = df.copy(deep = True)
    # Reemplazamos las comillas usando reemplazar_comillas
    res_df['text'] = reemplazar_comillas(res_df['text'])
    # Pasamos el texto a minúsculas
    res_df['text'] = to_lowercase(res_df['text'])
    # Construimos una nueva columna en el Dataframe contando el número de palabras
    # de cada línea
    res_df['words'] = contar_palabras(res_df['text'])
    # Vamos a realizar un procesado adicional para textos demasiado largos o demasiado cortos
    # Vamos a elminar los textos demasiado largos > 50 palabras
    long_text = res_df[res_df['words'] > 50]
    res_df.drop(long_text.index, inplace = True)
    # Por otra parte vamos a eliminar los textos demasiado cortos < 50 palabras
    short_text = res_df[res_df['words'] < 10]
    res_df.drop(short_text.index, inplace = True)
    # Hemos terminado el procesado y devolvemos el DatFrame
    return res_df

if __name__ == "__main__":
    # Comenzamos construyendo el DataFrame con el corpus "BROWN"
    # El DataFrame tendrá en principio una única columna 'text' en la que
    # cada fila será una frase del corpus brown permutada aleatoriamente
    print("Generando nuevo DataFrame...\n\n")
    brown_df = pd.DataFrame({'text': construye_textos() + construye_textos() + construye_textos() + construye_textos()})
    print(f"Generado el nuevo Dataframe -> \n {brown_df.head()}\n\n")
    # Comenzamos planteando el procesado del Dataframe en secuencial
    print("Lanzamos 100 ejecuciones secuenciales...")
    arr_sec = np.zeros(shape = (100, 1))
    for i in range(100):
        t0 = time.time()
        processed_df = process_df(brown_df)
        arr_sec[i] = time.time() - t0
    print(f"Tiempo en secuencial -> {arr_sec.mean()}")
    print(f"{processed_df.head()}\n\n")
    # Seguimos planteando el procesado del DataFrame de forma paralelizada
    # Para empezar dividimos el DataFrame en tantos "chunks" como procesadores
    # tenga nuestra máquina. La función multiprocessing.cpu_countS() devuelve el 
    # número de "procesadores lógicos" a los que tiene acceso el intérprete de Python.
    # La máquina en la que se desarrolló este código se contaba con 8 procesadores físicos
    # por lo que tomaremos este número para NUM_CORES con el objetivo de mejorar el 
    # rendimiento del código paralelizado.
    NUM_CORES =  8 #multiprocessing.cpu_count()
    print(f"Iniciando procesado en paralelo usando un Pool de {NUM_CORES} procesos\n\n")
    arr_pool = np.zeros(shape = (100, 1))
    df_chunks = np.array_split(brown_df, NUM_CORES)
    print("Lanzamos 100 ejecuciones en paralelo...")
    for i in range(100):
        # Cada proceso del Pool procesa una de las partes en las que se ha dividido el DataFrame original.
        # Finalmente se usa pd.concat() para ir acumulando los resultados que produce cada proceso
        with multiprocessing.Pool(NUM_CORES) as pool:
            t0 = time.time()
            processed_df_pool = pd.concat(pool.map(process_df, df_chunks), ignore_index = True)
            arr_pool[i] = time.time() - t0
    print(f"Tiempo en paralelo -> {arr_pool.mean()}\n")
    print(f"{processed_df_pool.head()}\n\n")
    # Mostramos algunas frases extraidas aleatoriamente del procesado secuencial
    print("----------------EJEMPLOS DEL PROCESADO SECUENCIAL----------------")
    for i in range(5):
        print(f"{processed_df.iloc[np.random.randint(0, len(processed_df))]['text']}\n")
    # Mostramos algunas frases extraidas aleatoriamente del procesado paralelo
    print("----------------EJEMPLOS DEL PROCESADO PARALELO----------------")
    for i in range(5):
        print(f"{processed_df_pool.iloc[np.random.randint(0, len(processed_df_pool))]['text']}\n")