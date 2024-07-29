from .error_messages import CYCLIC_LINK_ERROR, DECRYPTION_ERROR, LINK_RECURSION_DEPTH_ERROR


__all__ = ["CyclicLinkError", "DecryptionError", "LinkRecursionDepthError"]


class CyclicLinkError(Exception):
    def __init__(self, link_path: str) -> None:
        self.link_path: str = link_path
        self.message: str = CYCLIC_LINK_ERROR.format(self.link_path)
        super().__init__(self.message)


class DecryptionError(Exception):
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.message: str = DECRYPTION_ERROR.format(self.path)
        super().__init__(self.message)


class LinkRecursionDepthError(Exception):
    def __init__(self, link_path: str) -> None:
        self.path: str = link_path
        self.message: str = LINK_RECURSION_DEPTH_ERROR.format(self.path)
        super().__init__(self.message)
