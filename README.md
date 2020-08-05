# ScrapeModem

An extremely basic modem scraping utility, with default Prometheus and Grafana deployments for visualizing network status.

![Example Deployment Dashboard](https://i.imgur.com/pFBMeah.png)

## Supported Modems

Currently only the Netgear CM1000 is supported.

## Setup

The easiest deployment is using `docker-compose`, which will setup and link prometheus/grafana/scrapemodem. An environment
file is required, `modem-info.env` which is used to provide information on the modem being scraped.

```
MODEM_IP=192.168.100.1
MODEM_USER=example_user
MODEM_PASSWORD=example_password
```

This should be placed next to `docker-compose.yml` before execution. Once setup, `docker-compose` will take care of the rest:

```
docker-compose up -d
```
 
Default services can be found at the following addresses:

| Service | Default Port |
|---------|--------------|
| Grafana | 3000         |
| Prometheus | 9090      |
| Prometheus-blackbox | 9115 |
| ScrapeModem | 5000     |
