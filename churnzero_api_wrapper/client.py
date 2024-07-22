import requests
from requests import Session
from requests import HTTPError
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from churnzero_api_wrapper.logger import setup_logger

logger = setup_logger()
__version__ = "0.2.0"


class HTTPClient(Session):
    """
    A client wrapper for the ChurnZero HTTP API.

    This class provides methods to interact with the ChurnZero HTTP API endpoints.
    It handles authentication, making requests, and processing responses to the following objects:

    - Accounts
    - Contacts
    - Events

    Args:
        app_key (str): The ChurnZero API key.
        base_url (str): The base URL of the ChurnZero API.
        timeout (int, optional): :obj:`TimeoutHTTPAdapter` timeout value. Defaults to 5.
        total (int, optional): :obj:`Retry` total value. Defaults to 5.
        backoff_factor (int, optional): :obj:`Retry` backoff_factor value.Defaults to 30.
        ssl_verify (bool, optional): Whether to verify SSL certificates. Defaults to True.
    """

    def __init__(
        self,
        app_key: str,
        host: str,
        timeout: int = 5,
        total: int = 5,
        backoff_factor: int = 30,
        ssl_verify: bool = True,
    ):
        super().__init__()

        self.app_key = app_key
        self.host = host
        adapter = TimeoutHTTPAdapter(
            timeout=timeout,
            max_retries=Retry(
                total=total,
                status_forcelist=[429, 500, 502, 503, 504],
                backoff_factor=backoff_factor,
            ),
        )
        self.mount("https://", adapter)
        if not ssl_verify:
            logger.warning("SSL verification is disabled.")
            self.mount("http://", adapter)
            requests.packages.urllib3.disable_warnings()

        self.headers.update(
            {
                "User-Agent": f"churnzero-python-api-wrapper/{__version__}",
            }
        )
        self.__build_resources()

    def __build_resources(self):
        """Add each resource with a reference to this instance."""
        for k, v in globals().items():
            try:
                for base in v.__bases__:
                    if base.__name__ not in ["Collection", "Resource"]:
                        continue

                    v._client = self
                    setattr(self, k, v)

            except AttributeError:
                continue

    def request(
        self,
        param_data: dict,
        method: str = "GET",
    ):
        """
        Make a request to the ChurnZero API.

        Args:
            method (str, optional): The HTTP method to use. Defaults to "POST".
            params (dict, optional): The query parameters for the request. Defaults to None.
            data (dict, optional): The request payload. Defaults to None.

        Returns:
            dict: The JSON response from the API, or None if an error occurred.
        """

        data = {"appKey": self.app_key}
        params = {**data, **param_data}
        response = super().request(method, url=self.host, params=params)
        try:
            if response.status_code == 200:
                logger.info(f"HTTP Code: {response.status_code}. Request successful.")
            response.raise_for_status()
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 422:
                logger.error(
                    f"HTTP Code:{status_code} Unprocessable entity error occurred. Inspect your parameters: {e.response.text}"
                )
            else:
                logger.error(
                    f"Returned exception code: {status_code}. Exception message: {e}"
                )

    def _set_object_attributes(self, entity: str, object: dict) -> object:
        """
        Set attributes for either the account or contact objects. This is a helper method for the set_account_attributes and set_contact_attributes methods.

        Args:
            entity (str): The entity to set attributes for. Either "account" or "contact".
            **kwargs: Additional keyword arguments to include in the request data object for the corresponding object.
        """
        data = {
            "entity": entity,
            "action": "setAttribute",
        }
        request_data = {**data, **object}
        return self.request(param_data=request_data)

    def set_account_attributes(self, account: dict) -> object:
        """
        Sets the attributes of an account in the ChurnZero API. If the account does not exist, the account is created.

        Args:
            account (dict): A dictionary containing the account information.
                The dictionary should have the following keys:
                - "externalAccountId" (str): The unique identifier for the account.
                - attr_XXXX (optional) (str): The custom field to be updated,
                  prefixed by "attr_", to set the corresponding attribute of the object.

        Returns:
            The response from the ChurnZero API.
        """
        return self._set_object_attributes(entity="account", object=account)

    def set_contact_attributes(self, contact: dict) -> object:
        """
        Sets the attributes of a contact in the ChurnZero API. If the contact does not exist, the contact is created.

        Args:
            contact (dict): A dictionary containing the contact information and attributes to be set.
                The dictionary should have the following structure:
                {
                    "externalContactId": "The unique identifier for the contact",
                    attr_XXXX (optional): "The custom field to be updated prefixed by 'attr_' to set the corresponding attribute of the object"
                }

        Returns:
            The response from the ChurnZero API.

        """
        return self._set_object_attributes(entity="contact", object=contact)

    # Add more methods for other API endpoints as needed
    def track_event(self, event: dict):
        """
        Track an event for a specific account and contact.

        Args:
            # Example event dict input
            event = {
                "accountExternalId": "Account External ID",
                "contactExternalId": "Contact External ID",
                "eventDate": "2021-09-01T12:00:00Z" ISO 8601 formatted date and time.,
                "eventName": "Event Name",
                "description":  "A description of this particular event (ie. blog title). Note: There is a 255 character limit on this field."
                "quantity": "The number related to this event. (ie. Commonly used to track things like email sent, etc)",
                "allowDupes": "true | false. By default ChurnZero ignores duplicate events (same Date, Account, Contact and Description). Set this parameter to "true" to allow duplicate events.",
                cf_XXXX (optional): "The custom field to be updated prefixed by "cf_". You must create this custom field in Admin > Custom Fields > Events  BEFORE you begin sending data for this field, or it will end up in the Description field of the Event"
            }

        Returns:
            dict: The response from the API, or None if an error occurred.
        """
        data = {
            "action": "trackEvent",
        }
        return self.request(param_data={**data, **event})


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, timeout, *args, **kwargs):
        """TimeoutHTTPAdapter constructor.

        Args:
            timeout (int): How many seconds to wait for the server to send data before
                giving up.
        """
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        """Override :obj:`HTTPAdapter` send method to add a default timeout."""
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)
