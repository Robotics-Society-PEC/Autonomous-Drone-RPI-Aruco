// Soft serial 4,5
#define BMP280


double altitude_of_quad_from_ultrasonic = 0;
double altitude_of_quad_from_BMP = 0;


#define trigpin 2
#define echopin 3



#include <Adafruit_BMP280.h>
Adafruit_BMP280 bmp;


void setup()
{
  Serial.begin(9600);

  unsigned status;
  status = bmp.begin(0x77);
  if (!status)
  {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                     "try a different address!"));
    while (1)
    {
      status = bmp.begin(0x76);
      delay(1000);
    }
  }

  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
  calibrateForAltitude();                           // ALtitude

}

void loop()
{

printAltitudeData();

}


#ifdef BMP280
void get_altitude_from_barometer()
{
  if (current_time - time_since_last_altitude > 100000) // 10HZ
  {
    time_since_last_altitude = micros();
    // Serial.println("getting Altitude");
    double temp_alt = bmp.readAltitude(normalize_pressure);
    altitude_of_quad_from_BMP = isnan(temp_alt) ? altitude_of_quad_from_BMP : temp_alt;
    altitude_of_quad_from_BMP = constrain(altitude_of_quad_from_BMP, 0, 100);
    // get altitude from sensor
  }
}
#endif

#ifdef HCSR04
void get_altitude_of_quad_from_ultrasonic()
{
  Wire.requestFrom(32, 1); // request 6 bytes from slave device #8

  while (Wire.available())
  {                                                 // slave may send less than requested
    altitude_of_quad_from_ultrasonic = Wire.read(); // receive a byte as character
    // Serial.print(c);      // print the character
  }
  altitude_of_quad_from_ultrasonic /= 100.0;
}
#endif

void printAltitudeData()
{
  if (current_time - print_counter > 10000)
  {

    print_counter = micros();
#ifdef BLUETOOTH_EN
    Serial8.println(altitude_of_quad_from_BMP);
#endif
#ifdef BMP280
    Serial.print("Altitude from BMP280 is ");
    Serial.println(altitude_of_quad_from_BMP);
#endif
#ifdef HCSR04
    Serial.print("Altitude from Ultrasonic is ");
    Serial.println(altitude_of_quad_from_ultrasonic);
#endif
  }
}

void calibrateForAltitude()
{
  // enter calibration code
  // do slowly at 10 hz
  Serial.println("Calibration Starting");
  int i = 0;
  normalize_pressure = 0;
  float temp = 0;
  while (i < 50)
  {
    temp = bmp.readPressure() / 100.0 / 5.0;
    normalize_pressure += temp; // do this 25 times in loop
    Serial.println(temp);
    i++;
    delay(500);
  }
  normalize_pressure = normalize_pressure / 10.0; // for 100th pascal callibration

  // get altitude from sensor
  Serial.println("Calibration Done");
}

#ifdef m8nGPS
void get_data_from_GPS()
{
  if (current_time - time_since_last_gps < 1000000)
  {

    return;
  }

  time_since_last_gps = micros();

  unsigned long start = millis();
  do
  {
    while (Serial5.available()) /* Encode data read from GPS while data is available on serial port */
    {
      gps.encode(Serial5.read());
    }
    /* Encode basically is used to parse the string received by the GPS and to store it in a buffer so that information can be extracted from it */
  } while (millis() - start < 200);
}

void print_gps_data()
{
  if (current_time - print_counter < 10000)
    return;
  print_counter = micros();

  if (!loc_valid)
  {
    Serial.print("Latitude : ");
    Serial.println("*****");
    Serial.print("Longitude : ");
    Serial.println("*****");
    Serial.print("Number of Satellites : ");
    Serial.println(sats_val);
    Serial.print("HDOP of GPS : ");
    Serial.println(gps_hdop);
  }
  else
  {
    Serial.print("Latitude in Decimal Degrees : ");
    Serial.println(lat_val, 6);
    Serial.print("Longitude in Decimal Degrees : ");
    Serial.println(lng_val, 6);
    Serial.print("Number of Satellites : ");
    Serial.println(sats_val);
    Serial.print("HDOP of GPS : ");
    Serial.println(gps_hdop);
  }
  if (!alt_valid)
  {
    Serial.print("Altitude from GPS: ");
    Serial.println("*****");
  }
  else
  {
    Serial.print("Altitude from GPS: ");
    Serial.println(altitude_of_quad_from_GPS, 6);
  }
  if (!time_valid)
  {
    Serial.print("Time : ");
    Serial.println("*****");
  }
  else
  {
    char time_string[32];
    sprintf(time_string, "Time : %02d/%02d/%02d \n", hr_val, min_val, sec_val);
    Serial.print(time_string);
  }
}
#endif