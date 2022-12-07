import Adafruit_CharLCD as LCD
import time
import RPi.GPIO as GPIO

# Pinos LCD x Raspberry (GPIO)
lcd_rs = 18
lcd_en = 23
lcd_d4 = 25
lcd_d5 = 16
lcd_d6 = 20
lcd_d7 = 21
lcd_backlight = 4
push_button1 = 4
push_button2 = 3
servoSerra = 12
servoPeca = 13
DELAY = 0.003
DELAY1 = 0.1
duty = 0
# Define numero de colunas e linhas do LCD
lcd_colunas = 16
lcd_linhas = 2


class Hardware:

    def __init__(self):
        self.lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5,
                                        lcd_d6, lcd_d7, lcd_colunas, lcd_linhas,
                                        lcd_backlight)
        GPIO.setup(push_button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(push_button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(servoSerra, GPIO.OUT)
        GPIO.setup(servoPeca, GPIO.OUT)
        self.pwm1 = GPIO.PWM(servoSerra, 100)
        self.pwm0 = GPIO.PWM(servoPeca, 100)
        self.dificuldade = 0
        self.pos0 = 180
        self.pos1 = 41
        self.pwm0.start(self.AngleToDuty(self.pos0))
        self.pwm1.start(self.AngleToDuty(self.pos1))

    def imprime_dificil(self):
        self.lcd.clear()
        self.lcd.message('     Hard\n')
        self.lcd.message('Change    Select')

    def imprime_facil(self):
        self.lcd.clear()
        self.lcd.message('     Easy\n')
        self.lcd.message('Change    Select')

    def imprime_normal(self):
        self.lcd.clear()
        self.lcd.message('     Medium\n')
        self.lcd.message('Change    Select')

    def imprime_escolheInicio(self):
        self.lcd.clear()
        self.lcd.message('Quem comeca?\n')
        self.lcd.message('Jogador   Coelho')

    def botao_pressionado(self):
        if GPIO.input(push_button1) == GPIO.HIGH:
            return 1
        elif GPIO.input(push_button2) == GPIO.HIGH:
            return 2
        else:
            return 0

    def AngleToDuty(self, ang):
        return float(ang) / 10. + 5.

    def jogada(self, coluna):
        self.lcd.clear()
        self.lcd.message('     Jogada\n')
        self.lcd.message('    Coluna %s' % (coluna))
        if coluna == 0:
            aux = 41
        elif coluna == 1:
            aux = 39
        elif coluna == 2:
            aux = 35
        elif coluna == 3:
            aux = 32
        elif coluna == 4:
            aux = 26
        elif coluna == 5:
            aux = 17
        else:
            aux = 0

        while self.pos1 > aux:
            self.pos1 = self.pos1 - 1
            duty = self.AngleToDuty(self.pos1)
            self.pwm1.ChangeDutyCycle(duty)
            time.sleep(DELAY1)

        time.sleep(1.0)
        self.dispara_peca()
        time.sleep(5.0)

        while self.pos1 < 41:
            self.pos1 = self.pos1 + 1
            duty = self.AngleToDuty(self.pos1)
            self.pwm1.ChangeDutyCycle(duty)
            time.sleep(DELAY1)

    def dispara_peca(self):
        while self.pos0 > 0:
            self.pos0 = self.pos0 - 1
            duty = self.AngleToDuty(self.pos0)
            self.pwm0.ChangeDutyCycle(duty)
            time.sleep(DELAY)

        while self.pos0 < 180:
            self.pos0 = self.pos0 + 1
            duty = self.AngleToDuty(self.pos0)
            self.pwm0.ChangeDutyCycle(duty)
            time.sleep(DELAY)


if __name__ == '__main__':
    hard = Hardware()

    dificuldade = 0
    starter = 0

    hard.imprime_facil()
    difSelected = 0
    while difSelected == 0:
        botao = hard.botao_pressionado()
        if botao == 1:
            dificuldade = (dificuldade % 3) + 1
            if dificuldade == 1:
                hard.imprime_facil()
            elif dificuldade == 2:
                hard.imprime_normal()
            else:
                hard.imprime_dificil()
            time.sleep(1.0)
        elif botao == 2:
            difSelected = 1
            hard.imprime_escolheInicio()
            time.sleep(1.0)

    while hard.botao_pressionado() == 0:
        continue

    if hard.botao_pressionado() == 1:
        starter = 1
    else:
        starter = 2

    hard.lcd.clear()
    hard.lcd.message('%s comeca\n'% (starter))
    hard.lcd.message('Dificuldade %s'% (dificuldade))




        # hard.botao_pressionado()
        # hard.jogada(6)
        # time.sleep(2.0)
        # hard.jogada(5)
        # time.sleep(2.0)
        # hard.jogada(4)
        # time.sleep(2.0)
        # hard.jogada(3)
        # time.sleep(2.0)
        # hard.jogada(2)
        # time.sleep(2.0)
        # hard.jogada(1)
        # time.sleep(2.0)
        # hard.jogada(0)
        # time.sleep(2.0)