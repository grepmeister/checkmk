#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import ast
import logging
import time
from collections.abc import Mapping, MutableMapping
from typing import Final

from cmk.utils.type_defs import HostName, SectionName

from cmk.snmplib.type_defs import SNMPRawData, SNMPRawDataSection

from cmk.fetchers.cache import SectionStore

from ._base import Parser
from .cache import FileCache
from .host_sections import HostSections
from .type_defs import SectionNameCollection

__all__ = ["SNMPFileCache", "SNMPParser"]


class SNMPFileCache(FileCache[SNMPRawData]):
    @staticmethod
    def _from_cache_file(raw_data: bytes) -> SNMPRawData:
        return {SectionName(k): v for k, v in ast.literal_eval(raw_data.decode("utf-8")).items()}

    @staticmethod
    def _to_cache_file(raw_data: SNMPRawData) -> bytes:
        return (repr({str(k): v for k, v in raw_data.items()}) + "\n").encode("utf-8")


class SNMPParser(Parser[SNMPRawData, SNMPRawDataSection]):
    """A parser for SNMP data.

    Note:
        It is forbidden to add base dependencies to this class.

    """

    def __init__(
        self,
        hostname: HostName,
        section_store: SectionStore[SNMPRawDataSection],
        *,
        check_intervals: Mapping[SectionName, int | None],
        keep_outdated: bool,
        logger: logging.Logger,
    ) -> None:
        super().__init__()
        self.hostname: Final = hostname
        self.check_intervals: Final = check_intervals
        self.section_store: Final = section_store
        self.keep_outdated: Final = keep_outdated
        self._logger = logger

    def parse(
        self,
        raw_data: SNMPRawData,
        *,
        # The selection argument is ignored: Selection is done
        # in the fetcher for SNMP.
        selection: SectionNameCollection,
    ) -> HostSections[SNMPRawDataSection]:
        sections = dict(raw_data)
        now = int(time.time())

        def lookup_persist(section_name: SectionName) -> tuple[int, int] | None:
            if (interval := self.check_intervals.get(section_name)) is not None:
                return now, now + interval
            return None

        cache_info: MutableMapping[SectionName, tuple[int, int]] = {}
        new_sections = self.section_store.update(
            sections,
            cache_info,
            lookup_persist,
            now=now,
            keep_outdated=self.keep_outdated,
        )
        return HostSections[SNMPRawDataSection](new_sections, cache_info=cache_info)
