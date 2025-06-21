import time
import logging
import base64
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import threading

class WhatsAppBot:
    def __init__(self):
        self.driver = None
        self.is_connected = False
        self.logger = logging.getLogger(__name__)
        self.qr_code_base64 = None
        
    def setup_driver(self):
        """Configura o driver do Chrome para o WhatsApp Web"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Para desenvolvimento, não usar headless para poder ver o QR code
        # chrome_options.add_argument("--headless")
        
        # Configurações para WhatsApp Web
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            # Usar WebDriver Manager para baixar automaticamente o ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao configurar driver: {e}")
            return False
    
    def capture_qr_code(self):
        """Captura o QR Code e converte para base64"""
        try:
            # Aguardar o QR Code aparecer
            qr_element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Scan me!']"))
            )
            
            # Capturar screenshot do QR Code
            qr_screenshot = qr_element.screenshot_as_png
            
            # Converter para base64
            qr_base64 = base64.b64encode(qr_screenshot).decode('utf-8')
            self.qr_code_base64 = f"data:image/png;base64,{qr_base64}"
            
            return True, "QR Code capturado com sucesso"
            
        except TimeoutException:
            return False, "QR Code não encontrado - talvez já esteja conectado"
        except Exception as e:
            self.logger.error(f"Erro ao capturar QR Code: {e}")
            return False, f"Erro ao capturar QR Code: {str(e)}"
    
    def wait_for_connection(self, timeout=90):
        """Aguarda a conexão ser estabelecida após escanear o QR Code com timeout estendido"""
        try:
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                # Verificar conexão usando múltiplos métodos
                connected, message = self.check_connection_status()
                if connected:
                    self.is_connected = True
                    self.qr_code_base64 = None  # Limpar QR Code após conexão
                    return True, "Conectado com sucesso"
                
                # Aguardar um pouco antes da próxima verificação
                time.sleep(2)
            
            return False, "Timeout - QR Code não foi escaneado a tempo"
            
        except Exception as e:
            self.logger.error(f"Erro ao aguardar conexão: {e}")
            return False, f"Erro ao aguardar conexão: {str(e)}"
    
    def connect_whatsapp(self):
        """Conecta ao WhatsApp Web com detecção melhorada"""
        if not self.setup_driver():
            return False, "Erro ao configurar o navegador", None
        
        try:
            self.driver.get("https://web.whatsapp.com")
            
            # Aguardar o carregamento da página
            time.sleep(8)  # Aumentar tempo de carregamento
            
            # Verificar se já está logado usando múltiplos métodos
            connected, message = self.check_connection_status()
            if connected:
                self.is_connected = True
                return True, "Conectado com sucesso", None
            
            # Se não está conectado, tentar capturar QR Code
            success, qr_message = self.capture_qr_code()
            if success:
                return False, "QR Code disponível para escaneamento", self.qr_code_base64
            else:
                return False, qr_message, None
                
        except Exception as e:
            self.logger.error(f"Erro ao conectar WhatsApp: {e}")
            return False, f"Erro de conexão: {str(e)}", None
    
    def check_connection_status(self):
        """Verifica se a conexão ainda está ativa com múltiplos métodos de detecção"""
        if not self.driver:
            return False, "Driver não inicializado"
        
        try:
            # Verificar se ainda está na página do WhatsApp
            current_url = self.driver.current_url
            if "web.whatsapp.com" not in current_url:
                self.is_connected = False
                return False, "Não está na página do WhatsApp Web"
            
            # Método 1: Verificar se há QR Code (indica não conectado)
            try:
                qr_element = self.driver.find_element(By.XPATH, "//canvas[@aria-label='Scan me!']")
                if qr_element and qr_element.is_displayed():
                    self.is_connected = False
                    # Atualizar QR Code
                    self.capture_qr_code()
                    return False, "QR Code disponível - não conectado"
            except NoSuchElementException:
                pass  # Não há QR Code, pode estar conectado
            
            # Método 2: Verificar elementos que indicam conexão ativa
            connection_indicators = [
                "//div[@contenteditable='true'][@data-tab='3']",  # Caixa de busca
                "//div[@data-testid='search']",  # Nova caixa de busca
                "//span[@data-testid='search-input']",  # Input de busca
                "//div[contains(@class, 'search')]//input",  # Input genérico de busca
                "//div[@title='Nova conversa']",  # Botão nova conversa
                "//div[@data-testid='chat-list']",  # Lista de conversas
                "//div[contains(@class, 'chat-list')]",  # Lista de conversas alternativa
                "//header[contains(@class, 'app-header')]",  # Header do app
                "//div[@data-testid='side']",  # Sidebar
                "//div[contains(@class, 'app-wrapper-web')]"  # Wrapper principal
            ]
            
            for xpath in connection_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                    if element and element.is_displayed():
                        self.is_connected = True
                        self.qr_code_base64 = None  # Limpar QR Code se conectado
                        return True, "Conectado"
                except NoSuchElementException:
                    continue
            
            # Método 3: Verificar se há texto indicativo de conexão
            try:
                page_source = self.driver.page_source.lower()
                if any(text in page_source for text in ['whatsapp web', 'conversas', 'chats', 'mensagens']):
                    # Verificar se não há indicadores de desconexão
                    if not any(text in page_source for text in ['qr code', 'scan', 'código', 'escanear']):
                        self.is_connected = True
                        return True, "Conectado (detectado por conteúdo)"
            except Exception:
                pass
            
            # Método 4: Verificar URL específica de conversa
            if "/send?phone=" in current_url or "/chat/" in current_url:
                self.is_connected = True
                return True, "Conectado (em conversa)"
            
            # Se chegou até aqui, provavelmente não está conectado
            self.is_connected = False
            return False, "Status de conexão incerto - pode não estar conectado"
                
        except Exception as e:
            self.logger.error(f"Erro ao verificar status: {e}")
            self.is_connected = False
            return False, f"Erro ao verificar status: {str(e)}"
    
    def search_contact(self, phone_number):
        """Busca um contato pelo número de telefone"""
        if not self.is_connected:
            return False, "WhatsApp não está conectado"
        
        try:
            # Limpar número de telefone (remover caracteres especiais)
            clean_phone = ''.join(filter(str.isdigit, phone_number))
            
            # Usar a URL direta para abrir conversa
            url = f"https://web.whatsapp.com/send?phone=55{clean_phone}"
            self.driver.get(url)
            
            # Aguardar a conversa carregar
            time.sleep(3)
            
            # Verificar se a conversa foi aberta
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
                )
                return True, "Contato encontrado"
            except TimeoutException:
                return False, "Contato não encontrado ou não possui WhatsApp"
                
        except Exception as e:
            self.logger.error(f"Erro ao buscar contato: {e}")
            return False, f"Erro ao buscar contato: {str(e)}"
    
    def send_message(self, phone_number, message):
        """Envia uma mensagem para um número específico"""
        if not self.is_connected:
            return False, "WhatsApp não está conectado"
        
        try:
            # Buscar o contato
            success, msg = self.search_contact(phone_number)
            if not success:
                return False, msg
            
            # Encontrar a caixa de texto
            try:
                message_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
                )
                
                # Limpar a caixa de texto e digitar a mensagem
                message_box.clear()
                message_box.send_keys(message)
                
                # Aguardar um pouco antes de enviar
                time.sleep(1)
                
                # Encontrar e clicar no botão de enviar
                send_button = self.driver.find_element(By.XPATH, "//span[@data-icon='send']")
                send_button.click()
                
                # Aguardar o envio
                time.sleep(2)
                
                return True, "Mensagem enviada com sucesso"
                
            except TimeoutException:
                return False, "Não foi possível encontrar a caixa de mensagem"
            except NoSuchElementException:
                return False, "Botão de enviar não encontrado"
                
        except Exception as e:
            self.logger.error(f"Erro ao enviar mensagem: {e}")
            return False, f"Erro ao enviar mensagem: {str(e)}"
    
    def send_bulk_messages(self, contacts_messages):
        """
        Envia mensagens em lote
        contacts_messages: lista de dicionários com 'phone' e 'message'
        """
        if not self.is_connected:
            return False, "WhatsApp não está conectado"
        
        results = []
        
        for contact in contacts_messages:
            phone = contact.get('phone')
            message = contact.get('message')
            
            if not phone or not message:
                results.append({
                    'phone': phone,
                    'success': False,
                    'message': 'Telefone ou mensagem não fornecidos'
                })
                continue
            
            success, msg = self.send_message(phone, message)
            results.append({
                'phone': phone,
                'success': success,
                'message': msg
            })
            
            # Aguardar entre mensagens para evitar bloqueios
            time.sleep(3)
        
        return True, results
    
    def disconnect(self):
        """Desconecta do WhatsApp Web"""
        if self.driver:
            try:
                self.driver.quit()
                self.is_connected = False
                self.qr_code_base64 = None
                return True, "Desconectado com sucesso"
            except Exception as e:
                self.logger.error(f"Erro ao desconectar: {e}")
                return False, f"Erro ao desconectar: {str(e)}"
        return True, "Já estava desconectado"
    
    def get_status(self):
        """Retorna o status da conexão"""
        return {
            'connected': self.is_connected,
            'driver_active': self.driver is not None,
            'qr_code': self.qr_code_base64
        }

# Instância global do bot
whatsapp_bot = WhatsAppBot()

