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

BlynkTimer timer;
unsigned int uptime;            // 1 second intervals
unsigned int pinStatus;         // status of BCM 17
unsigned int lastpinStatus = 0; // to toggle
bool m_isAuto = false;
int m_distance = 0;

enum Action
{
    forward,
    backward,
    left,
    right,
    stop

};


Action m_lastAction = Action::stop;

void Execute(bool leftForward, bool leftBackward, bool rightForward, bool rightBackward)
{
    //analogWrite(21, 255); //Sets speed variable via PWM 
    digitalWrite(17, leftForward);
    digitalWrite(18, leftBackward);
    digitalWrite(23, rightForward);
    digitalWrite(24, rightBackward);
}

void Execute(Action action)
{
    if ( action != m_lastAction )
    {
        switch(action) 
        {
            case Action::left:
                printf("left\n");
                Execute(true, false, true, false); 
                break;
            
            case Action::right: 
                printf("right\n");
                Execute(false, true, false, true); 
                break;
            
            case Action::forward: 
                printf("forward\n");
                Execute(false, true, true, false); 
                break;
            
            case Action::backward: 
                printf("backward\n");
                Execute(true, false, false, true); 
                break;
            
            case Action::stop: 
                printf("stop\n");
                Execute(false, false, false, false); 
                break;

            default: 
                printf("default");
        }

        m_lastAction = action;
    }
}

// This function sends Arduino's up time every second to Virtual Pin (5).
// // In the app, Widget's reading frequency should be set to PUSH. This means
// // that you define how often to send data to Blynk App.
void myTimerEvent()
{
    if (millis() % 10000 == 0)
    {
        printf("My Timer Event 2 - %i (ms)\n", millis());
    }

    Blynk.virtualWrite(V10, millis()/1000);
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

int getDistance()
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

  return distance;

}

int checkDistance(int distance)
{
    if (distance > 100)
    {
        distance = 100;
    }

    return distance;
}

void distanceSensor()
{
    int distance = 0;

    distance = getDistance();

    distance = checkDistance(distance);

    m_distance = distance;

    Blynk.virtualWrite(V9, m_distance);
}

void autoRun()
{
    if (m_isAuto) {
        if (m_distance > 50) {
	    // forward
	    Execute(Action::forward);
	}
	else if (m_distance < 20){
	    // backward
	    Execute(Action::backward);
	}
	else {
	    // if the distance is 20 to 50 then turn left
	    Execute(Action::left);
	}
    }
}

BLYNK_WRITE(V1)
{
    int x = param[0].asInt();
    int y = param[1].asInt();

    //printf("(x,y) = (%i,%i)\n", x, y);

    if (x<50) {
        Execute(Action::left);    
    } else if (x>200) {
        Execute(Action::right);    
    } else if (y>147) {
        Execute(Action::forward);    
    } else if (y<100) {
        Execute(Action::backward);    
    } else { 
        Execute(Action::stop);    
    }
}

BLYNK_WRITE(V2)
{
    int value = param[0].asInt();

    printf("V2 value: %i \n", value);

    m_isAuto = value;

    if (m_isAuto == false)
    {
        Execute(Action::stop);
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
  pinMode(17, OUTPUT);
  pinMode(18, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);
  
  //pinMode(20, OUTPUT);
  //pinMode(21, OUTPUT);

  //analogWrite(20, 200);
  //analogWrite(21, 200);

  timer.setInterval(1000L, myTimerEvent);
  timer.setInterval(1000L, distanceSensor);
}


void loop()
{
  Blynk.run();
  timer.run();
  autoRun();
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

