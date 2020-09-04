## Yellow Page Crawler
 
> It is aiming to get a list of [organizations](https://github.com/naivomah3/yellowpage-harvesting/blob/master/yellow-page-data.csv) in [Madagascar](https://www.yellowpagesofafrica.com/country/madagascar/) along with their activity, address and contact from the [Yellow Page Africa](https://www.yellowpagesofafrica.com/). \
> I made this script to help a friend of mine who has recently set up his own startup on the business call campaign. \
\
> WARNING: 
> As web scraping is sometimes subject to nuisance to the website and could disrupt its services, I highly recommend to first read and agree on the TOS of the website and experiment this script on your own head be it. 


## Installation

This is an implementation of a Python [Scrapy](https://scrapy.org/) web crawler in which I use [Splash](https://splash.readthedocs.io/en/stable/index.html) to load and render Javascript embedded on pages and [Docker](https://www.docker.com/) container as a middleware serving the **fully rendered**(includes the necessary javascript events embedded on different components) pages. 


```bash
# For conda user 
conda install -c conda-forge scrapy
# Or using pip 
pip install Scrapy
# Install Splash using pip 
pip install scrapy-splash
# Pull the image 
sudo docker pull scrapinghub/splash
# Run the container
sudo docker run -p 8050:8050 scrapinghub/splash
```
In order to use Splash in `pga.py` spider script, the following settings have to be in the `settings.py`
```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
# For Windows & Mac, use the IP address instead of localhost 
SPLASH_URL = 'http://localhost:8050' 
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```

(**Optional**) Depending on the scenario, basic page restriction can be bypassed using the following packages along with their settings. They can be used together or separately as they already have different and unique priority values but make sure to put in the `DOWNLOADER_MIDDLEWARES` section the corresponding settings. 

- The simplest way to legit requests towards the website is to change the User-Agent. This can be done statically in `settings.py` file by initializing this parameter. 
```python 
USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
```

- [`scrapy-user-agents`](https://pypi.org/project/scrapy-fake-useragent/) can be used to automate picking a random User-Agent from a pull of pre-defined user agent. Install it via `pip` and add the following settings in `DOWNLOADER_MIDDLEWARES` section
```bash 
pip install scrapy-user-agents
```
```python
#....
'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
#....
```

- [`scrapy-proxy-pool`](https://pypi.org/project/scrapy-proxy-pool/) can also be used to skirt firewall rules by the use of Proxies. Install it via `pip` and add the following settings in the `DOWNLOADER_MIDDLEWARES` section
```bash 
pip install scrapy-proxy-pool
```
```python
#....
'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
#....
```
## Usage 
Before running this command, make sure that the Docker container has run successfully. Go to the current project and run the following command. The output will be generated as a CSV file  [`yellow-page-data.csv`](https://github.com/naivomah3/yellowpage-harvesting/blob/master/yellow-page-data.csv). 
Take a look at the scrapped data sample having 4000+ organizations available [here](https://github.com/naivomah3/yellowpage-harvesting/blob/master/yellow-page-data.csv)
```bash
scrapy crawl pga -o yellow-page-data.csv
```
To generate your own spider, use the following command. For more details, use the [documentation](https://docs.scrapy.org/en/latest/topics/commands.html) 
```bash
scrapy genspider yourspider yourdomain.com
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
