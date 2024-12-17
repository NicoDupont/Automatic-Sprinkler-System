#pip3 install smbus
import lcddriver
from time import *
lcd = lcddriver.lcd()
lcd.lcd_clear()
lcd.lcd_display_string(" Go Tronic", 1)
lcd.lcd_display_string("", 2)
lcd.lcd_display_string(" I2C Serial", 3)
lcd.lcd_display_string(" LCD", 4)
