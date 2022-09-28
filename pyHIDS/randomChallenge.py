from copyreg import pickle
import random
import time
import pickle
import os

import conf




def log(message, display=False):
    """
    Devuelve por consola y escribe el log en el log file.
    """
    
    if display:
        print(message)
    try:
        log_file.write(message+"\n")
    except Exception as e:
        print(e)

def search_files(motif, root_path):
    """
    Return a list of files.

    Search fo files containing 'motif' that
    aren't symbolic links.
    """
    result = []
    #Realiza una revisión en profundidad del contenido de la base de ficheros. Todos estos y el contenido de las subcarpetas
    w = os.walk(root_path)
    import re
    for (path, dirs, files) in w:
        for f in files:
            if re.compile(motif).search(f):
                # if not a symbolic link
                if not os.path.islink(os.path.join(path, f)):
                    result.append(os.path.join(path, f))
    return result

def detectionNewFiles():
    res = []
    #Recogemos todos los ficheros que han sido añadidos al conjunto de ficheros global (ficheros)
    for rules in conf.FOLDER_FILES:
        new_files = search_files(rules[0], rules[1])

    if os.path.exists(conf.BASE_PATH):
        with open(conf.BASE_PATH,"rb") as r:
            older_database = pickle.load(r)
        for file in new_files:
            if file not in list(older_database.keys()):
                res.append(file)
    return res


def challenge():
    #Recogemos el tiempo actual
    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

    #Abrimos el fichero donde almacenamos la lista de files que han sido modificados en la ultima revison.
    with open(conf.MOD_PATH, "rb") as f:
        modified_files = pickle.load(f)

    #Recogemos el conjunto de ficheros que han sido añadidos al conjunto total de documentos (ficheros)
    new_files = detectionNewFiles()

    #Numeros aleatorios para la operacion de challenge
    numero1 = random.randint(0,10)
    numero2 = random.randint(0,10)
    #Error de autentificacion
    error_auth = 0
    #Numero random para establecer la probabilidad de operacion
    x = random.random()

    log(local_time + " Authentication challenge Starting")
    if x>0.5:
        res = numero1+numero2
        resP = int(input("Resuelve "+ str(numero1) +" + "+str(numero2)+": "))
        if res==resP:
            print('Eres humano!')
            exec(open(os.path.join(conf.PATH,"genBD.py")).read())
        else:
            print('Eres un robot!')
            globals()['humano'] = False
            
            if new_files:
                for new_file in new_files:
                    message = local_time + " [error_auth] "  + new_file + " se ha intentado agregar a la base de datos"
                    log(message,True)
                    error_auth = error_auth + 1
            if modified_files:
                for modified_file in modified_files:
                    message = local_time + " [error_auth] "  + modified_file + " se ha intentado modificar"
                    log(message, True)
                    error_auth = error_auth + 1
        
    else:
        res = numero1-numero2
        resP = int(input("Resuelve "+ str(numero1) +" - "+str(numero2)+": "))
        if res==resP:
            print("¡Eres humano!")
            exec(open(os.path.join(conf.PATH,"genBD.py")).read())
        else:
            print("¡Eres un robot!")
            globals()['humano'] = False

            if new_files:
                for new_file in new_files:
                    message = local_time + " [error_auth] "  + new_file + " se ha intentado agregar a la base de datos"
                    log(message,True)
                    error_auth = error_auth + 1
            if modified_files:
                for modified_file in modified_files:
                    message = local_time + " [error_auth] "  + modified_file + " se ha intentado modificar"
                    log(message, True)
                    error_auth = error_auth + 1

    log(local_time + " Auth_Error(s) : " + str(error_auth))
    log(local_time + " Authentication challenge Finished")

if __name__ == "__main__":

    humano = True 
    log_file = None
    try:
        log_file = open(conf.LOGS, "a")
    except Exception as e:
        print("Algo no esta funcionando como debería al abrir el log: " + str(e))
        exit(0)

    print("¿Eres humano? \nDebes resolver la siguiente prueba: ")
    challenge()
    

    if log_file is not None:
        log_file.close()
    

    

