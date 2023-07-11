from typing import List, Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import BaseOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
import copy
import uuid

class Navigator(webdriver.Remote, By):

    def __init__(self, command_executor="http://127.0.0.1:4444", keep_alive=True, file_detector=None, options: BaseOptions | List[BaseOptions] = None) -> None:
        super().__init__(command_executor, keep_alive, file_detector, options)

    def initialArguments(self, url:str, test):

        self.targetURL:str = url
        # self.rutinaNormal:list = JSON["rutinaNormal"]
        self.test = test
        self.sucesos:list = []

    def registrarSuceso(self, tipoDeTest:str, indice:int, mensajeEsperado:list, action:dict):

        reporte = {
            "tipoDeTest" : tipoDeTest,
            "indice" : indice,
            "mensajeEsperado" : mensajeEsperado,
            "action" : action
        }
        
        path = uuid.uuid4()
        self.element.screenshot(f'./{path}.png')

        self.sucesos.append(reporte)

    def selectElementByXPATH(self, location:str):
        WebDriverWait(driver=self, timeout=30).until(EC.presence_of_element_located((self.XPATH, location)))
        self.element = self.find_element(by=self.XPATH, 
        value=location)

    def selectElementByCssSelector(self, location:str):
        WebDriverWait(driver=self, timeout=30).until(EC.presence_of_element_located((self.CSS_SELECTOR, location))) 
        self.element = self.find_element(by=self.CSS_SELECTOR, 
        value=location)

    def clickAction(self, validador:bool, mensajesEsperados:list):

        self.element.click()

        if validador:

            print('validando')

            pagesource:str = self.page_source
            errorEncontrado:bool = False

            #Si lo encuentra alguna vez, entonces cambiara su valor a falso
            for m in mensajesEsperados:
                if m in pagesource:
                    print('encontrado')
                    errorEncontrado = True

            #Si el errorEcontrado no ha cambiado su estado, entonces se toma como un suceso registrado; en caso si haya cambiado, no se registra, se detiene la ejecucion
            if errorEncontrado:
                raise TimeoutException
            else:
                raise AssertionError
                

    def initSession(self):
        
        self.get(self.targetURL)

        self.set_window_size(height=1000, width=1300)
        print('sesion iniciada')

    #Ejecutar esto para cada test que se encuentre en el array
    def executeRoutine(self):

        t = self.test

        self.initSession()

        indice:int = int(t["indice"])
        tipoDeTest:str = t["tipoDeTest"]
        mensajesEsperados:list = copy.deepcopy(t["mensajesEsperados"])
        rutina:list = t["rutina"]

        if len(mensajesEsperados) != 0:

            for action in rutina:

                action:dict
                
                command:str = action["command"]

                target:str = action["target"]["location"]
                typeTarget:str = action["target"]["detail"]

                value:str = action["value"]

                validador:bool = action["validador"]

                #Seleccionar elemento:
                if typeTarget != 'css':
                    self.selectElementByXPATH(target)
                else:
                    self.selectElementByCssSelector(target)

                #Realizar accion:
                match command:
                    case 'type':
                        self.element.send_keys(value)
                    case 'click':
                        try:
                            self.clickAction(validador, mensajesEsperados)
                        except TimeoutException:
                            print('Test Inverso Exitoso')
                            break
                        except AssertionError:
                            self.registrarSuceso(tipoDeTest, indice, mensajesEsperados, action)
                            print('suceso registrado')
                            break

        self.quit()