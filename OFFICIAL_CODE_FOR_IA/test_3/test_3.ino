// Include the library code and declare variables 

#include <LiquidCrystal.h>
LiquidCrystal lcd(7, 8, 9, 10, 11, 12); // initialize the library with the numbers of the interface pins

#include <OneWire.h>
OneWire ds(2);  // on pin 2 (a 4.7K resistor is necessary)

String x, y, z;
String out_data;

//////////////////////////////////// VOID SET UP & LOOP ///////////////////////////
void setup() {
  Serial.begin(9600); //serial begin
  lcd.begin(16, 2); // set up the LCD's number of columns and rows:
  lcd.print("Hello, Mr.Ebesol!"); // Print a message to the LCD.
  delay(5000);
  lcd.clear();  // clear the beginning/introduction screen
  lcd.setCursor(0, 0);
  lcd.print("pH:");
  lcd.setCursor(0, 1);
  lcd.print("Temp:");  // print characters that will always remain on the LCD
}

void loop() {
  lcd.setCursor(7, 0);  //delete all old value
  lcd.print("     ");   //delete all old value
  lcd.setCursor(7, 1);  //delete all old value
  lcd.print("     ");   //delete all old value
  
  ph_process();
//  temperature_process();
//  moisture_process();
  
  out_data = x + "," + y + "," + z;
  Serial.print(out_data); // Print a string which contains all three sensors data
  
  String x, y, z;
  String out_data;

  delay(1000);
}

//////////////////////////// pH reading ////////////////////////////////////

void ph_process() {
  float total_ph_Value = 0;
  for (int i = 0; i < 10; i++) {  // Loop 10 times
    float ph_analog_Value = analogRead(A0); //buf analog data from sensor into array
    Serial.print("Analog: ");
    Serial.print(ph_analog_Value);
    Serial.print(" ");

  
    total_ph_Value += ph_analog_Value;
    Serial.print("Total: ");
    Serial.print(total_ph_Value);
    delay(50); 
  }   
  
  float average_ph_Value = ((total_ph_Value * 5.0) / 1024) / 10 ; // change to Voltage value
  Serial.print("Average: ");
  Serial.print(average_ph_Value);
  float ph_Value = -5.70 * average_ph_Value + 15.34 ; // change to pH scale

//  Serial.print("phValue : ");
//  Serial.print(phValue);
  lcd.setCursor(7, 0); // print to the LCD
  lcd.print(ph_Value);

  x = String(ph_Value);

  total_ph_Value = 0;
}
