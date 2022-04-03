#!/usr/bin/env python3
# Token Authentication API Resource
from flask_restx import fields, Resource
from Api.api import api, conn

# tokens Namespace
tokens_ns = api.namespace(
    name="auth/tokens",
    description="Allows users to authenticate using a token.")
tokens_model = api.model(
    "Auth Method - Token", {
        "token": fields.String(
            required=True, pattern="[a-fA-F0-9]+", min_length=8,
            description="Token for API authentication"),
        "status": fields.String(
            required=False,
            description="Operation Status"),
    })

# tokens Arguments
tokens_parser = api.parser()
tokens_parser.add_argument(
    "token", type=str, required=True, location="form",
    help="API Token used to authenticate with the Secrets Manager")


@tokens_ns.route("/")
@api.doc(
    responses={},
    params={})
class Auth_Tokens(Resource):
    """Token operations"""

    @api.doc(
        description="Revoke a given API token",
        responses={200: "Token revoked"},
        parser=tokens_parser)
    @api.marshal_with(tokens_model)
    def delete(self):
        """Revoke a given API token"""
        # TODO: Add support for userpass
        args = tokens_parser.parse_args()
        return conn.tokens.revoke(token=args['token'])

    @api.doc(description="Generate a new API token.")
    @api.marshal_with(tokens_model)
    def get(self):
        """Generate a new API token"""
        # TODO: Add support for userpass
        return conn.tokens.generate()
