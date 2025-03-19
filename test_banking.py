from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
import time
import re 

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000/login")

driver.find_element(By.ID, "email").send_keys("jose.ort@urosario.edu.co")
driver.find_element(By.ID, "password").send_keys("Admin123*")
driver.find_element(By.ID, "login").click()
time.sleep(2)
saldo_texto= driver.find_element(By.ID, "saldo_usuario").text
saldo_inicial= float(saldo_texto.split(":")[1].strip())

print(saldo_inicial)

driver.find_element(By.ID, "deposit_button").click()
time.sleep(2)
driver.find_element(By.ID, "balance").send_keys("100")
driver.find_element(By.ID, "deposit_button").click()
time.sleep(2)
saldo_texto= driver.find_element(By.ID, "saldo_usuario").text
saldo_final= float(saldo_texto.split(":")[1].strip())
assert saldo_final == saldo_inicial + 100,(f"El saldo final es {saldo_final} y el saldo inicial es {saldo_inicial}")
time.sleep(2)

#prueba bonita
driver.find_element(By.ID, "withdraw_button").click()
time.sleep(2)
driver.find_element(By.ID, "balance").send_keys("50")
driver.find_element(By.ID, "password").send_keys("Admin123*")
driver.find_element(By.ID, "withdraw_button").click()
time.sleep(2)
saldo_texto= driver.find_element(By.ID, "saldo_usuario").text
saldo_final= float(saldo_texto.split(":")[1].strip())
assert saldo_final == saldo_inicial + 50,(f"El saldo final es {saldo_final} y el saldo deberia ser {saldo_inicial + 50,}")
time.sleep(2)
#prueba fea
driver.find_element(By.ID, "logout_button").click()
driver.find_element(By.ID, "email").send_keys("se.ort@urosario.edu.co")
driver.find_element(By.ID, "password").send_keys("A23*")
driver.find_element(By.ID, "login").click()
time.sleep(2)
alerta = driver.find_element(By.ID, "alertaa").text
assert alerta == "Credenciales inválidas", (f"El mensaje de alerta es {alerta} y deberia ser Credenciales inválidas")
driver.quit()