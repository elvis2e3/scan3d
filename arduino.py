import threading
import time
import math
import serial

class Arduino(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.siguiente = 0
        self.fin = False
        self.v = [
            [0.000000, 0.000000, -1.000000],
        ]
        self.verticies = []
        self.ser = serial.Serial('COM14', 9600, timeout=0)
        self.estado = -1;

    def es_fin(self):
        return self.fin

    def set_estado(self, estado):
        self.estado = estado

    def getSiguientePunto(self):
        if len(self.verticies) > self.siguiente:
            self.siguiente += 1
            return self.verticies[self.siguiente-1]
        else:
            return None

    def run(self):
        print "entro al hilo"
        st = -1
        while True:
            if self.estado == 0:
                st = self.estado
            elif self.estado == 1:
                print "estado:", self.estado
                self.ser.write(str(self.estado))
                st = self.estado
                self.estado = -1
            elif self.estado == 2:
                st = self.estado
            if st == 1:
                print ">>>"
                try:
                    dato = self.ser.readline()
                    datos = dato.split(" ")
                    if len(datos) > 1:
                        datos = map(float, datos[0:-1])
                        if datos[0] < 0:
                            pass
                            #self.fin = True
                            #break
                        x = datos[0] * math.cos(math.radians(datos[2]))
                        y = datos[0] * math.sin(math.radians(datos[2]))
                        z = datos[1]
                        self.verticies.append([x, z, y])
                        print x, y, z
                    time.sleep(1)
                except self.ser.SerialTimeoutException:
                    print "datos incorrectos"
        print "fin del hilo"
