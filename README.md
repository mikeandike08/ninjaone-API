# ninjaone-API
A simple NinjaOne API Wrapper

## Requirements ##
- Client ID, and Secret Key from NinjaOne, consult to the [NinjaOne Documentation](https://app.ninjaone.com/apidocs-beta/core-resources) for more info.
- Have Pip package requests installed

## DISCLAIMER ##
- This will not be maintained
  
- Only supports GET requests for now

- run_device_script has not been tested, problems most likely will arise with that.

## Example Usage ##
```
client = NinjaAPI(CLIENT_ID, SECRET_KEY)

# Returns a dict of all the network
network_interfaces = client.query_network_interfaces()
```
