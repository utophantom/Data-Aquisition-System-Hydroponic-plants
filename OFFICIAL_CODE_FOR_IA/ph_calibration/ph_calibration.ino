
void setup() {
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 5; i++) {
    // read the input on analog pin 0:
    int sensorValue = analogRead(A0);
  
    // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
    float voltage = sensorValue * (5.0 / 1023.0);

    // print out the value you read:

    Serial.println("----- BEGIN ------");
    Serial.println("Trial: ");
    Serial.println(i+1);
    Serial.println(" SensorValue: ");
    Serial.println(sensorValue);
    
    Serial.println("Voltage: ");
    Serial.println(voltage);
    
    Serial.println("----- END ------");
    Serial.println("");
    Serial.println("");   
    delay(1000);
  }
}
