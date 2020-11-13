import logging

from flask import Blueprint, jsonify, request, current_app
from requests import HTTPError

from app.utils import validate_organization, any_application_required

from app.workflows.services import (
    create_workflow,
    delete_workflow,
    fetch_workflow,
    fetch_workflows,
    update_workflow,
)

logger = logging.getLogger("organization-workflows")

organization_workflow_bp = Blueprint("workflows", __name__)


@organization_workflow_bp.route("/<organization_uuid>/workflows", methods=["POST"])
@any_application_required
@validate_organization()
def create(organization_uuid):
    """Create a Organization Workflow.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    requestBody:
      description: "Workflow name and description."
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              description:
                type: string
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                name:
                  type: string
                description:
                  type: string
                docker_image_url:
                  type: string
                repository_ssh_url:
                  type: string
                repository_branch:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """
    try:
        return jsonify(create_workflow(organization_uuid, request.json))
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route("/<organization_uuid>/workflows", methods=["GET"])
@any_application_required
@validate_organization()
def workflows(organization_uuid):
    """Get Organization Workflows.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  uuid:
                    type: string
                  name:
                    type: string
                  description:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """
    try:
        return jsonify(fetch_workflows(organization_uuid))
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>", methods=["GET"]
)
@any_application_required
@validate_organization(False)
def workflow(organization_uuid, organization_workflow_uuid):
    """Get Organization Workflow.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                name:
                  type: string
                description:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """
    try:
        return jsonify(fetch_workflow(organization_uuid, organization_workflow_uuid))
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>", methods=["PUT"]
)
@any_application_required
@validate_organization()
def workflow_update(organization_uuid, organization_workflow_uuid):
    """Updates Organization Workflow.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                name:
                  type: string
                description:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """
    try:
        return jsonify(
            update_workflow(organization_uuid, organization_workflow_uuid, request.json)
        )
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>", methods=["DELETE"]
)
@any_application_required
@validate_organization(False)
def workflow_delete(organization_uuid, organization_workflow_uuid):
    """Delete a Organization Workflow.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """

    try:
        delete_workflow(organization_uuid, organization_workflow_uuid)
        return {}, 200
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400