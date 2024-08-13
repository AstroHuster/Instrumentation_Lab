// Speed of sound in water
#define pin_trigger        8 
#define pin_echo 	9 
#define contraste 	6
#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

float sa = 343.0;    // speed fo sound in air
float sa = 7.0;     // insert the air columm height in "cm"
float sw = 30.0;    // insert the water columm height in "cm"
float t;
float vw,va;

void setup() {
	lcd.begin(16, 2);
	pinMode(pin_trigger, OUTPUT);
	pinMode(pin_echo, INPUT);    
	analogWrite(contraste, 110);
	
	lcd.print(" SPEED OF SOUND ");
	lcd.setCursor(0, 1);
	lcd.print("    IN WATER    ");
	delay(2000);
	lcd.clear();
}

void loop()
{
	digitalWrite(pin_trigger, LOW);
	delayMicroseconds(2);
	digitalWrite(pin_trigger, HIGH);
	delayMicroseconds(10);
	digitalWrite(pin_trigger, LOW);
	t = pulseIn(pin_echo, HIGH);     // time in us
	vw = 2. * sa * va / ((va * t * 0.0001) - (2. * sa)); // 0.0001 factor converts va value to m/s
	lcd.clear();
	lcd.setCursor(0, 0);
	lcd.print("t= ");
	lcd.print(t);
	lcd.print(" us");
	
	lcd.setCursor(0, 1);
	lcd.print("v_w= ");
	lcd.print(vw, 1);
	lcd.print(" m/s");
	delay(1000);
}
