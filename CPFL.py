from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

global driver, contTotal


def getButtonMensagemInicial():
    global driver, contTotal
    try:
        time.sleep(5)
        btn = driver.find_element(By.XPATH, '//*[@id="modal-footer"]/div/div/div/button')
        btn.click()
        return btn
    except:
        return getButtonMensagemInicial()

def RealizarLogin(user, paswrd):
    global driver, contTotal
    contTotal = 0
    time.sleep(7)

    btn = driver.find_element(By.XPATH, '//*[@id="modal-footer"]/div/div/div/button')
    btn.click()

    email = driver.find_element(By.ID, "documentoEmail")
    senha = driver.find_element(By.ID, "password")

    email.send_keys(user)

    senha.send_keys(paswrd)

    ##Tempo para realizar o CAPTCHA
    time.sleep(15)

    btnLogar = driver.find_element(By.XPATH ,'//*[@id="panelMobile"]/div/div[2]/div/div/div/div/div/div/div[3]/div[2]/div/div/div[1]/div/form/div/div[3]/div/button')

    btnLogar.click()


def baixarConta(indexConta, indexTabela):
    global contTotal

    if contTotal == 60:
        return

    time.sleep(25)
    showContas = driver.find_element(By.ID, 'iconeMinhasContasPagas')
    showContas.click()
    
    if (indexTabela > 0):
        i = 0 
        while (i < indexTabela):
            btnProximo = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div/div/div/div/div[5]/div/div/div/div/div/div[2]/div/div/div/div/div/ul/li[7]/a')
            btnProximo.click()
            i = i + 1

    containerContas = driver.find_element(By.ID, 'minhasContasPagas')

    tableContas = containerContas.find_elements(By.TAG_NAME, 'tbody')
    contas = tableContas[0].find_elements(By.TAG_NAME, 'tr')
    mesAno = contas[indexConta].find_elements(By.TAG_NAME, 'td')[0].text
    td2via = contas[indexConta].find_elements(By.TAG_NAME, 'td')[5]
    btn2via = td2via.find_element(By.TAG_NAME, 'button')
    btn2via.click()


    time.sleep(15)
    btnVerConta = driver.find_element(By.ID, 'btnVerContaCompleta')
    btnVerConta.click()

    indexConta = indexConta + 1
    contTotal = contTotal + 1

    if (indexConta >= contas.__len__()):
        indexConta = 0
        indexTabela = indexTabela + 1

    driver.back()

    print(str.format("Index conta: {0} Index Tabela: {1} Mês/Ano: {2}", indexConta, indexTabela, mesAno))

    baixarConta(indexConta, indexTabela)



########################################################## ___MAIN CODE____ #####################################################################

fp = webdriver.FirefoxProfile()

fp.set_preference("browser.download.folderList",2);
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", "D:\joaov")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("plugin.scan.plid.all",False)
fp.set_preference("plugin.scan.Acrobat","99.0")
fp.set_preference("pdfjs.disabled",True)

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(executable_path='C:/geckodriver.exe', options=options, firefox_profile=fp)


driver.get("https://servicosonline.cpfl.com.br/agencia-webapp/#/historico-contas")

RealizarLogin("user", "password")
baixarConta(0,0)