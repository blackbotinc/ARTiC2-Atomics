from blackbot.core.utils import get_path_in_package
from blackbot.core.srv.atomic import Atomic
from terminaltables import SingleTable

import os
import json

class Atomic(Atomic):
    def __init__(self):
        self.name = 'Impact/cmd'
        self.controller_type = ''
        #self.external_id = ''
        self.version = ''
        self.language = 'boo'
        self.description = self.get_description()
        self.last_updated_by = 'Blackbot, Inc. All Rights reserved'
        self.references = ["System.Management.Automation"]
        self.options = {
            'Atomic': {
                'Description'   :   'Atomic test you want to execute',
                'Required'      :   True,
                'Value'         :   '',
            },
        }

    @property
    def blackbot_id(self):
        global alias_map
        alias_map = self.get_alias_map()

        if self.options['Atomic']['Value'] not in alias_map:
            raise Exception('Atomic test does not exist: {}'.format(self.options['Atomic']['Value']))

        ttp = alias_map[self.options['Atomic']['Value']]
        return ttp

    @property
    def external_id(self):
        external_id = self.blackbot_id
        external_id = external_id.split('-')[0]

        return external_id


    def payload(self):
        with open(get_path_in_package('core/srv/ttp/art/src/cmd_prompt.boo'), 'r') as ttp_src:
            src = ttp_src.read()
            posh_script = get_path_in_package(f'core/srv/ttp/art/cmd_scripts/impact/{self.options["Atomic"]["Value"]}')

            with open(posh_script) as posh_ps1:
                src = src.replace("CMD_SCRIPT", posh_ps1.read())
                
                return src

    def walking_in_directory(self):
        path = get_path_in_package('core/srv/ttp/art/cmd_scripts/impact/')

        (root, _, filenames) = next(os.walk(path))
        return (root, _, filenames)

    def get_description(self):
        root, _, scripts = self.walking_in_directory()
        scripts.sort()

        full_description = {}
        for s in scripts:
            with open(root + s) as text:
                head = [next(text) for l in range(2)]
                technique_name = head[0].replace('#TechniqueName: ', '').strip('\n')
                atomic_name = head[1].replace('#AtomicTestName:', '').strip('\n')

                if technique_name not in full_description:
                    full_description[technique_name] = [(atomic_name, s)]
                else:
                    full_description[technique_name].append((atomic_name, s))
        
        description_display = ''
        table_data = []
        for key, values in full_description.items():
            table_data.append([f'\n#{key}', ''])
            
            for ttp_variant in values:
                table_data.append([f'  {ttp_variant[0]}', ttp_variant[1]])

        table = SingleTable(table_data, title='Atomics')
        table.inner_column_border = False
        table.inner_heading_row_border = False
        table.inner_row_border = False
        table.outer_border = False

        description_display += table.table

        return description_display 


    def get_alias_map(self):
        root, _, scripts = self.walking_in_directory()
        scripts.sort()

        alias_map = {}
        for s in scripts:
            alias_map[s] = f'{s}'

        return alias_map





