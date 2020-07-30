from os import environ

import requests
from bs4 import BeautifulSoup
from flask import Flask

MODEM_IP = environ.get("MODEM_IP")
MODEM_USER = environ.get("MODEM_USER")
MODEM_PASSWORD = environ.get("MODEM_PASSWORD")

app = Flask(__name__)


# TODO: Cleanup structure/management of data instead of using "dumb" objects
class USBondedChannel:
    def __init__(self, number, lock, modulation, channel_id, freq, power):
        self.number = number
        self.lock = lock
        self.modulation = modulation
        self.channel_id = channel_id
        self.freq = freq
        self.power = power

    def __repr__(self):
        return f"modem_us_bonded_channel{{id=\"{self.number}\",frequency=\"{self.freq}\"}} {self.power.split(' ')[0]}"


class BondedChannel:
    def __init__(self, number, lock, modulation, channel_id, freq, power, snr_mer,
                 unerrored_cw, correctable_cw, uncorrectable_cw):
        self.number = number
        self.lock = lock
        self.modulation = modulation
        self.channel_id = channel_id
        self.freq = freq
        self.power = power
        self.snr_mer = snr_mer
        self.unerrored_cw = unerrored_cw
        self.correctable_cw = correctable_cw
        self.uncorrectable_cw = uncorrectable_cw

    def __repr__(self):
        return f"modem_bonded_channel{{id=\"{self.number}\",frequency=\"{self.freq}\"}} {self.power.split(' ')[0]}"


@app.route('/metrics')  # TODO: cache most recent result
def get_current_stats():
    data = []  # TODO: Don't just build a bunch of objects to throw away every API hit

    def __clean_data(table):
        return [[ele.text.strip() for ele in _item.find_all("td")]
                for _item in table]

    # TODO: make the default endpoints configurable based on modem being queried
    url = f"http://{MODEM_IP}/DocsisStatus.asp"
    request = requests.get(url, auth=(MODEM_USER, MODEM_PASSWORD))

    soup = BeautifulSoup(request.content, 'html.parser')

    # TODO: create per-modem parsing callbacks
    ds_table = soup.find(id="dsTable")
    ds_rows = __clean_data(ds_table.find_all("tr"))
    for item in ds_rows[1:]:
        data.append(BondedChannel(*item))

    us_table = soup.find(id="usTable")
    us_rows = __clean_data(us_table.find_all("tr"))
    for item in us_rows[1:]:
        data.append(USBondedChannel(*item))

    return "\n".join([str(value) for value in data])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
