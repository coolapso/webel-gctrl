Simple script to control webel-online.se GCTRL power outlets from the CLI

These power outlets are used to power on car heaters when it's cold outside. I only know that this is used in my neighborhood and have no clue if this would be useful for anyone else.

If you stumble here and actually find this useful and know that it could be beneficial for more people, just let me know, and I will definitely rewrite it in a more end-user-friendly way, such as Home Assistant automations or other better and cooler ways!

## Usage

**Turn on**
```
python gctrl.py on --username ${GCTRL_USERNAME} --password ${GCTRL_PASSWORD}
```

**Turn off**
```
python gctrl.py off --username ${GCTRL_USERNAME} --password ${GCTRL_PASSWORD}
```

**Check status**
```
python gctrl.py status --username ${GCTRL_USERNAME} --password ${GCTRL_PASSWORD}
```
