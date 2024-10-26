from unittest.mock import patch, Mock
from src.external_api import converts_currency


@patch('requests.get')
@patch('src.external_api.os.getenv')
def test_external_api(mock_getenv, mock_get):
    mock_getenv.return_value = 'valid_api_key'


    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'result': 0.0}
    mock_get.return_value = mock_response

    assert converts_currency("USD", "RUB", 100) == 0.0

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "valid_api_key"},
        params={'to': 'USD', 'from': 'RUB', 'amount': 100}
    )
