import requests
from collections import defaultdict

class NinjaAPI():

    def __init__(self, client_id, secret_key):
        self.base_url = 'https://api.ninjarmm.com'
        self.client_id = client_id
        self.secret_key = secret_key
        self.access_token = ''

    def get_token(self):
        url = f'{self.base_url}/ws/oauth/token'

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.secret_key,
            'scope': {
                'monitoring',
            }
        }

        response = requests.post(url, data=data)
        try:
            access_token = response.json()['access_token']
        except KeyError as e:
            return f'Invalid Token or Secret Key: {KeyError}'
        self.access_token = access_token
        return access_token

    def get_basic_devices(self, device_filter=''):
        """
        Get basic device information
        """
        return self.fetch_results(f'{self.base_url}/v2/devices?df={device_filter}')

    def get_detailed_devices(self, device_filter=''):
        """
        Get detailed device information
        """
        return self.fetch_results(f'{self.base_url}/v2/devices-detailed?df={device_filter}')

    def get_all_device_info(self, devices, mac):
        """
        Get all device info like id, organization_id, location_id, workstation, name, system_name, dns_name
        """

        for data in devices['devices']:
            if data['matchAttrValue'] == mac.upper():
                info = {
                    'id': data['id'],
                    'organization_id': data['organizationId'],
                    'location_id': data['locationId'],
                    'workstation': data['nodeClass'],
                    'name': data['displayName'],
                    'system_name': data['systemName'],
                    'dns_name': data['dnsName'],
                }
                return info
        return None
    
    def get_filtered_device_info(self, device_id=None, devices=None):
        """
        Get Specific device info like id, organization_id, location_id, workstation, name, system_name, dns_name
        Pass in device_id if you'd like to perform the search locally
        """
        if device_id:
            device_info = client.get_specific_device_info(device_id)
            system = device_info.get('system')
            info = {
                        'id': device_info.get('id'),
                        'organization_id': device_info.get('organizationId'),
                        'location_id': device_info.get('locationId'),
                        'workstation': device_info.get('nodeClass'),
                        'name': system.get('name'),
                        'system_name': device_info.get('systemName'),
                        'dns_name': device_info.get('dnsName'),
                        'model': system.get('model'),
                        'serialNumber': system.get('serialNumber'),
                        'chassisType': system.get('chassisType'),
                        'device_type': device_info.get('deviceType'),
                        'last_logged_user': device_info.get('lastLoggedInUser'),
                        'uid': device_info.get('uid')
                    }
            return info
        
        if devices:
            for data in devices['devices']:
                if data['matchAttrValue'] == mac.upper():
                    info = {
                        'id': data['id'],
                        'organization_id': data['organizationId'],
                        'location_id': data['locationId'],
                        'workstation': data['nodeClass'],
                        'name': data['displayName'],
                        'system_name': data['systemName'],
                        'dns_name': data['dnsName'],
                    }
                    return info
        return None

    def get_device_id_by_mac(self, mac):
        """
        Get the device ID from mac
        """
        search = self.search_device(mac)
        for data in search.get('devices'):
            if data['matchAttrValue'] == mac.upper():
                return data['id']
        return None

    def search_device(self, query, limit=1):
        """
        Search devices by a query (name, logged on user name, IP address etc)
        """
        return self.fetch_results(f'{self.base_url}/v2/devices/search?q={query}')

    def get_device_jobs(self, device_id):
        """
        Get the device Jobs through device ID
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/jobs')

    def get_last_logged_on_user(self, device_id):
        """
        Get the last logged on user by Device ID
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/last-logged-on-user')

    def get_device_processors(self, device_id):
        """
        Get the device processor information through Device ID
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/processors')
    
    def get_software_inventory(self, device_id):
        """
        Get the device inventory through Device ID
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/software')
    
    def get_device_volumes(self, device_id):
        """
        Get the Device Volumes through Device ID
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/volumes')
    
    def get_specific_device_info(self, device_id):
        """
        Get a specific Device Info through Device ID
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}')

    # Returns the url of the device dashboard
    def get_device_dashboard(self, device_id):
        """
        Get the Device Dashboard from Device ID
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/dashboard-url')

    def get_device_disks(self, device_id):
        """
        Get the devices disk by device ID
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/disks')
    
    def get_activity_log(self, device_id, activityType='', olderThan='', newerThan='', status='', pageSize=200):
        """
        Get the activity log of a device
            Optionally filtering:
            activityType: 'string'
            olderThan: older than specific activity id
            newThan: newer than specific activity id
        """

        params = {
            'activityType': activityType.upper() if activityType else None,
            'olderThan': olderThan if olderThan else None,
            'newerThan': newerThan if newerThan else None,
            'status': status.upper() if status else None,
            'pageSize': pageSize if pageSize else None
        }

        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/activities', params=params)

    def get_device_network_interface(self, device_id):
        """
        Get network interface from a device
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/network-interfaces')
    
    def get_custom_fields(self, device_id):
        """
        Get custom fields from a device
        """
        return self.fetch_results(f'{self.base_url}/v2/device/{device_id}/custom-fields')

    def list_software_products(self):
        """
        List software products
        """
        return self.fetch_results(f'{self.base_url}/v2/software-products')
    
    # ---------QUERIES ARE MORE VAGUE SEARCHES---------------
    # Using queries you can search for mor specifc values like name, id, location, organization etc

    # FORMAT - field {operator} value
    # Ex for deviceID - id = 1234

    def query_network_interfaces(self, device_filter=''):
        """
        Query for all network interfaces, optionally filtering device
        """
        return self.fetch_results(f'{self.base_url}/v2/queries/network-interfaces')

    def query_operating_system(self, device_filter=''):
        """
        query operating systems, optionally filtering device
        """
        return self.fetch_results(f'{self.base_url}/v2/queries/operating-systems?df={device_filter}')
    
    def query_device_health(self, device_filter=''):
        """
        Query device health, optionally filtering device
        """
        return self.fetch_results(f'{self.base_url}/v2/queries/device-health?df={device_filter}')
    
    def query_custom_fields(self, device_filter=''):
        """
        Query custom fields, optionally filtering device
        """
        return self.fetch_results(f'{self.base_url}/v2/queries/custom_fields?df={device_filter}')
    
    def query_disks(self, device_filter=''):
        """
        Query device disks, optionally filtering device
        """
        return self.fetch_results(f'{self.base_url}/v2/queries/disks?df={device_filter}')
    
    def query_volumes(self, device_filter=''):
        """
        Query device volumes, optionally filtering device
        """
        return self.fetch_results(f'{self.base_url}/v2/queries/volumes?df={device_filter}')
    
    def query_logged_on_users(self, device_filter=''):
        """
        Query logged on users, optionally filtering device
        """

        if self.access_token is None:
            return 'No access token found, please wait and try again'

        return self.fetch_results(f'{self.base_url}/v2/queries/logged-on-users?df={device_filter}')
    
    def query_software(self, device_filter=''):
        """
        Query the software, optionally filtering device
        """
        return self.fetch_results(f'{self.base_url}/v2/queries/software?df={device_filter}')
    
    def list_organization_locations(self, organization_id):
        """
        Get organization locations
        """
        return self.fetch_results(f'{self.base_url}/v2/organization/{organization_id}/locations')
    
    def list_location_custom_fields(self, organization_id, location_id):
        """
        Get a list of location custom fields
        """
        return self.fetch_results(f'{self.base_url}/v2/organization/{organization_id}/location/{location_id}/custom-fields')
 
    def organization_devices(self, organization_id):
        """
        Get the devices in a organization
        """
        return self.fetch_results(f'{self.base_url}/v2/organization/{organization_id}/devices')

    def organization_custom_fields(self, organization_id):
        """
        Get the organization custom fields
        """
        return self.fetch_results(f'{self.base_url}/v2/organization/{organization_id}/custom-fields')

    def organization_details(self, organization_id):
        """
        Get the organization details
        """
        return self.fetch_results(f'{self.base_url}/v2/organization/{organization_id}')

    def list_all_automation_scripts(self):
        """
        list all automation scripts available
        """
        return self.fetch_results(f'{self.base_url}/v2/automation/scripts')
    
    def run_device_script(self, device_id, payload):
        """
        # ----------Example payload-----------------
        # payload = {
        #   'type': 'ACTION',
        #   'id': 0,
        #   'uid': uuid,
        #   'parameters': 'string',
        #   'runAs': 'string'
        # }

        #------- PARAMS --------------
        # type: allowed values = ACTION, SCRIPT
        # id: script identifier
        # uid: build-in action identifier
        # parameters: action/script parameters
        # runAs: Credential role/identifier
        """

        if self.access_token is None:
            return 'No access token found, please wait and try again'

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Authorization': f'Bearer {self.access_token}'
        }

        return requests.post(f'{self.base_url}/v2/device/{device_id}/script/run', headers=headers, json=payload)
    
    def fetch_results(self, url, header='', payload='', params=''):
        header = {
            'Authorization': f'Bearer {self.access_token}'
        }

        if params:
            response = requests.get(url=url, headers=header, params=params)
        else:
            response = requests.get(url=url, headers=header)
        return response.json()
