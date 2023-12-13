#DATA: 21/09/2023
import dht
import machine
import time
import urequests

# Configuração do dht11
d = dht.DHT11(machine.Pin(4))

# Configuração do relé
rele = machine.Pin(2, machine.Pin.OUT)

# Função para conectar no wifi
def conecta(ssid, senha):
    import network
    import time
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, senha)
    for t in range(50):
        if station.isconnected():
            break
        time.sleep(0.1)
    return station

# Configuração do wifi
print("Conectando....")
station = conecta("ID_WIFI", "SENHA_WIFI")
time.sleep(5);

# Função para enviar os dados ao ThingSpeak
def enviar_dados_thingspeak():
    d.measure()
    temperatura = d.temperature()
    umidade = d.humidity()
    print("Temperatura= {}ºC Umidade= {}%".format(temperatura, umidade))
    
    print("Acessando o site...")
    url = "https://api.thingspeak.com/update?api_key=1IGAVUOLSI8CFL5R&field1="+str(temperatura)+"&field2="+str (umidade)
    response = urequests.get(url)
    print("Dados enviados para o ThingSpeak...", response.text)
    response.close()
          
if not station.isconnected():
    print("Não Conectado!")   
else:
    print("Conectado!")
    # Loop para ficar mandando atualização para o ThingSpeak
    while True:
        enviar_dados_thingspeak()
        
        # Verifica as condições para ligar o Relé
        temperatura = d.temperature()
        umidade = d.humidity()
        if temperatura > 31 or umidade > 70:
            print("Condição atendida - Relé Ligado")
            rele.on()# Liga o relé
        else:
            print("Condição não atendida - Relé Desligado ")
            rele.off()# Desliga o relé
        
        time.sleep(180)# Aguarda 3 minutos para enviar um nova leitura para o ThingSpeak
    station.disconnect()
