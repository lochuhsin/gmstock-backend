class CustomScript:
    unique: str = None

    @classmethod
    def run_script(cls, data) -> tuple[bool, float | str]:
        try:
            ...
        except Exception as e:
            return False, str(e)
        return True, 1.0
