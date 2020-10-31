from Session import Session, default_dir_schema

if __name__ == "__main__":
    session = Session(default_dir_schema).load()
    session.output(verbose=True)
    session.input()
    session.output()
    session.dump()
