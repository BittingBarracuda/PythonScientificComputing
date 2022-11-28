import threading
import time
import random

class Barberia:
    def __init__(self, num_sillas = 3):
        ### Inicialización de mecanismos y variables de control para clientes y acceso a la sala
        # 1.- Control de entrada a la sala
        # Para este mecanismo de control vamos a utilizar un Semaphore inicializado
        # con value = num_sillas. El parámetro num_sillas nos permite controlar el número de "sillas"
        # de las que disponemos, es decir, cuantos clientes pueden esperar dentro de la barbería
        self.espera_sala = threading.Semaphore(num_sillas)
        # 2.- Control del número de clientes en sala
        # Usaremos la lista clientes para almacenar los hilos que tenemos esperando dentro de la barbería
        # El objetivo de esta lista es imponer una política FIFO sobre los clientes esperando. En otras palabras,
        # el barbero SIEMPRE atenderá al cliente que lleva más tiempo esperando (el que entra antes) y, de esta forma,
        # evitamos problemas de inanición de hilos tan característicos de la programación concurrente.
        self.num_sillas = num_sillas
        self.clientes = []
        # 3.- Exclusión mútua para modificación de variables de control
        # Utilizaremos un Lock que cada hilo podrá adquirir para modificar la variable (lista)
        # clientes sin producir condiciones de carrera.
        self.exclusion_sala = threading.Lock()


        ### Incialización de mecanismos y variables de control para el barbero
        # 1 .- Control de acceso al sillón 
        # Lo inicializaremos como un Condition(). De esta forma, si el barbero está ocupado cortando el pelo
        # los hilos quedarán a la espera en esta condición. Cuando el barbero termine usaremos
        # un mecanismo de notificación para, en caso de que hayan clientes a la espera, pase alguno
        # de ellos. 
        self.sillon = threading.Condition()
        # 2.- Control para poner el barbero a dormir y ser despertado
        self.dormir = threading.Condition()


    def actividad_barbero(self):
            while True:
                # En primer lugar el barbero comprueba si hay clientes y debe despertar
                self.exclusion_sala.acquire()
                with self.dormir:
                    if len(self.clientes) == 0:
                        print(f"{threading.current_thread().name} no tiene clientes y pasa a dormir.\n")
                        self.exclusion_sala.release()
                        self.dormir.wait()
                    else:
                        print(f"{threading.current_thread().name} tiene trabajo\n")
                        self.exclusion_sala.release()
                # Si llegamos a esta región del código el barbero está despierto y debe comenzar
                # a atender a los clientes. Como explicábamos en el constructor, la idea es implementar
                # una política FIFO de atención a los clientes. Para ello, vamos a tomar la lista de clientes
                # y atender al cliente en la posición 0 de la lista. Eliminaremos ese elemento de la lista
                # para indicar que ya ha sido atendido.
                self.exclusion_sala.acquire()
                cliente_actual = self.clientes.pop(0)
                self.exclusion_sala.release()
                print(f"{threading.current_thread().name} pasa a atender a {cliente_actual.name}\n")
                time.sleep(5)
                print(f"{threading.current_thread().name} termina de atender a {cliente_actual.name}\n")
                # Una vez el cliente ha sido atendido, el barbero dará una notificación sobre sillon
                # para que el cliente atendido notifique de su salidad de la barbería y libere el semáforo de espera
                with self.sillon:
                    self.sillon.notify_all()       
    
    def actividad_cliente(self):
        print(f"El cliente {threading.current_thread().name} llega a la barbería\n")
        # El cliente llega y comprueba si puede sentarse a esperar en alguna silla
        # Opción 1.- Todas las sillas están ocupadas y el cliente espera "fuera" de la barbería
        # Opción 2.- Hay sillas libres y el cliente se sienta a esperar
        self.espera_sala.acquire()
        # Si llegamos a esta región del código habían sillas libres y el cliente se sienta a esperar.
        # Para simbolizar esto añadimos el hilo actual a la lista de clientes.
        print(f"El cliente {threading.current_thread().name} se sienta a esperar su turno\n")
        self.exclusion_sala.acquire()
        self.clientes.append(threading.current_thread())
        self.exclusion_sala.release()
        # Notificamos al barbero para despertarlo en caso de que esté dormido
        with self.dormir:
            self.dormir.notify()
        # Una vez notificado, el barbero debería despertar y comenzar a atender a los clientes
        # Se atenderá por orden FIFO por lo que los clientes que están sentados deberán esperar 
        # a que sea su turno. Cuando el barbero libere el sillón se lanzará una notificación y
        # el hilo que haya sido atendido saldrá del bucle while para abandonar la barbería
        while threading.current_thread() in self.clientes:
            with self.sillon:
                self.sillon.wait()
        # El cliente que abandone la barbería liberará el Semaphore para que otros puedan entrar.
        self.espera_sala.release()
        print(f"El cliente {threading.current_thread().name} sale de la barbería\n")       
        
if __name__ == "__main__":
    # Incializamos la barbería con 3 sillas para la espera
    barberia = Barberia(3)
    # Creamos el hilo que representa al barbero
    barbero = threading.Thread(target = barberia.actividad_barbero, name = 'Barbero')
    cli = []
    # Creamos los hilos de los clientes
    names = ['Harry Potter', 'Ragnar', 'Walter White', 'Voldemort', 'Frodo', 'Han Solo']
    for name in names:
        cli.append(threading.Thread(target = barberia.actividad_cliente, name = name))
    
    # Comenzamos los hilos dejando una pausa para que el barbero comience durmiendo
    barbero.start()
    time.sleep(1)
    # Vamos a introducir cierto retardo en la llegada de los clientes para evitar que lleguen
    # al mismo tiempo
    for client in cli:
        client.start()
        time.sleep(random.randint(2, 8))
    # Esperamos a que terminen todos los hilos
    barbero.join()
    for client in cli:
        client.join()


                
