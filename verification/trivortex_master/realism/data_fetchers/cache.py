#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — TTL-кэш на JSON + mtime.

get(key) / put(key, data, ttl) / invalidate(key). Формат — файл JSON,
свежесть по mtime + ttl. Используется TAP-запросами NASA.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import time
from typing import Any


class TTLCache:
    """Handle TTLCache."""
    def __init__(self, cache_dir: str, ttl: int = 86400):
        """Do TTLCache.  init for cache_dir, ttl and return the result."""
        self.dir = cache_dir
        self.ttl = ttl
        os.makedirs(cache_dir, exist_ok=True)

    def _path(self, key: str) -> str:
        """Do TTLCache. path for key and return the result."""
        safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in key)
        return os.path.join(self.dir, safe + ".json")

    def put(self, key: str, data: Any, ttl: int | None = None) -> None:
        """Do TTLCache.put for key, data, ttl and return the result."""
        payload = dict(
            saved=_dt.datetime.now().isoformat(timespec="seconds"),
            ttl=ttl if ttl is not None else self.ttl,
            data=data,
        )
        tmp = self._path(key) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False)
        os.replace(tmp, self._path(key))

    def get(self, key: str, max_age: int | None = None) -> Any | None:
        """None, если записи нет или она протухла."""
        path = self._path(key)
        if not os.path.isfile(path):
            return None
        try:
            age = time.time() - os.path.getmtime(path)
            limit = max_age if max_age is not None else self.ttl
            if age > limit:
                return None
            with open(path, encoding="utf-8") as fh:
                payload = json.load(fh)
            return payload.get("data")
        except (OSError, ValueError):
            return None

    def get_stale(self, key: str) -> Any | None:
        """Запись без проверки свежести (fallback при недоступной сети)."""
        path = self._path(key)
        if not os.path.isfile(path):
            return None
        try:
            with open(path, encoding="utf-8") as fh:
                payload = json.load(fh)
            return payload.get("data")
        except (OSError, ValueError):
            return None

    def invalidate(self, key: str) -> None:
        """Do TTLCache.invalidate for key and return the result."""
        try:
            os.remove(self._path(key))
        except OSError:
            pass

    def clear(self) -> None:
        """Handle TTLCache.clear."""
        for name in os.listdir(self.dir):
            if name.endswith(".json"):
                try:
                    os.remove(os.path.join(self.dir, name))
                except OSError:
                    pass

    def keys(self) -> list[str]:
        """Handle TTLCache.keys."""
        return sorted(f[:-5] for f in os.listdir(self.dir) if f.endswith(".json"))

    def status(self) -> list[dict[str, Any]]:
        """Handle TTLCache.status."""
        out = []
        for key in self.keys():
            path = self._path(key)
            try:
                age = time.time() - os.path.getmtime(path)
                out.append(
                    dict(
                        key=key,
                        age_seconds=int(age),
                        fresh=age <= self.ttl,
                        size=os.path.getsize(path),
                    )
                )
            except OSError:
                continue
        return out
