from io import StringIO
import json
import shutil


default_dir_schema = 'schema.json'

class Schema:
    """
    {[clear] -> load} -> [create] -> (safe) edit -> dump
    note: [] is optional, {} is init

    states: loaded -> created
    """
    def __init__(self, dir_schema: str=None) -> None:
        self.schema = {}
        self.info = []
        self.paragraph = []
        self.summary = []
        self.loaded = False
        self.identical = False
        self.dir_schema = default_dir_schema if dir_schema is None else dir_schema
    def clear(self):
        self.schema.clear()
        return self
    def load(self, output=False):
        with open(self.dir_schema, 'r') as f:
            self.schema = json.load(f)
        if output:
            print(json.dumps(self.schema, indent=4))
        try:
            self.info = self.schema['info']
            self.paragraph = self.schema['paragraph']
            self.summary = self.schema['summary']
        except KeyError as e:
            print(f"{e}")
            print("Error: broken schema.")
            self.loaded = False
            self.clear()
        else:
            self.loaded = True
        return self
    def create(self):
        if self.loaded:
            self.schema.update({'session':{
                'info': {}.fromkeys(self.info, ""),
                'para_list': [],
                'summary': {}.fromkeys(self.summary, "")
            }})
        else:
            print("Error: create while unloaded.")
        return self
    def dump(self):
        if self.loaded:
            shutil.copyfile(self.dir_schema, f'{self.dir_schema}.bak')
            with open(self.dir_schema, 'w') as f:
                json.dump(self.schema, f, indent=4)
        else:
            print("Error: dump while unloaded.")
        return self

    ''' is_ utils'''
    def is_identical(self):
        if not self.loaded:
            return False
        for prop in ['info', 'summary']:
            for item in self.schema[prop]:
                if not item in self.schema['session'][prop].keys():
                    return False
        for item_ses in self.schema['session']['para_list']:
            for item in item_ses:
                if not item in self.schema['paragraph']:
                    return False
        return True
    @staticmethod
    def valid_str(string: str):
        return string != "" and not string.isspace()

    def input_prop_item(self, prop: str, item: str):
        previous = self.schema['session'][prop][item]
        filling = input(f'{item} {f"({previous})" if self.valid_str(previous) else ""}: ')
        self.schema['session'][prop][item] = filling if not (filling.isspace() or filling == "") else previous

    def input_prop(self, prop: str):
        for item in self.schema[prop]:
            self.input_prop_item(prop, item)
    
    def input_para_item(self, index: int, item: str):
        para_list = self.schema['session']['para_list']
        previous = para_list[index][item]
        filling = input(f'{item} {f"({previous})" if self.valid_str(previous) else ""}: ')
        para_list[index][item] = filling if not (filling.isspace() or filling == "") else previous

    def input_para(self, index: int=None):
        if index is None:
            para_list = self.schema['session']['para_list']
            index = len(para_list)
            if index == 0:
                para_list.append({}.fromkeys(self.paragraph, ""))
                print("Appended para.")
            else:
                index -= 1
            print(f"Inputting: para {index}.")
        for item in self.paragraph:
            self.input_para_item(index, item)

    def input(self) -> bool:
        """
        create and continue if not identical
        """
        if not self.is_identical():
            self.create()
        self.input_prop('info')
        while True:
            self.input_para()
            filling = input('Another paragraph? [Y/n] ')
            if filling.lower() != 'y':
                break
        self.input_prop('summary')
        return True

    def output(self, verbose: bool=False) -> None:
        if verbose:
            print(json.dumps(self.schema, indent=4))
        else:
            print(json.dumps(self.schema['session'], indent=4))

    @staticmethod
    def dumps(obj):
        return json.dumps(obj, indent=4)

    def content_fixed(self) -> dict:
        if not (self.loaded and self.is_identical()):
            return None
        content = {}
        content.update(self.schema['session']['info'])
        content.update(self.schema['session']['summary'])
        content.update(self.schema['session']['para_list'][0])
        # Todo: remove para_list
        # print(json.dumps(content, indent=4))
        return content

if __name__ == "__main__":
    schema = Schema(default_dir_schema).load()
    # schema.output(verbose=True)
    # schema.input()
    # schema.output()
    schema.content()
    schema.dump()
