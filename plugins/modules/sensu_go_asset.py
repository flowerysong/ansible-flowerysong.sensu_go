#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: sensu_go_asset
author: "Cameron Hurst (@wakemaster39)"
short_description: Manages Sensu assets
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/assets/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.object
options:
  download_url:
    description:
      - The URL location of the asset.
    required: true
  sha512:
    description:
      - The checksum of the asset.
    required: true
  filters:
    description:
      - A set of Sensu query expressions used to determine if the asset should be installed.
    type: list
    default: []
  headers:
    description:
      - List of headers access secured assets.
    type: list
    default: []
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import SensuObject


class SensuAsset(SensuObject):
    def __init__(self, module):
        super(SensuAsset, self).__init__(module)

        self.path = '/assets/{0}'.format(self.params['name'])

        for key in (
            'download_url',
            "sha512",
            "filters",
            "headers"
        ):
            if self.params[key] is not None:
                if key == "download_url":
                    self.payload["url"] = self.params[key]
                else:
                    self.payload[key] = self.params[key]

    # def compare(self):
    #     """
    #     This override is nessecary because sensu go is not respecting their API?
    #     """
    #     for key in self.payload:
    #         if key == "filters":
    #             obj = self.server_object.get(key)
    #             for k,v in self.payload[key].items():
    #                 if "{0} == '{1}'".format(k,v) not in obj:
    #                     return False
    #         else:
    #             if self.payload[key] != self.server_object.get(key):
    #                 return False
    #     return True

def main():
    argspec = SensuAsset.argument_spec()
    argspec.update(
        dict(
            download_url=dict(
                required=True,
            ),
            sha512=dict(
                required=True,
            ),
            filters=dict(
                type='list',
            ),
            headers=dict(
                type='list',
            ),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    check = SensuAsset(module)
    result = check.reconcile()
    module.exit_json(changed=result['changed'], check=result['object'])


if __name__ == '__main__':
    main()
