/**
 * @file       motorCar.cpp
 * @author     Jackie Wong
 * @license    This project is released under the MIT License (MIT)
 * @copyright  Copyright (c) 2017 Volodymyr Shymanskyy
 * @date       Dec 2017
 * @brief      class to control motor car
 */
#include "motorCar.h"
#include <wiringPi.h>

 void MotorCar::forward() {
    //left
    digitalWrite (17, HIGH);
    digitalWrite (18, LOW) ;  

    //right
    digitalWrite (23, LOW);
    digitalWrite (24, HIGH) ;  
 }