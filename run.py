import os
from az_app.views.admin_views_route import mayapp

'''
    For a sample, at the start of the application, this translation services are launched
    The one listen on port : 8024 is the SPANISH-WIXARIKA service and
    The second one listen on port : 8042 is the WIXARIKA-SPANISH service and
    
    ===========ADDITIONAL INFORMATION (This command allows to detect service running on server and their ports)=========
    INSTALL IF NOT YET : sudo apt-get install lsof
    HOW TO USE IT      : sudo lsof -i :port  (this command will display the service running on the port you specify
    
    HOW TO STOP A SERVICE : fuser -k port/tcp
    TO STOP SPANISH-WIXARIKA SERVICE : fuser -k 8024/tcp
    
    
    
'''
# SPANISH-WIXARIKA
os.system("/opt/wixarika/mosesdecoder/bin/moses -f /opt/wixarika/working/binarised-model/moses.ini --server --server-port 8024 &")
# os.system("/opt/wixarika/mosesdecoder/bin/moses -f /opt/wixarika/workingWS/binarised-model/moses.ini --server --server-port 8042 &")


if __name__ == "__main__":

    mayapp.run(debug=True)

