#!bin/bash
curl -X POST https://we303v9ck8.execute-api.eu-west-1.amazonaws.com/Prod/marearts_anpr_eu \
     -H "Content-Type: image/jpeg" \
     -H "x-api-key: your-api-key" \
     -H "user-id: your-user-id" \
     --data-binary "@./path/upload.jpg"
