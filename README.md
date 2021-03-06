# Dola
Dola is a Python-based bot specialising in Splatoon and [Slapp](https://github.com/kjhf/SplatTag) but also comes with some utility functions.
Code on [Github](https://github.com/kjhf/DolaBot).

Import prefix is `DolaBot`.

## Requirements
- Python 3.9+

## Bot Setup
* Create a `.env` in the repository root with the following values:

```py
# This is the bot's Discord token from the Developer API page.
BOT_TOKEN="xxxx.xxxx.xxxx"
# This is the bot's Discord Id.
CLIENT_ID=123456789
# This is your Discord Id.
OWNER_ID=123456789
# Path to SplatTagConsole for Slapp things
SLAPP_CONSOLE_PATH=".../SplatTagConsole.dll"
# Path to the Slapp App Data folder
SLAPP_DATA_FOLDER=".../SplatTag"
# Discord id of a logging channel (optional)
LOGS_CHANNEL=870436255777837098
# Bot command symbol (optional). 
# '~' by default or not specified.
# Recommend using a different symbol for local testing.
BOT_COMMAND_SYMBOL="+"
# Path to the Google Sheets service account json definition
# e.g. https://console.cloud.google.com/iam-admin/serviceaccounts/details/...
MIT_GOOGLE_CREDS_FILE_PATH=".../SplatTag/dola-gsheet-access.json"
# Discord id of the MIT Webhook channel
MIT_WEBHOOK_CHANNEL=743901312718209154
# Discord id of the MIT Webhook User
MIT_WEBHOOK_USER_ID=927297819159711744
# Google sheet id of the verification spreadsheet
MIT_GOOGLE_SHEET_ID="1aaaaaaa_aaaaa"
# Google sheet page index for cycle (0 is first sheet/page of the workbook)
MIT_GOOGLE_SHEET_PAGE_INDEX=0
# Google sheet page id for the friend codes
MIT_FC_PAGE_ID=123456
###
# Remember additional values should be included in the Dockerfile ...
###
```

You must also set the relevant env values for [SlappPy](https://github.com/kjhf/SlappPy)

### Dockerised setup (not required)
* The Dockerfile assumes SplatTag is under /bin. Adjust if necessary.
  * First, grab SplatTag and put it into the Docker build context, e.g.
  * `. GrabSplatTag.bat`
  
THEN
* With Docker Desktop running,
* `docker build --no-cache --pull --tag="slate.azurecr.io/dola:latest" -f Dockerfile .`

### Test or run with 
* `docker run -t -d slate.azurecr.io/dola`
* Recommended tests:
  * Expected result, e.g. "slate"
  * Query that has players and teams, e.g. "squid" - should be green
  * Multiple teams query e.g. "squid --team" - should be gold
  * Multiple players query "squid --player" - should be blue
  * Test reacts (1 and 20)
  * Single player result, e.g. react to the above - should be dark gold
  * Single team, e.g. react to the above - should be dark blue
  * Test a plus member, e.g. Sendou


### Update Azure Image with
After the build step, (note these commands are long in this window!)
* `az login`
* `az acr login --name slate`
* `docker push slate.azurecr.io/dola:latest`
* To stop:
  * `az container stop --name dola --resource-group slapp-resource-group`
* To recreate from scratch (this should also re-pull the image)
  * `az container create --resource-group slapp-resource-group --name dola --image slate.azurecr.io/dola:latest`
  * The username is slate, and the password is in the ACR access keys.
* To start:
  * `az container start --name dola --resource-group slapp-resource-group`

### Azure Cloud setup from scratch
```shell
ACR_NAME=slate.azurecr.io
SERVICE_PRINCIPAL_NAME=acr-service-principal
ACR_REGISTRY_ID=$(az acr show --name $ACR_NAME --query id --output tsv)
SP_APP_ID=$(az ad sp show --id http://$SERVICE_PRINCIPAL_NAME --query appId --output tsv)
echo "Service principal ID: $SP_APP_ID"
SP_PASSWD=$(az ad sp create-for-rbac --name http://$SERVICE_PRINCIPAL_NAME --scopes $ACR_REGISTRY_ID --role acrpull --query password --output tsv)
echo "Service principal password: $SP_PASSWD"
az container create --resource-group slapp-resource-group --name dola --image slate.azurecr.io/dola
```
