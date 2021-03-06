# Copyright (C) 2017 O.S. Systems Software LTDA.
# This software is released under the MIT License

from .base import HydraManager


class Client:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.owner = kwargs.get('owner')
        self.name = kwargs.get('name') or kwargs.get('client_name')
        self.secret = kwargs.get('secret') or kwargs.get('client_secret')
        self.uri = kwargs.get('uri') or kwargs.get('client_uri')
        self.policy_uri = kwargs.get('policy_uri')
        self.tos_uri = kwargs.get('tos_uri')
        self.logo_uri = kwargs.get('logo_uri')
        self.contacts = kwargs.get('contacts')
        self.redirect_uris = kwargs.get('redirect_uris')
        self.grant_types = kwargs.get('grant_types')
        self.response_types = kwargs.get('response_types')
        self.is_public = kwargs.get('public')
        self.scopes = kwargs.get('scope', '').split() or kwargs.get('scopes', [])  # nopep8

    def as_dict(self):
        data = {
            'id': self.id,
            'owner': self.owner,
            'client_name': self.name,
            'client_secret': self.secret,
            'client_uri': self.uri,
            'policy_uri': self.policy_uri,
            'tos_uri': self.tos_uri,
            'logo_uri': self.logo_uri,
            'contacts': self.contacts,
            'scope': ' '.join(self.scopes),
            'redirect_uris': self.redirect_uris,
            'grant_types': self.grant_types,
            'response_types': self.response_types,
            'public': self.is_public,
        }
        return {k: v for k, v in data.items() if v is not None}


class ClientManager(HydraManager):

    SCOPE = 'hydra.clients'

    def create(self, client):
        response = self.hydra.request(
            'POST', '/clients', scope=self.SCOPE, json=client.as_dict())
        if response.ok:
            return Client(**response.json())

    def get(self, client_id):
        path = '/clients/{}'.format(client_id)
        response = self.hydra.request('GET', path, scope=self.SCOPE)
        if response.ok:
            return Client(**response.json())

    def update(self, client):
        path = '/clients/{}'.format(client.id)
        response = self.hydra.request(
            'PUT', path, scope=self.SCOPE, json=client.as_dict())
        if response.ok:
            return Client(**response.json())

    def delete(self, client_id):
        path = '/clients/{}'.format(client_id)
        self.hydra.request('DELETE', path, scope=self.SCOPE)

    def all(self):
        response = self.hydra.request('GET', '/clients', scope=self.SCOPE)
        if response.ok:
            return [Client(**data) for data in response.json().values()]
