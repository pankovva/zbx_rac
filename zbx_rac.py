#!/bin/env python3
# -*- coding: utf-8 -*-
# version 0.8

import argparse
from collections import Counter
from lib_rac import Client1C, UserDecorators



def discovery(args):
    server = Client1C(args.hostname, args.cls_user, args.cls_pwd)
    db_list = server.get_db_list()
    return Client1C.get_zabbix_lld(db_list)


@UserDecorators.to_json
def session(args):
    result = {}
    server = Client1C(args.hostname, args.cls_user, args.cls_pwd)
    session = server.get_session_list(args.db_id)
    result["total sessions"] = len(session)
    if result["total sessions"] > 0:
        result["hibernate"] = Client1C.counter_session(session,
                                            "hibernate", "yes")
        _ = Counter([x["app-id"] for x in session])
        result.update(dict(_))
    return result


@UserDecorators.to_json
def process(args):
    server = Client1C(args.hostname, args.cls_user, args.cls_pwd)
    process = server.get_process_list()
    result = []
    for i, proc in enumerate(process):
        proc["id"] = i
        result.append(proc)
    return result


@UserDecorators.to_json
def licenses(args):
    server = Client1C(args.hostname, args.cls_user, args.cls_pwd)
    lic = server.get_license_list(args.db_id)
    result = Counter([x["short-presentation"] for x in lic])
    return result


parser = argparse.ArgumentParser(description="Скрипт для сбора"
                                 " данных сервера 1С")
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='description')
discovery_parser = subparsers.add_parser("discovery",
                                         help="поиск баз данных Zabbix LLD")
discovery_parser.add_argument("-s", dest="hostname",
                              required=True,
                              help="-s hostname | ip")
discovery_parser.add_argument("-cls-user",
                              dest="cls_user",
                              default=None,
                              help="Имя администратора кластера 1С")
discovery_parser.add_argument("-cls-pwd",
                              dest="cls_pwd",
                              default=None,
                              help="пароль администратора кластера 1С")
discovery_parser.set_defaults(func=discovery)

session_parser = subparsers.add_parser("session",
                                       help="Отчет по сесиям для БД")
session_parser.add_argument("-s", dest="hostname",
                            required=True,
                            help="-s hostname | ip")
session_parser.add_argument("-cls-user",
                            dest="cls_user",
                            default=None,
                            help="Имя администратора кластера 1С")
session_parser.add_argument("-cls-pwd",
                            dest="cls_pwd",
                            default=None,
                            help="пароль администратора кластера 1С")
session_parser.add_argument("-db-id",
                            dest="db_id",
                            required=True,
                            help="ID БД(INFOBASE)")
session_parser.set_defaults(func=session)


process_parser = subparsers.add_parser("process",
                                       help="Отчет по процессам кластера 1С")
process_parser.add_argument("-s", dest="hostname",
                            required=True,
                            help="-s hostname | ip")
process_parser.add_argument("-cls-user",
                            dest="cls_user",
                            default=None,
                            help="Имя администратора кластера 1С")
process_parser.add_argument("-cls-pwd",
                            dest="cls_pwd",
                            default=None,
                            help="пароль администратора кластера 1С")
process_parser.set_defaults(func=process)


session_parser = subparsers.add_parser("licenses",
                                       help="Отчет по сесиям для БД")
session_parser.add_argument("-s", dest="hostname",
                            required=True,
                            help="-s hostname | ip")
session_parser.add_argument("-cls-user",
                            dest="cls_user",
                            default=None,
                            help="Имя администратора кластера 1С")
session_parser.add_argument("-cls-pwd",
                            dest="cls_pwd",
                            default=None,
                            help="пароль администратора кластера 1С")
session_parser.add_argument("-db-id",
                            dest="db_id",
                            required=True,
                            help="ID БД(INFOBASE)")
session_parser.set_defaults(func=licenses)

if __name__ == '__main__':
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        print(args.func(args))
