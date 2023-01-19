#include <TinyGPS++.h>
#include <SoftwareSerial.h>

TinyGPSPlus gps;
SoftwareSerial ss(21, 20); // RX, TX

void setup()
{
  ss.begin(9600);
  Serial.begin(9600);
}

void loop()
{

  while (ss.available() > 0)
  {
    gps.encode(ss.read());
  }

  Serial.print("\nLAT= "); Serial.print(gps.location.lat(), 6);
  Serial.print("\nLNG= "); Serial.println(gps.location.lng(), 6);
  Serial.print("No of sats= "); Serial.println(gps.satellites.value());
  Serial.print("HDOP= "); Serial.println(gps.hdop.value());

  delay(2000);

}
