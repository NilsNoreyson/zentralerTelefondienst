/////////////////////////////////////////////////
////// Telefon Impulswahl Arduino 1.0 ///////////
//// (ccnc) Lasse Marburg / machinaex.de ////////
/////////////////////////////////////////////////

// Impulswahltelefon an Arduino anschließen ////
// und Wahleingaben abhnehmen //////////////////

#define encoder0PinA  2
#define encoder0PinB  3

volatile unsigned int rotCountLimit = 3;
volatile unsigned int rotCount = 0;
volatile unsigned int rotDir = 100;
volatile unsigned int encoder0Pos = 0;


int dialPin = 0; // Analog 0 für Messung am Telefon
int dialVal = 0;
int dialValStat = 1;

int nummer = 0;
int taste = 10;

unsigned long int signalstart = 0;
unsigned long int signalstop = 0;

unsigned long int signalzeit = 0;
unsigned long int keinsignalzeit = 0;

unsigned long int auszeit = 200;
unsigned long int zwischenzeit = 600;

int midValue = 1000; // der Schwellenwert um aufgelegt (LOW) von abgenommen (HIGH) zu unterscheiden

boolean dialing = false;
boolean aufgelegt = false;


void setup() 
{
  // Serial Schnittstelle inititalisieren
  Serial.begin(115200);

  pinMode(dialPin, INPUT);

   
   pinMode(encoder0PinA, INPUT); 
   digitalWrite(encoder0PinA, HIGH);       // turn on pulldown resistor
   pinMode(encoder0PinB, INPUT); 
   digitalWrite(encoder0PinB, HIGH);       // turn on pulldown resistor

   attachInterrupt(0, doEncoder, CHANGE);  // encoder pin on interrupt 0 - pin 2
}


void loop() 
{
  //Serial.println(analogRead(0));
  
  if (analogRead(dialPin) > midValue)
  {
    dialVal = 1;
  } else {
    dialVal = 0;
  }

 
  if ( dialVal != dialValStat )
  {
    dialValStat = dialVal;
    //Serial.println("AHHHH");
    if (dialVal == HIGH)
    {
      signalstop = millis();
      nummer++;
      //Serial.println("tel.dail");
      delay(50);

    }
  }

  /*
  *   Abfrage ob waehlscheibe runtergelaufen
  */
  keinsignalzeit = millis() - signalstop;

  if ( keinsignalzeit > zwischenzeit )
  {
    if (nummer == 10) 
    {
      taste = 0;
    } 
    else if (nummer > 0) {
      taste = nummer;
    }
    if (taste < 10) 
    {
      Serial.print("tel.");
      Serial.print(taste);
      Serial.println();

    }

    nummer = 0;
    taste = 10;
  }


  /*
  *   abfrage ob hoerer aufgelegt
   */
  
}



void doEncoder() {
  /* If pinA and pinB are both high or both low, it is spinning
   * forward. If they're different, it's going backward.
   *
   * For more information on speeding up this process, see
   * [Reference/PortManipulation], specifically the PIND register.
   */
  if (digitalRead(encoder0PinA) == digitalRead(encoder0PinB)) {
    encoder0Pos--;
    rotDir=rotDir-1;
    rotCount=rotCount+1;
  } else {
    encoder0Pos++;
    rotDir=rotDir+1;
    rotCount=rotCount+1;
  }
//  Serial.println(rotDir);
  if (rotCount>rotCountLimit){
    if (rotDir>101) {
      Serial.println ("rot.+");
    }
    if (rotDir<99){
      Serial.println ("rot.-");
    }
    rotDir=100;
    rotCount=0;
  }
 
}
