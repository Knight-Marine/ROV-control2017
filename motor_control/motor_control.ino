#include <Servo.h>
#define INPUT_SIZE 30

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

char messageFromPC[32] = {0};
int integerFromPC = 0;
float floatFromPC = 0.0;

Servo thrusterOne;
Servo thrusterTwo;
Servo thrusterThree;
Servo thrusterFour;

int thrustOne_val;
int thrustTwo_val;
int thrustThree_val;
int thrustFour_val;

// the setup routine runs once when you press reset:
void setup() {
  
  Serial.begin(9600);
  Serial.println("serial initalized....");
  
  //attach Servos to pins
  thrusterOne.attach(11);
  thrusterTwo.attach(10);
  thrusterThree.attach(6);
  thrusterFour.attach(5);
  
  delay(5000); //wait for ESCs to boot
  
  thrusterOne.writeMicroseconds(1500);
  thrusterTwo.writeMicroseconds(1500);
  thrusterThree.writeMicroseconds(1500);
  thrusterFour.writeMicroseconds(1500);
  
  Serial.println("Ready");
}

// the loop routine runs over and over again forever:
void loop() {
  
  rec_Packet();
  if (newData == true) {
    parseData();
    //showParsedData();
    setMotors();
    newData = false;
  }
  
}

void rec_Packet () {
  static boolean recInProgress = false;
  static byte ndx = 0;
  char startMarker = '[';
  char endMarker = ']';
  char rc;

  if (Serial.available() > 0) {
    while (Serial.available() > 0 && newData == false) {
      rc = Serial.read();

      if (recInProgress == true) {
        if (rc != endMarker) {
          receivedChars [ndx] = rc;
          ndx++;
          if (ndx >= numChars) {
            ndx = numChars - 1;
          }
        }
        else {
          receivedChars [ndx] = '\0';
          recInProgress = false;
          ndx = 0;
          newData = true;
        }
      }

      else if (rc == startMarker) {
        recInProgress = true;
      }
    }
  }
}

void parseData() {
    
    
    char * strtokIndx;

    strtokIndx = strtok(receivedChars, ",");
    thrustOne_val = atoi(strtokIndx);

    strtokIndx = strtok(NULL, ",");
    thrustTwo_val = atoi(strtokIndx);

    strtokIndx = strtok(NULL, ",");
    thrustThree_val = atoi(strtokIndx);

    strtokIndx = strtok(NULL, ",");
    thrustFour_val = atoi(strtokIndx);
    
  }
    
  void showParsedData () {
     Serial.println ("-------------------------------");
      Serial.print("MotorOne ");
      if (1199 < thrustOne_val < 1801) {
        Serial.print("check ");
        thrusterOne.writeMicroseconds(thrustOne_val);
      } else { Serial.println("ERROR");
      }
      Serial.println(thrustOne_val);

      
      Serial.print("MotorTwo ");
       if (1199 < thrustTwo_val < 1801) {
        thrusterTwo.writeMicroseconds(thrustTwo_val);
      } else { Serial.println("ERROR");
      }
      Serial.println(thrustTwo_val);

      
      Serial.print("MotorThree ");
       if (1199 < thrustThree_val < 1801) {
        thrusterThree.writeMicroseconds(thrustThree_val);
      } else { Serial.println("ERROR");
      }
      Serial.println(thrustThree_val);

      
      Serial.print("MotorFour ");
       if (1199 < thrustFour_val < 1801) {
        thrusterFour.writeMicroseconds(thrustFour_val);
      } else { Serial.println("ERROR");
      }
      Serial.println(thrustFour_val);

      
  }

  void setMotors() {
    thrusterOne.writeMicroseconds(thrustOne_val);
    thrusterTwo.writeMicroseconds(thrustTwo_val);
    thrusterThree.writeMicroseconds(thrustThree_val);
    thrusterFour.writeMicroseconds(thrustFour_val);
  }
      
  
