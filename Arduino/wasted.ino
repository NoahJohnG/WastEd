#define IDK '4'
#define NONE '0'
#define COMPOST '1'
#define RECYCLE '2'
#define TRASH '3'

int incoming_byte = 0;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
    if(Serial.available() > 0){
      incoming_byte = Serial.read();

      switch(incoming_byte){
      case NONE:
        Serial.println("Unknown");
        break;
      case COMPOST:
        rotate_compost();
        Serial.println(incoming_byte, DEC);
        break;
      case RECYCLE:
        rotate_recycle();
        Serial.println(incoming_byte, DEC);
        break;
      case TRASH:
        rotate_trash();
        Serial.println(incoming_byte, DEC);
        break;
      case IDK:
        Serial.print("Defaulting to trash->\t");
        rotate_trash();
        Serial.println(incoming_byte, DEC);
        break;
      default:
        Serial.println("Invalid data");
      }
    }
}

void rotate_compost(){
  Serial.print("compost: ");
}

void rotate_recycle(){
    Serial.print("recycle: ");
}

void rotate_trash(){
    Serial.print("trash: ");

}
