class UsuarioException(Exception):
    ...

class UsuarioNotFoundError(UsuarioException):
    def __init__(self):
        self.status_code = 404
        self.detail = "USUARIO_NAO_ENCONTRADO"


class UsuarioAlreadyExistError(UsuarioException):
    def __init__(self):
        self.status_code = 409
        self.detail = "USUARIO_DUPLICADO"

class MigracaoException(Exception):
    ...

class MigracaoNotFoundError(MigracaoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "MIGRACAO_NAO_ENCONTRADA"
        
class NotificacaoException(Exception):
    ...

class NotificacaoNotFoundError(NotificacaoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "NOTIFICACAO_NAO_ENCONTRADA"
