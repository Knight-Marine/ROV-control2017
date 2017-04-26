
char rc;
char opn = 111;
char cls = 99;


void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(8, OUTPUT);
pinMode(7, OUTPUT);
Serial.write(opn);
}

void loop() {
    // put your main code here, to run repeatedly:
   if (Serial.available() > 0) {
         rc = Serial.read();
         if (rc == opn){
           digitalWrite (7, HIGH);
           digitalWrite(8, LOW);
           Serial.println("Opened");
         } else if (rc == cls) {
           digitalWrite(7, LOW);
           digitalWrite(8, HIGH);
           Serial.println("Closed");
         } else {
           digitalWrite(7,LOW);
           digitalWrite(8,LOW);
         }
   } else {
         digitalWrite (7,LOW);
         digitalWrite (8,LOW);
   } delay(200);
}
