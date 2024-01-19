import uvicorn
import dotenv
dotenv.load_dotenv()

def write_pid():
    import os
    pid = os.getpid()
    with open("./chatbot.pid","w+") as f:
        print(f"write pid {pid} to file")
        f.write(str(pid))
        


if __name__ == '__main__':
    from supports.facerander.script import import_lib
    import_lib()
    write_pid()
    uvicorn.run("app.server.app:app", host="0.0.0.0", port=5002, reload_dirs="./")
