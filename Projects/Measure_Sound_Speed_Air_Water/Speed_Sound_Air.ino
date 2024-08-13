//Speed of sound in air
#define pin_trigger	8
#define pin_echo	9
#define contrast  	6  \\ LCD contrast pin

#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

float sa = 14.0; // insert the air columm height in "cm"
float t;         
float va;		 

void setup() {
	lcd.begin(16, 2);  
	pinMode(pin_trigger, OUTPUT); 
	pinMode(pin_echo, INPUT); 
	analogWrite(contrast, 110);
	
	lcd.print(" SPEED OF SOUND ");
	lcd.setCursor(0, 1);
	lcd.print("      IN AIR    ");
	delay(2000);
	lcd.clear();
}

void loop() {
	digitalWrite(pin_trigger, LOW);
	delayMicroseconds(2);
	digitalWrite(pin_trigger, HIGH);
	delayMicroseconds(10);
	digitalWrite(pin_trigger, LOW);
	t = pulseIn(pin_echo, HIGH); // t in microseconds
	va = float((2 * sa * 10000.0) / t); // 10000.0 factor converts va value to m/s
	
	lcd.clear();
	lcd.setCursor(0, 0);
	lcd.print("t = "); 
	lcd.print(time ); // print t in microseconds 
	lcd.print("us");
	
	lcd.setCursor(0, 1);
	lcd.print("v_a = ");
	lcd.print(va, 1); // print va in microseconds
	lcd.print(" m/s");
	delay(1000); 	// Wait for 1000 ms
}
