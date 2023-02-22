# VK-Comics #

Script publishes [xkcd](https://xkcd.com) comics in [vk](http://vk.com) group

## How to install ##

Python should be already installed.

Use `pip`(or `pip3` for Python3) to install dependencies:

```commandline
pip3 install -r requirements.txt
```

Recommended using [virtualenv/venv](https://docs.python.org/3/library/venv.html)

## Launch ##
1) Login/Register in [vk.com](http://vk.com) and create a group
2) Get [group id](https://regvk.com/id/)
3) Create [an app](https://dev.vk.com) and get client_id
4) Get [vk access token](https://vk.com/dev/implicit_flow_user)
4) Add to .env file:
    - `IMAGE_PATH` - path to images folder
    - `GROUP_ID` - received group id
    - `ACCESS_TOKEN` - received access token
    
Run `main.py` with the comic link as an argument.

```commandline
python3 main.py https://xkcd.com/353/
```

If no argument is given, a random comic will be published.

```commandline
python3 main.py
```
