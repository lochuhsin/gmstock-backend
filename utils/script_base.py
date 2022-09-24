class CustomScript:
    unique: str | list = None

    """
     dataformat
     {
      "_id":"ObjectId(""632dd03e1133651df91dbecc"")",
      "datetime":datetime.datetime(2022,9,20,0,0),
      "open":168.89999,
      "high":170.3,
      "low":166.10001,
      "close":166.3,
      "volume":1181806
    }
    """

    @classmethod
    def run_script(cls, data: dict) -> tuple[bool, any]:
        try:
            ...
        except Exception as e:
            return False, str(e)
        return True, 1.0
