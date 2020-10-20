

def get_db_query_service_url():
    """
    :return: URL to the database SPARQL query service.
    """
    return 'http://staging.mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql'


def get_db_api_url():
    """
    :return: URL to the database API service.
    """
    return 'http://staging.mobilitydatabase.org/w/api.php'
