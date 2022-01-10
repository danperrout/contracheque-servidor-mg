from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv

load_dotenv()

masp = os.getenv('MASP')
senha = os.getenv('SENHA')


def save_html(codigo,data):
    f = open(f"{masp}/{data}.html", "w")
    f.write(codigo)
    f.close()
    print(f"{data}.html salvo com sucesso")

# Main Function
if __name__ == '__main__':
    
    if not os.path.exists(masp):
        os.makedirs(masp)

    sleep_timer = 1

    current_date = datetime.today()
    #current_date = datetime(2013, 8, 17)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')
  
    # Provide the path of chromedriver present on your system.
    driver = webdriver.Chrome(executable_path="chromedriver",
                              chrome_options=options)
  
    # Send a get request to the url
    driver.set_window_size(1920,1080)
    driver.get('https://www.portaldoservidor.mg.gov.br/azpf/broker2/?controle=ContraCheque')
    #time.sleep(10)

    driver.get("https://www.portaldoservidor.mg.gov.br/azpf/broker2/?controle=ContraCheque")
    driver.set_window_size(1440, 818)
    driver.find_element(By.ID, "inputMasp").click()
    driver.find_element(By.ID, "inputMasp").send_keys(masp)
    driver.find_element(By.ID, "inputSenha").send_keys(senha)
    time.sleep(sleep_timer)
    driver.find_element(By.CSS_SELECTOR, "input:nth-child(6)").click()
    while True:
        print('Current Date: ', current_date.date())
        n = 1
        past_date = current_date - relativedelta(months=n)
        # Convert datetime object to string in required format
        date_format = '%m/%Y'
        past_date_str = past_date.strftime(date_format)
        time.sleep(sleep_timer)
        try:
            driver.find_element(By.ID, "mesAno").click()
        except:
            driver.execute_script("window.history.go(-1)")
            time.sleep(sleep_timer)
            driver.find_element(By.ID, "mesAno").click()
            driver.find_element(By.ID, "mesAno").clear()

        time.sleep(sleep_timer)
        driver.find_element(By.ID, "mesAno").send_keys(past_date_str)
     
        time.sleep(sleep_timer)
        driver.find_element(By.CSS_SELECTOR, "input:nth-child(3)").click()
        codigo = driver.page_source
        stopword = "Nao possui contracheque no mes/ano"
        if stopword in codigo:
            break

        decimoterceiro = "FOLHA DECIMO TERCEIRO"
        folhaextra = "FOLHA EXTRA"
        premio = "PREMIO POR RESULTADOS"

        calcula_folha_extra = False
        texto_adicional_folha_extra = ""

        if (premio in codigo):
            calcula_folha_extra = True
            texto_adicional_folha_extra = premio.replace(" ","_")
        elif (folhaextra in codigo):
            calcula_folha_extra = True
            texto_adicional_folha_extra = folhaextra.replace(" ","_")
        elif (decimoterceiro in codigo):
            calcula_folha_extra = True
            texto_adicional_folha_extra = decimoterceiro.replace(" ","_")
        else:
            pass

        if calcula_folha_extra:
            #Faz procedimento da folha do 13o
            time.sleep(sleep_timer)
            driver.find_element(By.ID, "folha1").click()
            # 12 | click | css=input:nth-child(3) |  | 
            time.sleep(sleep_timer)
            driver.find_element(By.CSS_SELECTOR, "input:nth-child(3)").click()
            codigo = driver.page_source
            print(f"Decimo Terceiro Ou Folha Extra: {past_date.year}_{past_date.month}")
            save_html(codigo,f"{past_date.year}_{past_date.month}_{texto_adicional_folha_extra}")
            #time.sleep(10)
            # 13 | click | linkText=VOLTAR |  | 
            time.sleep(sleep_timer)
            driver.find_element(By.LINK_TEXT, "VOLTAR").click()

            #Faz o procedimento para o mes de Novembro Normal
            time.sleep(sleep_timer)
            driver.find_element(By.ID, "mesAno").click()
            time.sleep(sleep_timer)
            driver.find_element(By.ID, "mesAno").send_keys(past_date_str)
            time.sleep(sleep_timer)
            driver.find_element(By.CSS_SELECTOR, "input:nth-child(3)").click()
            time.sleep(sleep_timer)
            driver.find_element(By.CSS_SELECTOR, "input:nth-child(3)").click()
            
            codigo = driver.page_source


        save_html(codigo,f"{past_date.year}_{past_date.month}")
        time.sleep(sleep_timer)
        driver.find_element(By.LINK_TEXT, "VOLTAR").click()
        #Reseta variaveis
        current_date = past_date
        calcula_folha_extra = False
        texto_adicional_folha_extra = ""

    time.sleep(sleep_timer)
    driver.quit()
    print("Done")