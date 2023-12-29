#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_INA219.h>

#define RPM_PIN 4
Adafruit_INA219 ina219_gen;
Adafruit_INA219 ina219_buck(0x41);

float current_gen = 0.00, voltage_gen = 0.00;
float current_buck = 0.00, voltage_buck = 0.00, power_buck = 0.00;

float rpm_gen = 0.00;
unsigned long rpm_t0 = 0; 
unsigned long rpm_td = 0;

unsigned long delay_t0 = 0, delay_td = 0;

void send_vals_to_uart()
{
    // Packet format will be XXXXX<val0>,<val1>,<val2>,<val3>XXXXX
    Serial.print("XXXXX");
    Serial.print(current_gen, 4);
    Serial.print(",");
    Serial.print(voltage_gen, 4);
    Serial.print(",");
    Serial.print(current_buck, 4);
    Serial.print(",");
    Serial.print(voltage_buck, 4);
    Serial.print(",");
    Serial.print(power_buck, 4);
    Serial.print(",");
    Serial.print(rpm_gen, 4);
    Serial.println("OOOOO");
}

void setup() 
{
    ina219_gen.begin();
    ina219_buck.begin();

    pinMode(RPM_PIN, INPUT);
    Serial.begin(115200);

    delay_t0 = micros();
    delay_td = 0;
}

void loop()
{
    delay_td = micros() - delay_t0;

    if(!digitalRead(RPM_PIN))
    {
        rpm_td = micros() - rpm_t0;
        if(rpm_td >= 1000)
            rpm_gen = (1000000.0/(float)(rpm_td))*60.0;

        rpm_t0 = micros();
        rpm_td = 0;
    }
    
    if(delay_td >= 1000000)
    {
        current_gen = ina219_gen.getCurrent_mA();
        voltage_gen = ina219_gen.getBusVoltage_V();
        current_buck = ina219_buck.getCurrent_mA();
        voltage_buck = ina219_buck.getBusVoltage_V();
        power_buck = current_buck >= 0.0 ? voltage_buck * current_buck: 0.0;
        
        send_vals_to_uart();
        
        rpm_gen = 0.00;
        delay_t0 = micros();
        delay_td = 0;
    }
}
