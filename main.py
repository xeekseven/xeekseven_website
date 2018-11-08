
import xeekwebsite_server
if __name__=='__main__':
    app = xeekwebsite_server.creat_app()
    app.run(port=5555)