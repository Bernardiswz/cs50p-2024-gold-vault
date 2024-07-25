import os


__all__ = ["LinkProcessor"]


class LinkProcessor:
    def __init__(self) -> None:
        self.visited_paths: set = set()

    def get_link_path(self, link_path: str, max_depth: int = 10) -> str:
        if link_path in self.visited_paths:
            raise ValueError(f"Detected a cyclic link: {link_path}")
        
        self.visited_paths.add(link_path)
        
        if len(self.visited_paths) > max_depth:
            raise RecursionError(f"Maximum recursion depth reached for: {link_path}")

        if os.path.islink(link_path):
            target_path = os.readlink(link_path)
            return self._process_link(target_path, max_depth)
        else:
            return os.path.realpath(link_path)
