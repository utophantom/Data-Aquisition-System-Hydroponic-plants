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
  lcd.print("Moist:");  // print characters that will always remain on the LCD
}

void loop() {
  lcd.setCursor(7, 0);  //delete all old value
  lcd.print("     ");   //delete all old value
  lcd.setCursor(7, 1);  //delete all old value
  lcd.print("     ");   //delete all old value
  
  ph_process();
  temperature_process();
  moisture_process();
  
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
    total_ph_Value += ph_analog_Value;
    delay(50); 
  }   
  
  float average_ph_Value = ((total_ph_Value * 5.0) / 1023) / 10 ; // change to Voltage value
  float ph_Value = -5.4945 * average_ph_Value + 28.67 ; // change to pH scale

  lcd.setCursor(7, 0); // print to the LCD
  lcd.print(ph_Value);

  x = String(ph_Value);
  total_ph_Value = 0;
}

/////////////////////////// Temperature reading ////////////////////////////////////

void temperature_process(void) {
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  float celsius, fahrenheit;

  if ( !ds.search(addr)) {
    Serial.println("No more addresses.");
    Serial.println();
    ds.reset_search();
    delay(250);
    return;
  }

  if (OneWire::crc8(addr, 7) != addr[7]) {
      Serial.println("CRC is not valid!");
      return;
  }
  Serial.println();

  // the first ROM byte indicates which chip
  switch (addr[0]) {
    case 0x10:
      Serial.println("  Chip = DS18S20");  // or old DS1820
      type_s = 1;
      break;
    case 0x28:
      Serial.println("  Chip = DS18B20");
      type_s = 0;
      break;
    case 0x22:
      Serial.println("  Chip = DS1822");
      type_s = 0;
      break;
    default:
      Serial.println("Device is not a DS18x20 family device.");
      return;
  }

  ds.reset();
  ds.select(addr);
  ds.write(0x44);        // start conversion, use ds.write(0x44,1) with parasite power on at the end

  delay(1000);     // maybe 750ms is enough, maybe not
  // we might do a ds.depower() here, but the reset will take care of it.

  present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE);         // Read Scratchpad

  for ( i = 0; i < 9; i++) {           // we need 9 bytes
    data[i] = ds.read();
  }

  // Convert the data to actual temperature
  // because the result is a 16 bit signed integer, it should
  // be stored to an "int16_t" type, which is always 16 bits
  // even when compiled on a 32 bit processor.
  int16_t raw = (data[1] << 8) | data[0];
  if (type_s) {
    raw = raw << 3; // 9 bit resolution default
    if (data[7] == 0x10) {
      // "count remain" gives full 12 bit resolution
      raw = (raw & 0xFFF0) + 12 - data[6];
    }
  } 
  else {
    byte cfg = (data[4] & 0x60);
    // at lower res, the low bits are undefined, so let's zero them
    if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
    else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
    else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
    //// default is 12 bit resolution, 750 ms conversion time
  }
  celsius = (float)raw / 16.0;
  y = String(celsius);
}

///////////////////////// Moisture reading //////////////////////////////////////////

void moisture_process() {
  float total_moisture_Value = 0;
  for (int i = 0; i < 10; i++) {  // Loop 10 times
    float moisture_analog;
    float moisture_percentage;

    moisture_analog = analogRead(A1); // Input analog reading
    moisture_percentage = (100 - ((moisture_analog/1023.00) * 100 ));  // Convert into percentage value
    Serial.print("Moist_analog: ");
    Serial.print(moisture_analog);
    total_moisture_Value += moisture_percentage ;  // Add to total sum
  }
  
  float moisture_Value = total_moisture_Value / 10 ;

  lcd.setCursor(7, 1);
  lcd.print(moisture_Value);
  z = String(moisture_Value);
}
