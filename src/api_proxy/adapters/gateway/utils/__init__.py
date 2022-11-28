from typing import Callable, Dict

import tenacity as tnc


def retry(retry_strategy: Dict, method: Callable, url: str, **kwargs):
    for att in tnc.Retrying(**retry_strategy):
        with att:
            res = method(url=url, **kwargs)
            if res.status_code >= 500:
                res.raise_for_status()
            return res
