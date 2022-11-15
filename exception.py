# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""


class ReRateEx(Exception):
    def __init__(self, msg='You cannot re-rate.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_RE_RATE'

    pass


class InvalidNonce(Exception):
    def __init__(self, msg='Invalid nonce.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 406
        self.msg = msg
        self.errors = kwargs.get('errors', [{
            'nonce': 'Invalid'
        }])
        self.error_code = 'E_NONCE'

    pass


class InvalidSignature(Exception):
    def __init__(self, msg='Invalid signature.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 401
        self.msg = msg
        self.errors = kwargs.get('errors', [{
            'signature': 'Invalid'
        }])
        self.error_code = 'E_SIGNATURE'

    pass


class ELockAddress(Exception):
    def __init__(self, msg='Your address has a tx being processed. Please try again in 1 minute.', *args: object,
                 **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = []
        self.error_code = 'E_LOCK_ADDRESS'

    pass
