import requests
from bs4 import BeautifulSoup
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import logging
from datetime import datetime
import json
import os

class AlertaDesastres:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.model = self.setup_model()
        
    def setup_logging(self):
        """Configura o sistema de logs"""
        logging.basicConfig(
            filename='sistema_alerta.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Carrega configurações do sistema"""
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                'email': 'seu_email@example.com',
                'senha': 'sua_senha',
                'smtp_server': 'smtp.example.com',
                'smtp_port': 587,
                'cache_duration': 300  # 5 minutos
            }
            self.save_config()
            
    def save_config(self):
        """Salva configurações do sistema"""
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_weather_data(self, city_name):
        """Obtém dados meteorológicos"""
        cache_file = f'cache_{city_name}.json'
        
        # Verifica cache
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                if (datetime.now() - datetime.fromisoformat(cached_data['timestamp'])).seconds < self.config['cache_duration']:
                    self.logger.info(f"Usando dados em cache para {city_name}")
                    return cached_data['data']

        try:
            url = f"https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/107/{city_name.lower()}-sc"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            temperature = self.extract_temperature(soup)
            humidity = self.extract_humidity(soup)
            rainfall = self.extract_rainfall(soup)
            
            weather_data = {
                'temperature': temperature,
                'humidity': humidity,
                'rainfall': rainfall
            }
            
            # Salva no cache
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': weather_data
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
                
            self.logger.info(f"Dados meteorológicos coletados para {city_name}")
            return weather_data
            
        except Exception as e:
            self.logger.error(f"Erro ao coletar dados meteorológicos: {str(e)}")
            return None

    def extract_temperature(self, soup):
        """Extrai temperatura do HTML"""
        temp_element = soup.find('span', attrs={'class': '-bold -gray-dark-2 -font-55 _margin-l-20 _center'})
        return self.extract_number(temp_element.text) if temp_element else None

    def extract_humidity(self, soup):
        """Extrai umidade do HTML"""
        humidity_element = soup.find('span', attrs={'data-element': 'humidity'})
        return self.extract_number(humidity_element.text) if humidity_element else None

    def extract_rainfall(self, soup):
        """Extrai precipitação do HTML"""
        rainfall_element = soup.find('span', attrs={'data-element': 'rainfall'})
        return self.extract_number(rainfall_element.text) if rainfall_element else None

    def extract_number(self, text):
        """Extrai números de um texto"""
        if not text:
            return None
        numbers = re.findall(r'\d+', text)
        return int(''.join(numbers)) if numbers else None

    def setup_model(self):
        """Configura o modelo de machine learning"""
        # Dados de exemplo para treino
        X_train = np.array([
            [15, 70, 0],   # [temperatura, umidade, precipitação]
            [22, 80, 10],
            [30, 85, 20],
            [35, 90, 30],
            [40, 95, 40],
            [45, 100, 50]
        ])
        y_train = np.array([0, 0, 0, 1, 1, 1])  # 0: sem risco, 1: risco
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model

    def predict_disaster(self, weather_data):
        """Prevê risco de desastre"""
        if not all(weather_data.values()):
            self.logger.error("Dados meteorológicos incompletos")
            return False
            
        features = np.array([[
            weather_data['temperature'],
            weather_data['humidity'],
            weather_data['rainfall']
        ]])
        
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0][1]
        
        self.logger.info(f"Previsão realizada: {prediction} (Probabilidade: {probability:.2%})")
        return prediction == 1

    def send_alert(self, risk_level, weather_data, recipient):
        """Envia alerta por email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']
            msg['To'] = recipient
            msg['Subject'] = "ALERTA DE RISCO DE DESASTRE NATURAL"
            
            body = f"""
            ALERTA DE RISCO - Sistema de Prevenção de Desastres Naturais
            
            Condições atuais:
            - Temperatura: {weather_data['temperature']}°C
            - Umidade: {weather_data['humidity']}%
            - Precipitação: {weather_data['rainfall']}mm
            
            Nível de risco: {'ALTO' if risk_level else 'BAIXO'}
            
            Por favor, fique atento às orientações das autoridades locais.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['email'], self.config['senha'])
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Alerta enviado para {recipient}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao enviar alerta: {str(e)}")
            return False

def main():
    sistema = AlertaDesastres()
    
    # Lista de cidades a monitorar
    cidades = ["Blumenau", "Itajai", "Brusque"]
    email_destinatario = "recipient@example.com"
    
    for cidade in cidades:
        # Coleta dados
        weather_data = sistema.get_weather_data(cidade)
        if weather_data:
            # Analisa risco
            risco = sistema.predict_disaster(weather_data)
            if risco:
                # Envia alerta
                sistema.send_alert(risco, weather_data, email_destinatario)
                print(f"Alerta enviado para {cidade}")
            else:
                print(f"Sem risco detectado para {cidade}")
        else:
            print(f"Falha ao coletar dados para {cidade}")

if __name__ == "__main__":
    main()