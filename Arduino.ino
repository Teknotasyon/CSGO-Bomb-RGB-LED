
int displayAnything = 0;

int mycounter = 0;
//Time that the timer started at
long long startTime = 0;
//Time we are counting down until
long long endTime = 0;
byte incomingByte = 0;

void setup() {                
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);

  Serial.begin(9600);
}


void loop() {

  //Recieve a byte if available
  if (Serial.available() > 0){
    incomingByte = Serial.read();
    // say what you got:
//    Serial.print("I received: ");
//    Serial.println(incomingByte, DEC);
    //If the incoming byte is 80 ('P')
    //Then start a countdown
    if ((incomingByte == 80)  && (displayAnything == 0)){
      startTime = millis(); 
      endTime = startTime + 40000;
      displayAnything = 1;
    }
    //If incoming byte is 67 ('C')
    //Then cancel the timer
    if ((incomingByte == 67) && (displayAnything == 1)){
      displayAnything = 0;
      analogWrite(3, 0);
      analogWrite(6, 0);
      analogWrite(5, 0);
//      delay(5000);
    }
  }
  
  //If timer is displaying, then light appropriate segments
  if (displayAnything == 1){
//    mycounter++;
//    if(mycounter>=255){
//      mycounter=0;
//    }
    mycounter = 255;
    delay(10);
    if((endTime-millis())<5000){
      analogWrite(6, mycounter);
      analogWrite(5, 0);
      analogWrite(3, 0);
    }
    else if((endTime-millis())<10000){
      analogWrite(5, mycounter);
      analogWrite(6, 0);
      analogWrite(3, 25);
    }
    else{
      analogWrite(3, mycounter);
      analogWrite(6, 0);
      analogWrite(5, 0);
    }

    if (millis() > endTime){
        displayAnything = 0;
        analogWrite(3, 0);
        analogWrite(6, 0);
        analogWrite(5, 0);
        delay(1000);
        Serial.flush();
    }
  }
  if (displayAnything == 0){
      analogWrite(3, 0);
      analogWrite(6, 0);
      analogWrite(5, 0);
  } 

}

