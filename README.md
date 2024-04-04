Setup:
    
    Go to the Google Cloud Console.
    Create a new project or select an existing one.
    Go to the "APIs & Services > Dashboard" section.
    Click "ENABLE APIS AND SERVICES" to search for and enable the Google Drive API for your project (I did all, but that might not be neccessary).
    Go to "Credentials" on the sidebar, click "Create credentials", and choose "OAuth client ID".
    If prompted, configure the consent screen.
    For application type, select "Desktop app".
    Give your client a name and click "Create".
    Download credentials, add into same directory as main.py.
    Add adress to test users for credentials / project.


Dependecies:

pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Usage:

    Use any console line argument to force reauth.