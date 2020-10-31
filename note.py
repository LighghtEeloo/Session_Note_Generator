from Schema import Schema, default_dir_schema
from Phraser import *

if __name__ == "__main__":
    schema = Schema(default_dir_schema).load()
    # schema.input()
    # schema.dump()
    phr = Phraser().add_schema(schema)
    print(phr.phrases)
    phr.apply_schema()
    print(phr.phrases)
    phr.output(verbose=True)
