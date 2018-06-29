 // Incluímos la librería para poder utilizarla
#include <Stepper.h>
#include <NewPing.h>
 
// Esto es el número de pasos en un minuto
#define STEPS 4096 
// Número de pasos que queremos que de
#define NUMSTEPS 100

//ultrasonido
#define TRIGGER_PIN 4
#define ECHO_PIN 3
#define MAX_DISTANCE 15
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

// Motor A Derecho
int ENA = 5;
int IN3 = 7;
int IN4 = 6;

int v=255;
int led = 12;
// Constructor, pasamos STEPS y los pines donde tengamos conectado el motor
Stepper stepper(STEPS, 8, 9, 10, 11);
 
void setup() {
  // Asignamos la velocidad en RPM (Revoluciones por Minuto)
  stepper.setSpeed(5);
  pinMode (13, OUTPUT);
  pinMode (ENA, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN4, OUTPUT);
  pinMode (led, OUTPUT);
  Serial.begin(9600);
}

void arriba (){
 //Direccion motor A
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENA, v); //Velocidad motor A
}

void abajo (){
 //Direccion motor A
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENA, v); //Velocidad motor A
}
void parar (){
 //Direccion motor A
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, LOW);
 analogWrite (ENA, 0); //Velocidad motor A
}

int giro=0;
int punto=0;
int grados = 0;
int gintervalo = 9;
float z = 0;
char s = 0;
int estado = 0;
void loop() {
  
  if(Serial.available() > 0){
    s = Serial.read();
    //Serial.println(s);
    if(s == '0'){        //punto inicial
      
    }else if(s == '1'){  //iniciar scaneo      
       estado = 1; 
    }else if(s == '2'){  //parar escaneo
      estado = 0;
    }
  }
  
  if(estado == 1){
    if(giro<STEPS/2){
            stepper.step(1);
            if(punto==50){
                float uS = sonar.ping_median();
                Serial.print(13-(uS/US_ROUNDTRIP_CM));
                Serial.print(" ");
                Serial.print(z);
                Serial.print(" ");
                Serial.print(grados);
                Serial.println(" ");
                grados += gintervalo;
                punto=0;
            }
       punto++;
       delay(10);
       giro++;
       //digitalWrite(13,HIGH);
       }
       if(giro == STEPS/2){
           digitalWrite(led,LOW);
           delay(1000);
           grados = 0;
           arriba ();
           z += 0.5;
           delay (500);
           parar();
           giro=0;
       }  
       digitalWrite(led,HIGH);
  }
 
  //float uS = sonar.ping_median();
  //Serial.println(uS/US_ROUNDTRIP_CM);
  //arriba();
  //Serial.println(">>>");
  //delay(100);
  //parar();
  //delay(2000);
}
