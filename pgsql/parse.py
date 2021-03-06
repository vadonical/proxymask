#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2020/5/12 14:35
# @File     : parse.py
# @IDE      : PyCharm


from tools import fmt
from tools import forge
from settings import system
from pgsql import replace


class PgSQLParser:

    def __init__(self):
        self.packet = bytes()
        self.data = self.packet.upper()
        self.index = int()
        self.code = int()

    def _exclude(self) -> bool:
        """

        :return:
        """
        pass_keys = [i.encode().upper() for i in system.PGSQL_PASS_KEYS]
        if any(i in self.data for i in pass_keys):
            return True

    def _determine(self):
        """

        :return:
        """
        select_index = self.data.find(b'SELECT')
        create_index = self.data.find(b'CREATE')
        if create_index != -1 and create_index < select_index:
            self.index = create_index
        self.index = select_index

    def dispatch(self, packet: bytes) -> bytes:
        """

        :param packet:
        :return:
        """
        self.packet = packet
        self._determine()
        if self._exclude():
            return self.packet
        if self.index == 5 and self.code == 0:
            _sql = fmt.default_sql(self.packet[self.index:].decode('utf-8'))
            sql = replace.replace(_sql)
            return self._construct(sql)
        return self.packet

    def _construct(self, sql:str) -> bytes:
        """

        :param sql:
        :return:
        """
        s_one = bytes([self.packet[0]])
        s_thr = bytes([self.packet[5]])
        s_pos = self.packet[-38:]

        l_two = forge.number2bytes(
            number=len(sql) + 8,
            length=4,
            reverse=False
        )
        r_sql = sql.encode()
        # error
        packet = s_one + l_two + s_thr + r_sql + s_pos
        return packet
