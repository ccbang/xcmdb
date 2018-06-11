from rest_framework import authentication
from rest_framework import exceptions
from cmdb.models.xroleModel import Users
import hmac
import hashlib
import base64
import re


class SignatureAuthentication(authentication.BaseAuthentication):

    SIGNATURE_RE = re.compile('signature="(.+?)"')
    # SIGNATURE_HEADERS_RE = re.compile(r'headers="([\(\)\sa-z0-9-]+?)"')
    # 使用分号来分割
    SIGNATURE_HEADERS_RE = re.compile(r'headers="([\(\);a-z0-9-]+?)"')

    API_KEY_HEADER = 'X-Api-Key'
    ALGORITHM = 'hmac-sha256'

    def get_signature_from_signature_string(self, signature):
        """Return the signature from the signature header or None."""
        match = self.SIGNATURE_RE.search(signature)
        if not match:
            return None
        return match.group(1)

    def get_headers_from_signature(self, signature):
        """Returns a list of headers fields to sign.

        According to http://tools.ietf.org/html/draft-cavage-http-signatures-03
        section 2.1.3, the headers are optional. If not specified, the single
        value of "Date" must be used.
        """
        match = self.SIGNATURE_HEADERS_RE.search(signature)
        if not match:
            return ['date']
        headers_string = match.group(1)
        return headers_string.split(';')

    def header_canonical(self, header_name):
        """Translate HTTP headers to Django header names."""
        # Translate as stated in the docs:
        # https://docs.djangoproject.com/en/1.6/ref/request-response/#django.http.HttpRequest.META
        header_name = header_name.lower()
        if header_name == 'content-type':
            return 'CONTENT-TYPE'
        elif header_name == 'content-length':
            return 'CONTENT-LENGTH'
        return 'HTTP_%s' % header_name.replace('-', '_').upper()

    def build_dict_to_sign(self, request, signature_headers):
        """Build a dict with headers and values used in the signature.

        "signature_headers" is a list of lowercase header names.
        """
        d = {}
        for header in signature_headers:
            if header == '(request-target)':
                continue
            d[header] = request.META.get(self.header_canonical(header))
        return d

    def build_signature(self, user_api_key, user_secret, request):
        """Return the signature for the request."""
        sent_signature = request.META.get(
            self.header_canonical('Authorization'))
        signature_headers = self.get_headers_from_signature(sent_signature)
        unsigned = self.build_dict_to_sign(request, signature_headers)

        # 使用自定义加密方法
        sign_dict = {
            "key": user_secret,
            "dateStamp": unsigned.get("date"),
            "appName": unsigned.get("app"),
            "serviceName": unsigned.get("service")
        }
        try:
            ret = self.getSignatureKey(**sign_dict)
        except Exception as e:
            print(self.__class__.__name__, e)
            ret = None
        return ret

    def sign(self, key, msg):
        return hmac.new(key, msg.encode(), hashlib.sha256).digest()

    def getSignatureKey(self, key, dateStamp, appName, serviceName):
        kDate = self.sign(('esc' + key).encode(), dateStamp)
        kAPP = self.sign(kDate, appName)
        kService = self.sign(kAPP, serviceName)
        kSigning = self.sign(kService, 'esc_request')
        return base64.b64encode(kSigning).decode()

    def fetch_user_data(self, api_key):
        """Retuns (User instance, API Secret) or None if api_key is bad."""
        try:
            user = Users.objects.get(api_key=api_key)
            return (user, user.api_securt)
        except Users.DoesNotExist:
            return None

    def authenticate(self, request):
        # Check for API key header.
        api_key_header = self.header_canonical(self.API_KEY_HEADER)
        api_key = request.META.get(api_key_header)
        if not api_key:
            return None

        # Check if request has a "Signature" request header.
        authorization_header = self.header_canonical('Authorization')
        sent_string = request.META.get(authorization_header)
        if not sent_string:
            raise exceptions.AuthenticationFailed('No signature provided')
        sent_signature = self.get_signature_from_signature_string(sent_string)

        # Fetch credentials for API key from the data store.
        try:
            user, secret = self.fetch_user_data(api_key)
        except TypeError:
            raise exceptions.AuthenticationFailed('Bad API key')

        # Build string to sign from "headers" part of Signature value.
        # computed_string = self.build_signature(api_key, secret, request)
        # computed_signature = self.get_signature_from_signature_string(
        #     computed_string)
        computed_signature = self.build_signature(api_key, secret, request)

        if computed_signature != sent_signature:
            raise exceptions.AuthenticationFailed('Bad signature')

        return (user, api_key)
