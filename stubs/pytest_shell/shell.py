from pytest_shell.dialect import BashDialect, Dialect


class ShellSession(Dialect):
    def __call__(self, envvars=None, source=None, pwd=None):
        ...

    def run_script(self, path, args=None, timeout=10.0, soft_timeout=True):
        ...


class LocalBashSession(ShellSession, BashDialect):
    pass
