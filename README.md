Creates a webservice for Windows x64 to update your duckdns entry every 10 minutes. Also supports adding custom server or my current server if you don't have one.
#
1) Install python 3.23 or above in C:\Program FIles\Pyth...
#
2) Force modules to install in python path above by running below command, modify path as needed [eg ``..\Python313\..`` may differ in your case]

    ```"C:\Program Files\Python313\python.exe" -m pip install requests schedule load_dotenv --target="C:\Program Files\Python313\Lib\site-packages"```
#
3) Edit ``.env`` file Variables
    ```
    DUCKDNS_DOMAIN=yourDuckDNSDomainName  #example 'smith.duckdns.org' will be smith --everything after . should be excluded
    
    DUCKDNS_TOKEN=yourDuckDNSToken #example abcs5fe3-sf4g4h56-rtry66-t543
    
    SERVER_URL=https://stillkonfuzed.com/DDNS/index.php # If you have a custom server then replace it. else leave it
    
    SECRET_KEY=YourSecret1234Changed #example AppleNoHashOrStupiSymbols ->
        this will generate YourSecret1234.json when you visit https://stillkonfuzed.com/DDNS/index.php?download=Your_secret1234
        It will have your ip address just in case duckdns fails. (serves as backup for worst case scenario)
    ```
#
4) Run CMD (Open Command Prompt as Administrator) and change to your folder

    ``cd C:\Development\DuckDNSUpdaterPy or C:\DuckDNSUpdaterPy ``
#
5) Install Service

     ``duckdns-service-WinSW-x64.exe install duckdns-service.xml``
   
    And start

    ``duckdns-service-WinSW-x64.exe start duckdns-service.xml``
#

6) WHEN STOP/Restart/Uninstall IS REQUIRED
    ```
    duckdns-service-WinSW-x64.exe stop duckdns-service.xml
    duckdns-service-WinSW-x64.exe restart duckdns-service.xml
    duckdns-service-WinSW-x64.exe uninstall duckdns-service.xml
    ```

#
End - if errors -> see logs folder in the same folder you have the cron.py

#
My Server : https://stillkonfuzed.com/DDNS/index.php
