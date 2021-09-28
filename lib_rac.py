# -*- coding: utf-8 -*-
import logging, json, subprocess


logger = logging.getLogger('lib_1c_rac')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class UserDecorators():
    @classmethod
    def to_json(cls, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result = json.dumps(result)
            return result
        return wrapper


class Client1C:
    def __init__(self, hostname, cls_user=None, cls_pwd=None):
        self.hostname = hostname
        self.cls_user = cls_user
        self.cls_pwd = cls_pwd
        self.cluster_id = self.get_cluster_id()

    def get_cluster_id(self):
        command = 'rac cluster list {}'.format(self.hostname)
        result = self._exec_rac(command)
        return result[0]["cluster"]

    def get_db_list(self):
        command = 'rac infobase --cluster={} summary list {}'
        if self.cls_user and self.cls_pwd:
            command += " --cluster-user={} --cluster-pwd={}".format(
                       self.cls_user, self.cls_pwd)
        result = self._exec_rac(command.format(self.cluster_id, self.hostname))
        return result


    def get_session_list(self, db_id):
        command = 'rac session --cluster={} list --infobase={} {}'
        if self.cls_user and self.cls_pwd:
            command += " --cluster-user={} --cluster-pwd={}".format(
                       self.cls_user, self.cls_pwd)
        command = command.format(self.cluster_id, db_id, self.hostname)
        result = self._exec_rac(command)
        return result


    def get_license_list(self, db_id):
        command = 'rac session --cluster={} list --infobase={} {} --licenses'
        if self.cls_user and self.cls_pwd:
            command += " --cluster-user={} --cluster-pwd={}".format(
                       self.cls_user, self.cls_pwd)
        command = command.format(self.cluster_id, db_id, self.hostname)
        result = self._exec_rac(command)
        return result


    def get_db_info(self, db_id, user_name=None, user_pwd=None):
        command = 'rac infobase --cluster={} info --infobase={} {}'
        if self.cls_user and self.cls_pwd:
            command += " --cluster-user={} --cluster-pwd={}".format(
                       self.cls_user, self.cls_pwd)
        if user_name and user_pwd:
            command += " --infobase-user={} --infobase-pwd={}".format(
                       user_name, user_pwd)
        command = command.format(self.cluster_id, db_id, self.hostname)
        result = self._exec_rac(command)
        return result


    def get_process_list(self):
        command = 'rac process --cluster={} list {}'
        if self.cls_user and self.cls_pwd:
            command += " --cluster-user={} --cluster-pwd={}".format(
                       self.cls_user, self.cls_pwd)
        command = command.format(self.cluster_id, self.hostname)
        result = self._exec_rac(command)
        return result

    @staticmethod
    def _exec_rac(command:str) -> str:
        result = subprocess.run(command.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding="utf-8"
                                )
        if result.stderr:
            logger.error('Error subprocess.run, arg: {}, Error:{}'.format(
                         result.args, result.stderr))
        else:
            return Client1C._row_output_to_dict(result.stdout)

    @staticmethod
    def _row_output_to_dict(output:str) -> list:
        result = []
        for block in output.split("\n\n"):
            if block:
                dict_block = {}
                for line in block.split("\n"):
                    k, v = line.split(":", maxsplit=1)
                    k, v = k.strip(), v.strip("\"\' ")
                    dict_block[k] = v
                result.append(dict_block)
        return result

    @staticmethod
    @UserDecorators.to_json
    def get_zabbix_lld(output):
        result = []
        for item in output:
            new_item = {}
            for x, y in item.items():
                new_item["{{#{}}}".format(x.upper())] = y
            result.append(new_item)
        return result

    @staticmethod
    def top_session(session_list: list, d_key) -> dict:
        return max(session_list, key=lambda x: x[d_key])

    @staticmethod
    def counter_session(session_list: list, d_key, v_filter) -> int:
        return len([x for x in session_list if x[d_key] == v_filter])
