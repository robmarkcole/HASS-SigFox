# HASS-SigFox
[SigFox](https://www.sigfox.com/en) component for [Home-Assistant](https://home-assistant.io/), adding a [sensor]() for each SigFox device. Place the `custom_components` folder in your configuration directory (or add its contents to an existing custom_components folder). The component uses the [SigFox REST API](https://resources.sigfox.com/document/backend-api-documentation), and by default refreshes the data in the sensor every 30 seconds.  

Add to your config:
```yaml
sensor:
  - platform: sigfox
    login: your_login
    password: your_password
```

Where `your_login` and `your_password` are not the same as the credential you use to access Sigfox backend. Required are your API access credentials:

1. Log into [Sigfox backend](https://backend.sigfox.com)
2. Go to Groups
3. Select group
4. API ACCESS.
5. Click on 'new' and create new access entry.

Note that you can adjust the data refresh rate by [setting](https://home-assistant.io/docs/configuration/platform_options/#scan-interval) the `scan_interval` in the above config.

## Payload
It is recommended that you configure your SigFox device to send JSON formatted data in the payload. For example, I am using a micropython board and sending the time in the payload `{time:1151}`. In Home-Assistant my sigfox sensor is named `sigfox_4d30a7` and I can access the time in the payload using the template `{{states.sensor.sigfox_4d30a7.state.time}}`. I created a template sensor with the following config:



<p align="center">
<img src="https://github.com/robmarkcole/HASS-SigFox/blob/master/images/usage.png" width="500">
</p>
