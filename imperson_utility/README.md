# ImpersonUtility

  A class that enable impersonation on Windows
  1. Create object: WinUtil("david") 
  2. open()
  3. execute your file operation 
  4. close(), with try-finlly
  
Created and tested on Python 3.9 

secret.json:
{
  "account": [
    {
      "user": "username",
      "password": "********",
      "domain": "IDIR"
    }
  ]
}
