#!/usr/bin/env python3

import argparse
import json
import re
from datetime import datetime

import boto3 # type: ignore
try:
    from botocore.exceptions import ClientError # type: ignore
except ImportError:
    ClientError = Exception


# ---------------------------------------------------------------------
# Regex compiladas
# ---------------------------------------------------------------------

RE_CUSTOMER_PUBLIC = re.compile(
    r"<customer_gateway>.*?<tunnel_outside_address>.*?<ip_address>(.*?)</ip_address>",
    re.S,
)

RE_CUSTOMER_INSIDE = re.compile(
    r"<customer_gateway>.*?<tunnel_inside_address>.*?<ip_address>(.*?)</ip_address>",
    re.S,
)

RE_AWS_INSIDE = re.compile(
    r"<vpn_gateway>.*?<tunnel_inside_address>.*?<ip_address>(.*?)</ip_address>",
    re.S,
)

RE_IKE = re.compile(
    r"<ike>.*?"
    r"<authentication_protocol>(.*?)</authentication_protocol>.*?"
    r"<encryption_protocol>(.*?)</encryption_protocol>.*?"
    r"<lifetime>(.*?)</lifetime>.*?"
    r"<perfect_forward_secrecy>(.*?)</perfect_forward_secrecy>",
    re.S,
)

RE_IPSEC = re.compile(
    r"<ipsec>.*?"
    r"<authentication_protocol>(.*?)</authentication_protocol>.*?"
    r"<encryption_protocol>(.*?)</encryption_protocol>.*?"
    r"<lifetime>(.*?)</lifetime>.*?"
    r"<perfect_forward_secrecy>(.*?)</perfect_forward_secrecy>.*?"
    r"<tcp_mss_adjustment>(.*?)</tcp_mss_adjustment>.*?"
    r"<interval>(.*?)</interval>.*?"
    r"<retries>(.*?)</retries>",
    re.S,
)


# ---------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------

def fmt_date(date_string):
    if not date_string:
        return "-"

    try:
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M:%S UTC")
    except Exception:
        return date_string


def line():
    print("=" * 70)


def subline():
    print("-" * 70)


# ---------------------------------------------------------------------
# AWS
# ---------------------------------------------------------------------

def get_vpns(region, profile=None, vpn_id=None):
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()

    ec2 = session.client("ec2", region_name=region)

    kwargs = {}

    if vpn_id:
        kwargs["VpnConnectionIds"] = [vpn_id]

    response = ec2.describe_vpn_connections(**kwargs)

    return response["VpnConnections"]


# ---------------------------------------------------------------------
# Impressão
# ---------------------------------------------------------------------

def print_vpn(vpn):

    line()
    print("RESUMO DA VPN")
    line()

    print(f"VPN Connection ID : {vpn['VpnConnectionId']}")
    print(f"Tipo              : {vpn['Type']}")
    print(f"Estado            : {vpn['State']}")
    print(f"VGW               : {vpn.get('VpnGatewayId','-')}")
    print(f"Transit Gateway   : {vpn.get('TransitGatewayId','-')}")
    print(f"Customer Gateway  : {vpn['CustomerGatewayId']}")

    options = vpn["Options"]

    print(
        f"Roteamento        : {'Estático' if options['StaticRoutesOnly'] else 'BGP'}"
    )

    print(f"Rede Local        : {options.get('LocalIpv4NetworkCidr','-')}")
    print(f"Rede Remota       : {options.get('RemoteIpv4NetworkCidr','-')}")

    print()

    xml = vpn["CustomerGatewayConfiguration"]

    customer_public_ips = RE_CUSTOMER_PUBLIC.findall(xml)
    customer_inside_ips = RE_CUSTOMER_INSIDE.findall(xml)
    aws_inside_ips = RE_AWS_INSIDE.findall(xml)

    ike = RE_IKE.search(xml)
    ipsec = RE_IPSEC.search(xml)

    telemetry = vpn["VgwTelemetry"]

    for i in range(len(telemetry)):

        subline()
        print(f"TUNNEL {i+1}")
        subline()

        print(f"AWS Public IP         : {telemetry[i]['OutsideIpAddress']}")

        if i < len(customer_public_ips):
            print(f"Customer Public IP    : {customer_public_ips[i]}")

        if i < len(aws_inside_ips):
            print(f"Tunnel Inside AWS     : {aws_inside_ips[i]}")

        if i < len(customer_inside_ips):
            print(f"Tunnel Inside Customer: {customer_inside_ips[i]}")

        print(f"Status                : {telemetry[i]['Status']}")
        print(f"Rotas aprendidas      : {telemetry[i]['AcceptedRouteCount']}")
        print(
            f"Última alteração      : {fmt_date(telemetry[i]['LastStatusChange'])}"
        )

        print()

    if ike:
        line()
        print("CONFIGURAÇÃO IKE (FASE 1)")
        line()

        print(f"Criptografia : {ike.group(2).upper()}")
        print(f"Integridade  : {ike.group(1).upper()}")
        print(f"PFS / DH     : {ike.group(4).upper()}")
        print(f"Lifetime     : {ike.group(3)} segundos")

        print()

    if ipsec:
        line()
        print("CONFIGURAÇÃO IPSEC (FASE 2)")
        line()

        print(f"Criptografia : {ipsec.group(2).upper()}")
        print(f"Integridade  : {ipsec.group(1).upper()}")
        print(f"PFS          : {ipsec.group(4).upper()}")
        print(f"Lifetime     : {ipsec.group(3)} segundos")
        print(f"TCP MSS      : {ipsec.group(5)}")
        print(f"DPD          : {ipsec.group(6)}s / {ipsec.group(7)} tentativas")

        print()

    line()
    print("SAÚDE DA VPN")
    line()

    up = 0

    for idx, tunnel in enumerate(telemetry, start=1):

        icon = "🟢" if tunnel["Status"] == "UP" else "🔴"

        print(f"Tunnel {idx:<2} {icon} {tunnel['Status']}")

        if tunnel["Status"] == "UP":
            up += 1

    print()

    if up == len(telemetry):
        print("Resultado: VPN totalmente operacional.")
    elif up > 0:
        print(f"Resultado: VPN parcialmente operacional ({up} túnel(is) ativo(s)).")
    else:
        print("Resultado: Nenhum túnel IPsec estabelecido.")

    print()


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser()

    session = boto3.Session()

    parser.add_argument(
        "--region",
        default=session.region_name,
        help="Região AWS (usa a região configurada na AWS CLI por padrão)"
    )

    parser.add_argument(
        "--profile",
        help="AWS CLI Profile",
    )

    parser.add_argument(
        "--vpn",
        help="VPN Connection ID",
    )

    args = parser.parse_args()

    try:
        vpns = get_vpns(
            region=args.region,
            profile=args.profile,
            vpn_id=args.vpn,
        )

        if not vpns:
            print("Nenhuma VPN encontrada.")
            return

        for vpn in vpns:
            print_vpn(vpn)

    except ClientError as e:
        print(f"Erro AWS: {e}")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
