import requests
import os
import json
import logging

class request:
    
    def __init__(self):
        pass

    def get_aqi_request(self, city, state, country):
        try:
            api_url = 'https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69'
            custom_headers = {'accept': 'application/json'}
            query_params = {'api-key' : '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b', 'format' : 'json', 'limit' : 10,
                        'filters[country]' : country, 'filters[state]' : state, 'filters[city]' : city}
            
            response = requests.get(api_url, params=query_params, headers=custom_headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()  # Parse the JSON response

        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return None
        except ValueError as e: # Catch json decode errors
            print(f"Error decoding JSON: {e}")
            return None

    def process_response(self,data):
        Data_dict = {}
        for i in range(0,len(data['records'])):
            if data['records'][i]['avg_value'] != 'NA':
                val = data['records'][i]['pollutant_id']
                if val in Data_dict.keys():
                    if Data_dict[val] > data['records'][i]['avg_value']:
                        pass
                    else:
                        Data_dict[val] = data['records'][i]['avg_value']
                else:
                    Data_dict[val] = data['records'][i]['avg_value']
        return Data_dict
    
    def send_message(self, data_dict, bot_token, chat_id):
        # bot_token = '7962289368:AAH69o8EbAHnHtgcWjs16dCVQRV7IMfZb24'
        # chat_id = 7523910798

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={data_dict}"
        
        res = requests.post(url)
        
        return res


def main():
    try:
        dir = os.getcwd()
        parent = os.path.dirname(dir)
        data_path = "\\".join([parent,'utils','data.json'])
        log_path = "\\".join([parent,'log','logfile.log'])
        form_data_path = "\\".join([parent,'utils','form_data.json'])
        # Configure logging (basic configuration)
        logging.basicConfig(filename=log_path, 
                            level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode="a",)
        
        with open(form_data_path,'r') as file_read:
            form_data = json.load(file_read)
            
        
        #Object Creation
        obj = request()

        data = obj.get_aqi_request(form_data['dis'], form_data['state'], form_data['country'])

        
        if data:
            logging.info("AQI Data fetched successfully")

            response_dict = obj.process_response(data)
            
            res = obj.send_message(f"AQI Index is {response_dict}", form_data['bot_token'], form_data['chat_id'])
            if res == 200:
                logging.info("Data sent to Telegram")
            with open(data_path,'w') as file:
                json.dump(data, file, indent=4)
            
        else:
            logging.error("Failed to retrieve API data.")

    except Exception as e:
        logging.error(e)
        
    logging.shutdown()
        
if __name__ == "__main__":
    main()

    

        

    