import requests

def search_location(city, county, country, limit=1, format_type='jsonv2'):
    """
    Search for a location using the Nominatim API.

    Args:
        city (str): Street name or address to search.
        county (str): County or region to refine the search.
        country (str): Country to refine the search.
        limit (int): Number of results to return (default is 1).
        format_type (str): Response format, default is 'jsonv2'.

    Returns:
        list: JSON response from the API if successful.
        None: If the request fails.
    """
    # Base URL for Nominatim API
    url = 'https://nominatim.openstreetmap.org/search.php'

    # Headers
    headers = {
        'referer': 'https://nominatim.openstreetmap.org/ui/search.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    # Parameters
    params = {
        'city': city,
        'county': county,
        'country': country,
        'limit': limit,
        'format': format_type,
    }

    try:
        # Make the API request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes (4xx or 5xx)

        # Return the parsed JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        # Log the error (can use logging for production)
        print(f"An error occurred: {e}")
        return None
