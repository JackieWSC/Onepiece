/**
 * @file       main.cpp
 * @author     Volodymyr Shymanskyy
 * @license    This project is released under the MIT License (MIT)
 * @copyright  Copyright (c) 2015 Volodymyr Shymanskyy
 * @date       Mar 2015
 * @brief
 * 8b7365146c164bb88648e4569d4dec9a
 */

//#define BLYNK_DEBUG
#define BLYNK_PRINT stdout
#ifdef RASPBERRY
  #include <BlynkApiWiringPi.h>
#else
  #include <BlynkApiLinux.h>
#endif
#include <BlynkSocket.h>
#include <BlynkOptionsParser.h>

static BlynkTransportSocket _blynkTransport;
BlynkSocket Blynk(_blynkTransport);

#include <BlynkWidgets.h>
#include <wiringPi.h>
#include <sys/time.h>
#include "motorCar.h"

unsigned int uptime;            // 1 second intervals
unsigned int pinStatus;         // status of BCM 17
unsigned int lastpinStatus = 0; // to toggle


void myTimerEvent()             // button widget on V0 or direct access gp17 button
{
  Blynk.virtualWrite(V10, uptime/1000);
  pinStatus = digitalRead(17);
  if(pinStatus != lastpinStatus){
    lastpinStatus = pinStatus;
    printf("GP17 pin status: %i\n", pinStatus);
    if(pinStatus == 1){    // this is to synchronise V1 button if gp17 button is pressed
      //Blynk.virtualWrite(V0, 1);
    }
    else{
      //Blynk.virtualWrite(V0, 0);
    }
  }
}

int pulseIn(int pin, int level, int timeout)
{
   struct timeval tn, t0, t1;

   long micros;

   gettimeofday(&t0, NULL);

   micros = 0;

   while (digitalRead(pin) != level)
   {
      gettimeofday(&tn, NULL);

      if (tn.tv_sec > t0.tv_sec) micros = 1000000L; else micros = 0;
      micros += (tn.tv_usec - t0.tv_usec);

      if (micros > timeout) return 0;
   }

   gettimeofday(&t1, NULL);

   while (digitalRead(pin) == level)
   {
      gettimeofday(&tn, NULL);

      if (tn.tv_sec > t0.tv_sec) micros = 1000000L; else micros = 0;
      micros = micros + (tn.tv_usec - t0.tv_usec);

      if (micros > timeout) return 0;
   }

   if (tn.tv_sec > t1.tv_sec) micros = 1000000L; else micros = 0;
   micros = micros + (tn.tv_usec - t1.tv_usec);

   return micros;
}

void distanceSensor()
{
  unsigned int echoPin = 3;
  unsigned int trigPin = 2;

  digitalWrite (trigPin, LOW);

  delayMicroseconds(2);
  digitalWrite (trigPin, HIGH);

  delayMicroseconds(10);
  digitalWrite (trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 1000000);
  int distance = (duration/2) / 29.1;

  //printf("duration: %i\n", duration);

  Blynk.virtualWrite(V9, distance);

  //printf("distance: %i\n", distance);
}

BLYNK_WRITE(V11)
{
  printf("Got a value: %s\n", param[0].asStr());

  if(param[0] == 1){
    printf("V11 turned device ON\n");
    analogWrite(20, 100); //Sets speed variable via PWM 
    digitalWrite (17, HIGH);
    digitalWrite (18, LOW) ;  
  }
  else{
    printf("V11 turned device OFF\n");
    digitalWrite (17, LOW);
    digitalWrite (18, LOW); 
  }
}

BLYNK_WRITE(V12)
{
  printf("Got a value: %s\n", param[0].asStr());

  if(param[0] == 1){
    printf("V12 turned device ON\n");
    digitalWrite (17, LOW);
    digitalWrite (18, HIGH) ;  
  }
  else{
    printf("V12 turned device OFF\n");
    digitalWrite (17, LOW);
    digitalWrite (18, LOW) ; 
  }
}

BLYNK_WRITE(V13)
{
  printf("Got a value: %s\n", param[0].asStr());

  if(param[0] == 1){
    printf("V13 turned device ON\n");
    digitalWrite (23, HIGH);
    digitalWrite (24, LOW) ;  
  }
  else{
    printf("V13 turned device OFF\n");
    digitalWrite (23, LOW);
    digitalWrite (24, LOW) ; 
  }
}

BLYNK_WRITE(V14)
{
  printf("Got a value: %s\n", param[0].asStr());

  if(param[0] == 1){
    printf("V14 turned device ON\n");
    analogWrite(21, 100); //Sets speed variable via PWM
    digitalWrite (23, LOW);
    digitalWrite (24, HIGH) ;  
  }
  else{
    printf("V14 turned device OFF\n");
    digitalWrite (23, LOW);
    digitalWrite (24, LOW) ; 
  }
}

void setup()
{
  printf("Setup - uptime: %i\n", uptime);
  printf("Setup - milis time: %i\n", millis());

  // echoPin and trigPoin for the distance sensor
  unsigned int echoPin = 3;
  unsigned int trigPin = 2;

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}


void loop()
{
  Blynk.run();
  if(millis() >= uptime + 1000){  // 1 second intervals
    myTimerEvent();
    distanceSensor();
    //printf("loop - milis time: %i\n", millis());
    uptime = millis();
  }
}


int main(int argc, char* argv[])
{
    const char *auth, *serv;
    uint16_t port;
    parse_options(argc, argv, auth, serv, port);

    Blynk.begin(auth, serv, port);

    setup();
    while(true) {
        loop();
    }

    return 0;
}

