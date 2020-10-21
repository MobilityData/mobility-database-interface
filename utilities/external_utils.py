

def get_staging_sparql_url():
    """
    :return: URL to the staging SPARQL query service of the staging database.
    """
    return 'http://staging.mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql'


def get_production_sparql_url():
    """
    :return: URL to the SPARQL query service of the production database.
    """
    return 'http://mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql'


def get_staging_api_url():
    """
    :return: URL to the API service of the staging database.
    """
    return 'http://staging.mobilitydatabase.org/w/api.php'


def get_production_api_url():
    """
    :return: URL to the API service of the production database.
    """
    return 'http://staging.mobilitydatabase.org/w/api.php'
