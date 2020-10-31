from Schema import Schema, default_dir_schema
from Phraser import *

if __name__ == "__main__":
    schema = Schema(default_dir_schema).load()
    schema.input()
    schema.dump()
    phr = Phraser().add_schema(schema)
    phr.apply_schema()
    phr.output(verbose=False)
