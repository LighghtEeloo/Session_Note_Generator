import json
import shutil


default_dir_schema = 'schema.json'

class Session:
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

if __name__ == "__main__":
    session = Session(default_dir_schema).load().create().dump()
