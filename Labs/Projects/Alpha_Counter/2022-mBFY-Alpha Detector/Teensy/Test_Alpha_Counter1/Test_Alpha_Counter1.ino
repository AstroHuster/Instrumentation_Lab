/*
 * Test_Alpha_Counter
 * 
 * Generates pulses to test CircuitPython countio module.
 * Generate an average CPS with pulse interval varying.
 * 
 * ProfHuster@gmail.com
 * 2022-06-07
 * 
 */
const int LED = 13;
bool LEDState = false;

const int PIN  = 10;
const float CPS = 20.0;
const int minPulseInt = 1;
const int maxPulseInt = 10;
const float minPulseInterval_us = \
              1e6 * (2.0 / CPS) / (minPulseInt + maxPulseInt);
float pulseDuration_us = 1000.0;

IntervalTimer tmr;

volatile uint32_t pulses, done = 0;

void pulser() {
  digitalWriteFast(PIN, LOW);
  tmr.end();
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("# TestAlpha_Counter");
  Serial.printf("# Initial pulse length = %f us\n", pulseDuration_us);
  pinMode(PIN, OUTPUT);
  pinMode(LED, OUTPUT);
}

elapsedMillis t;

void loop() {
  static float delay_us = 0;
  if(t > 1000){
    t = 0;
    if(LEDState){
      LEDState = false;
      digitalWrite(LED, LOW);
    } else {
      digitalWrite(LED, HIGH);
      LEDState = true;
    }
  }

  // Check for input 
  if(Serial.available()){
    pulseDuration_us = Serial.readStringUntil('\n').toFloat();
    Serial.printf("# Change pulse length to %f us\n", pulseDuration_us);
  }

  delay_us = random(minPulseInt, maxPulseInt+1) * minPulseInterval_us;
  delayMicroseconds(delay_us);
  digitalWriteFast(PIN, HIGH);
  tmr.begin(pulser, pulseDuration_us);
}
