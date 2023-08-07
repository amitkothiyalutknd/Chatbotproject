from flask import Flask, request, jsonify
import requests

chatBot = Flask(__name__)
@chatBot.route('/', methods = ['POST'])

def index():
    data = request.get_json()
    sourceCurrency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    targetCurrency = data['queryResult']['parameters']['currency-name']
    # print(sourceCurrency, amount, targetCurrency[0])
    convFact = conversionFactor(sourceCurrency, targetCurrency[0])
    # print(convFact)
    finalAmount = round(amount * convFact, 2)
    print(f"Amount of {sourceCurrency}:{amount} in {targetCurrency[0]} is {finalAmount}.")
    reply = {'fulfillmentText': " Amount of {}:{} in {} is {}".format(amount, sourceCurrency, targetCurrency[0], finalAmount)}
    return jsonify(reply)

def conversionFactor(source, target):
    url = "https://v6.exchangerate-api.com/v6/8aabcf7694551cc0870979da/pair/{}/{}".format(source, target)
    result = requests.get(url)
    result = result.json()
    conversionRate = result.get('conversion_rate')
    return conversionRate 

if __name__ == "__main__":
    chatBot.run(debug = True)
