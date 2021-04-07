# Requirements to be able to deploy / test deployments
install [gcloud sdk](https://cloud.google.com/sdk/docs/quickstart#installing_the_latest_version)

# CI/CD
For now, we want to deploy on staging when a PR is merged on staging and on prod when a PR is merged on master.

To do so, we need 2 cloudbuild triggers, one for staging, one for prod.
[See the triggers here](https://console.cloud.google.com/cloud-build/triggers?project=top-glass-307718). if the triggers to deploy this project don't seem to exist, create them following these instructions:

* Click the `+ CREATE TRIGGER` button
* name: project-name-environment (where project name looks like the repo name and environment is either staging, prod or dev)
* description: short description of the trigger
* Event:
    * push to a branch
* Source: 
    * Find the repository in the drop down. If it's not there add the repository by following the instructions
    * Branch: a regex describing which branch is being observed: `^` means the start of a string and `$` the end of a string so either `^staging$` or `^master$` (or `^main$` for today standards), or `^your-feature-branch-name$` if you want to test your code.
* Configuration:
    * Type: Cloud Build configuration file
    * Location: repository
    * Cloud build configuration location: cloudbuild.json
    
* Advanced:
    * [Substitution Variables](https://cloud.google.com/cloud-build/docs/configuring-builds/substitute-variable-values): **this is important**🚨 This is where you'll define the ${_YOURVARNAME} vars that you need to use in the cloudbuild.json file.
    

Then click on the `CREATE` button.
    

# To deploy manually and test your changes

```bash
$ gcloud functions deploy initialize-sources-dev --entry-point=initialize_sources --service-account= publisher-scheduler@top-glass-307718.iam.gserviceaccount.com --set-env-vars=GOOGLE_CLOUD_PROJECT=top-glass-307718,ENV=dev --runtime=python39 --timeout=540 --trigger-topic=before-initializer-dev
```

Then publish a message in the before-initializer-dev queue. [You can do so through the ui](https://console.cloud.google.com/cloudpubsub/topic/detail/before-dispatcher-dev?project=top-glass-307718) (if the link doesn't work it's because the topic doesn't exist yet. If you're in that case that means that either the dispatcher's dev CF was never deployed or that someone deleted the topic manually).
You should see an execution of the CF and if you look into `before-archives-dev` and `before-database-dev`

# Local dev:

create a virtual environment with python 3.9, install the requirements, run the tests. They should run. If not either some requirement is missing either the python version of the environment is not right.
