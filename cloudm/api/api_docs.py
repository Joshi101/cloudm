import inspect
import yaml
import marshmallow
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import Swagger

from cloudm.api import serializers
from cloudm.api.urls import (
    get_all_machines,
    add_machine,
    edit_machine,
    get_all_clusters,
    add_cluster,
    edit_cluster,
    delete_cluster,
    operate_machine,
    get_machine,
)

OPENAPI_SPEC = """
openapi: 3.0.2
info:
    description: |
        This is the admin server.
        For this sample, you can use the auth token `some-special-token` to test the authorization filters.
        # Introduction
        This API is documented in **OpenAPI format**.
    x-logo:
        url: 'https://redocly.github.io/redoc/petstore-logo.png'
        altText: logo
    termsOfService: 'http://swagger.io/terms/'
servers:
- url: http://ec2-13-233-164-183.ap-south-1.compute.amazonaws.com
  description: Test server

"""


def setup_schema_definition(spec):
    for name, obj in inspect.getmembers(serializers):
        if inspect.isclass(obj) and type(obj) == marshmallow.schema.SchemaMeta:
            try:
                spec.components.schema(name, schema=obj)
            except Exception as e:
                pass


def setup_path(spec):

    spec.path(view=get_all_machines)
    spec.path(view=get_machine)
    spec.path(view=add_machine)
    spec.path(view=edit_machine)
    spec.path(view=operate_machine)
    spec.path(view=get_all_clusters)
    spec.path(view=add_cluster)
    spec.path(view=edit_cluster)
    spec.path(view=delete_cluster)


def init_docs(app):
    ctx = app.test_request_context()
    ctx.push()
    settings = yaml.safe_load(OPENAPI_SPEC)

    # Create an APISpec
    spec = APISpec(
        title="Swagger Cloudm",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=(FlaskPlugin(), MarshmallowPlugin()),
        **settings
    )
    setup_schema_definition(spec)
    setup_path(spec)
    with open("cloudm/docs/swagger.yml", "w") as swagger_file:
        swagger_file.write(spec.to_yaml())
    app.config["SWAGGER"] = {"title": "Swagger Cloudm", "openapi": "3.0.2"}
    Swagger(app, template=spec.to_dict())
