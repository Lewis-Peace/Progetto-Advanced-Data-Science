import requests
import os

class data_downloader:

    file_name = 'raw_data.xml'
    
    def __init__(self, file_name) -> None:
        self.file_name = file_name + '.xml'
        pass   
    
    def format_url(self, params, __from__, __to__) -> str:
        api_url = "https://api.geekdo.com/xmlapi2/thing?"
        for i in range(__from__, __to__ + 1):
            params["id"] = params["id"] + "," + str(i)
        formatted_params = []
        for key in params:
            formatted_params.append(key + "=" + params[key])
        return api_url + "&".join(formatted_params)

    def main(self, starting: int, range: int):
        __to__ = starting + range
        __from__ = starting
        print(f'Downloading boardgames with id {__from__} to id {__to__}')
        try:
            os.remove(self.file_name)
        except:
            1
            
        if not os.path.exists(f"./{self.file_name}"):
            open(f"./{self.file_name}", "x")

        params = {"type": "boardgame", "id": "0", "stats": "1"}


        r = requests.get(self.format_url(params, __from__, __to__))
        with open(f'./{self.file_name}', 'wb') as f:
            f.write(r.content)