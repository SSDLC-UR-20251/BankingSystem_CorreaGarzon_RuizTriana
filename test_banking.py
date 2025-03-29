from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import time
import re

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000/login")

# Iniciar sesión
driver.find_element(By.ID, "email").send_keys("sara.palaciosc@urosario.edu.co")
driver.find_element(By.ID, "password").send_keys("ELZN-ayGhj4WbaBaDKqL")
driver.find_element(By.ID, "login").click()

time.sleep(2)  # Esperar a que cargue la página

saldo_texto = driver.find_element(By.ID, "saldo_usuario").text
saldo_inicial = float(saldo_texto.split(":")[-1].strip())

#print(f"Saldo inicial: {saldo_inicial}")

driver.find_element(By.ID, "deposit_button").click()

time.sleep(2)

driver.find_element(By.ID, "balance").send_keys("100")

driver.find_element(By.ID, "deposit_button").click()

time.sleep(2)

saldo_texto_final = driver.find_element(By.ID, "saldo_usuario").text
saldo_final = float(saldo_texto_final.split(":")[-1].strip())

assert saldo_final == saldo_inicial + 100,f"Error: saldo esperado {saldo_inicial + 100}, pero se obtuvo {saldo_final}"

driver.quit()   