
import xeekwebsite_server
if __name__=='__main__':
    app = xeekwebsite_server.creat_app()
    app.run(host='0.0.0.0',port=5555)