# ChurnZero Python API Wrapper

This is a Python API wrapper for the ChurnZero HTTP API. It provides a convenient way to interact with the ChurnZero HTTP API platform. The following features are supported:

- Set Account Attributes (multi attributes only)
- Set Contact Attributes (multi attributes only)
- Track Events

Other features may be supported in the future.

> The wrapper only supports the HTTP API integrations documented on this page: [ChurnZero HTTP API](https://support.churnzero.com/hc/en-us/articles/360003183171-Integrate-ChurnZero-using-HTTP-API). REST features may be supported in the future.

**Note**: This is an unofficial API wrapper and is not affiliated with ChurnZero.

## Installation

To install the ChurnZero Python API Wrapper, you can use pip:

```shell
pip install churnzero_api_wrapper
```

## Usage

To use the ChurnZero Python API Wrapper, you need to import the `ChurnZeroClient` class from the package:

```python
from churnzero_api_wrapper import HTTPClient
```

Next, you need to create an instance of the `HTTPClient` class and provide your ChurnZero APP credentials:

```python
client = HTTPClient(app_key='{app_key}', host = "https://{domain}.churnzero.net/i")
```

Your app key and domain can be found in the ChurnZero dashboard under `Admin` -> `Data` -> `Application Keys` -> `Application Key & HTTP API Endpoint`.

Once you have created the client, you can start making HTTP API requests. For example, to set an Account attribute:

```python
account = {
    "externalAccountID": "12345",
    "attr{CustomAttribute1}": "Value1",
}
client.set_account_attributes(account)
```

To set a Contact attribute:

```python
contact = {
    "externalAccountID": "12345",
    "externalContactID": "67890",
    "attrFirstName": "Value1",
    "attrLastName": "Value2",
}

client.set_contact_attributes(contact)
```

To track an event:

```python
event = {
    "externalAccountID": "12345",
    "externalContactID": "67890",
    "eventName": "EventName",
    "description": "EventDescription",
    "eventDate": "2021-01-01T00:00:00Z",
}

client.track_event(event)
```

### Logging

To configure the logging level for the ChurnZero Python API Wrapper, you can use the `logging` module in Python. Here's an example of how to set the log level to `DEBUG`:

```python
import logging

# Set the log level to DEBUG
logging.getLogger().setLevel(logging.DEBUG)
# Set the log level to INFO
logging.getLogger().setLevel(logging.INFO)
# Set the log level to WARNING
logging.getLogger().setLevel(logging.WARNING)
# Set the log level to ERROR
logging.getLogger().setLevel(logging.ERROR)
```

> <font color="red">**WARNING**</font>: note that setting the log level to `DEBUG` will expose the `app_key` to logs due to ChurnZero's HTTP API configuration. It is recommended to only use the `DEBUG` log level for debugging purposes and not in production environments.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
