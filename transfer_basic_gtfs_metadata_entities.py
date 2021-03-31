import argparse
import json
from wikibaseintegrator import wbi_core, wbi_login
from wikibaseintegrator.wbi_config import config as wbi_config
from utilities.constants import SVC_URL, USERNAME, PASSWORD, ENGLISH


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transfer script")
    parser.add_argument(
        "--path-to-production-credentials",
        action="store",
        default="./production_credentials.json",
        help="Path to the production credentials.",
    )
    parser.add_argument(
        "--staging-entities",
        action="store",
        help="List of the staging entities to transfer to production.",
    )
    parser.add_argument(
        "--path-to-props-map",
        action="store",
        default="./properties_map.json",
        help="A map from staging to production of the properties required for the entities to transfer.",
    )
    parser.add_argument(
        "--path-to-entities-map",
        action="store",
        default="./entities_map.json",
        help="A map from staging to production of the entities to transfer.",
    )
    parser.add_argument(
        "--mode",
        action="store",
        choices=["create", "update"],
        help="Whether to perform entities creation or update their properties on the database.",
    )
    args = parser.parse_args()

    # Load production credentials
    with open(args.path_to_production_credentials) as f:
        production_credentials = json.load(f)
    production_username = production_credentials.get(USERNAME)
    production_password = production_credentials.get(PASSWORD)

    # Load properties map
    with open(args.path_to_props_map) as f:
        properties_map = json.load(f)

    # -------------------------
    # Collect data from staging
    # -------------------------

    # Set Wikibase Integrator config for staging
    wbi_config["MEDIAWIKI_API_URL"] = "http://staging.mobilitydatabase.org/w/api.php"
    wbi_config[
        "SPARQL_ENDPOINT_URL"
    ] = "http://staging.mobilitydatabase.org:8989/bigdata/sparql"
    wbi_config["WIKIBASE_URL"] = SVC_URL

    # Fetch data from staging for the entities to transfer
    staging_entities_data = {}
    for entity_id in args.staging_entities.split():
        entity_data = wbi_core.ItemEngine(item_id=entity_id)
        staging_entities_data[entity_id] = entity_data.get_json_representation()

    # ----------------------------------------
    # Transfer data from staging to production
    # ----------------------------------------

    # Set Wikibase Integrator config for production
    wbi_config["MEDIAWIKI_API_URL"] = "http://mobilitydatabase.org/w/api.php"
    wbi_config[
        "SPARQL_ENDPOINT_URL"
    ] = "http://mobilitydatabase.org:8989/bigdata/sparql"
    wbi_config["WIKIBASE_URL"] = SVC_URL

    # Create login instance to the production database
    login_instance = wbi_login.Login(
        user=production_username, pwd=production_password, use_clientlogin=True
    )

    # Create entities on the production database
    if args.mode == "create":
        entities_map = {}
        for staging_entity_id, data in staging_entities_data.items():
            entity = wbi_core.ItemEngine()

            label = data.get("labels", {}).get("en", {}).get("value")
            if label is not None:
                entity.set_label(label, ENGLISH)

            prod_entity_id = entity.write(login_instance)
            entities_map[staging_entity_id] = prod_entity_id

        print(entities_map)
        with open(args.path_to_entities_map, "w") as f:
            json.dump(entities_map, f)

    # TODO update the properties of the entities
