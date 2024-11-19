#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth


class AdGuardClient:
    def __init__(self, url, username, password):
        self.url = url
        self.auth = HTTPBasicAuth(username, password)
        self.headers = {
            'Content-Type': 'application/json'
        }

    def list_rewrites(self):
        response = requests.get(
            f'{self.url}/control/rewrite/list', headers=self.headers, auth=self.auth)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch rewrites: {response.text}")
        return response.json()

    def add_rewrite(self, rewrite):
        response = requests.post(
            f'{self.url}/control/rewrite/add', json=rewrite, headers=self.headers, auth=self.auth)
        if response.status_code != 200:
            raise Exception(f"Failed to add rewrite: {response.text}")

    def delete_rewrite(self, rewrite):
        response = requests.post(
            f'{self.url}/control/rewrite/delete', json=rewrite, headers=self.headers, auth=self.auth)
        if response.status_code != 200:
            raise Exception(f"Failed to delete rewrite: {response.text}")


def manage_rewrites(data):
    servers = data['servers']
    rewrites = data['rewrites']
    state = data['state']

    changed = False
    errors = []

    for server in servers:
        client = AdGuardClient(
            server['url'], server['username'], server['password'])
        try:
            current_rewrites = client.list_rewrites()
        except Exception as e:
            errors.append(f"Error listing rewrites for server {
                          server['url']}: {str(e)}")
            continue

        if state == 'present':
            changed, errors = handle_present_state(
                client, rewrites, current_rewrites, changed, errors, server['url'])
        elif state == 'absent':
            changed, errors = handle_absent_state(
                client, rewrites, current_rewrites, changed, errors, server['url'])

    if errors:
        return True, changed, errors
    return False, changed, None


def handle_present_state(client, rewrites, current_rewrites, changed, errors, server_url):
    for rewrite in rewrites:
        if rewrite not in current_rewrites:
            try:
                client.add_rewrite(rewrite)
                changed = True
            except Exception as e:
                errors.append(f"Error adding rewrite {
                              rewrite} to server {server_url}: {str(e)}")
    return changed, errors


def handle_absent_state(client, rewrites, current_rewrites, changed, errors, server_url):
    for rewrite in rewrites:
        if rewrite in current_rewrites:
            try:
                client.delete_rewrite(rewrite)
                changed = True
            except Exception as e:
                errors.append(f"Error deleting rewrite {
                              rewrite} from server {server_url}: {str(e)}")
    return changed, errors


def main():
    module_args = dict(
        servers=dict(type='list', elements='dict', required=True, options=dict(
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
        )),
        rewrites=dict(type='list', elements='dict', required=True),
        state=dict(type='str', choices=[
                   'present', 'absent'], default='present')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    is_error, has_changed, errors = manage_rewrites(module.params)

    if is_error:
        module.fail_json(msg="Error managing rewrites", errors=errors)
    else:
        module.exit_json(changed=has_changed, errors=errors)


if __name__ == '__main__':
    main()
