#include <Serial_CAN_Module.h>
#include <SoftwareSerial.h>
Serial_CAN can;
#define can_tx  2           // tx of serial can module connect to D2
#define can_rx  3           // rx of serial can module connect to D3

// 622
byte DATA_622[8];


void setup() {
  //622
  DATA_622[0] = 0;
  DATA_622[1] = 1;
  DATA_622[2] = 2;
  DATA_622[3] = 3;
  DATA_622[4] = 4;
  DATA_622[5] = 5;
  DATA_622[6] = 6;


  Serial.begin(9600);
  can.begin(can_tx, can_rx, 9600);      // tx, rx
}

void loop() {
  if (can.recv(&recv_id, recv_data, &len)) {
	  can.send(0x622, 0, 0, 8, DATA_622);
  }
  delay(1000);
}
