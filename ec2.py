#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path


# =====================================================================
# CONFIGURAÇÃO
# =====================================================================

REGION = "sa-east-1"
OUTPUT_FILE = "ec2_report.txt"

# Caso queira filtrar por perfil AWS
AWS_PROFILE = None
# AWS_PROFILE = "default"


# =====================================================================
# AUXILIARES
# =====================================================================

def aws_describe_instances():

    cmd = ["aws"]

    if AWS_PROFILE:
        cmd.extend(["--profile", AWS_PROFILE])

    cmd.extend([
        "ec2",
        "describe-instances",
        "--region",
        REGION,
        "--output",
        "json"
    ])

    try:

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        return json.loads(result.stdout)

    except subprocess.CalledProcessError as e:

        print("\nErro ao executar AWS CLI\n")
        print(e.stderr)
        sys.exit(1)

    except json.JSONDecodeError:

        print("AWS CLI retornou um JSON inválido.")
        sys.exit(1)


def get_tags(instance):
    return {
        tag["Key"]: tag["Value"]
        for tag in instance.get("Tags", [])
    }


def line(title, value):
    return f"{title:<22}: {value}"


# =====================================================================
# FORMATAÇÃO
# =====================================================================

def format_instance(instance):

    tags = get_tags(instance)

    txt = []

    txt.append("=" * 90)
    txt.append(f"INSTÂNCIA: {tags.get('Name', '(Sem Nome)')}")
    txt.append("=" * 90)

    txt.append(line("Instance ID", instance.get("InstanceId")))
    txt.append(line("Estado", instance["State"]["Name"]))
    txt.append(line("Tipo", instance.get("InstanceType")))
    txt.append(line("AMI", instance.get("ImageId")))
    txt.append(line("Arquitetura", instance.get("Architecture")))
    txt.append(line("Launch Time", instance.get("LaunchTime")))
    txt.append(line("Availability Zone",
                    instance["Placement"]["AvailabilityZone"]))
    txt.append(line("VPC", instance.get("VpcId")))
    txt.append(line("Subnet", instance.get("SubnetId")))
    txt.append(line("Private IP",
                    instance.get("PrivateIpAddress", "-")))
    txt.append(line("Public IP",
                    instance.get("PublicIpAddress", "-")))
    txt.append(line("Private DNS",
                    instance.get("PrivateDnsName", "-")))
    txt.append(line("Public DNS",
                    instance.get("PublicDnsName", "-")))
    txt.append(line("Key Pair",
                    instance.get("KeyName", "-")))
    txt.append(line("Plataforma",
                    instance.get("PlatformDetails")))
    txt.append(line("Virtualização",
                    instance.get("VirtualizationType")))
    txt.append(line("Root Device",
                    instance.get("RootDeviceName")))
    txt.append(line("Source/Dest Check",
                    instance.get("SourceDestCheck")))
    txt.append(line("Monitoring",
                    instance["Monitoring"]["State"]))

    txt.append("")
    txt.append("NETWORK INTERFACES")
    txt.append("-" * 90)

    for eni in instance.get("NetworkInterfaces", []):

        assoc = eni.get("Association", {})

        txt.append(f"Descrição : {eni.get('Description', '-')}")
        txt.append(f"ENI        : {eni.get('NetworkInterfaceId')}")
        txt.append(f"MAC        : {eni.get('MacAddress')}")
        txt.append(f"Subnet     : {eni.get('SubnetId')}")
        txt.append(f"VPC        : {eni.get('VpcId')}")
        txt.append(f"Private IP : {eni.get('PrivateIpAddress')}")
        txt.append(f"Public IP  : {assoc.get('PublicIp', '-')}")
        txt.append("")

    txt.append("SECURITY GROUPS")
    txt.append("-" * 90)

    for sg in instance.get("SecurityGroups", []):

        txt.append(
            f"{sg['GroupName']} ({sg['GroupId']})"
        )

    txt.append("")
    txt.append("EBS VOLUMES")
    txt.append("-" * 90)

    for dev in instance.get("BlockDeviceMappings", []):

        ebs = dev.get("Ebs", {})

        txt.append(f"Device : {dev.get('DeviceName')}")
        txt.append(f"Volume : {ebs.get('VolumeId')}")
        txt.append(f"Status : {ebs.get('Status')}")
        txt.append("")

    txt.append("TAGS")
    txt.append("-" * 90)

    for key, value in sorted(tags.items()):

        txt.append(f"{key:<35} {value}")

    txt.append("")
    txt.append("")

    return "\n".join(txt)


# =====================================================================
# RELATÓRIO
# =====================================================================

def build_report(data):

    report = []

    report.append("=" * 90)
    report.append("RELATÓRIO DE INSTÂNCIAS EC2")
    report.append("=" * 90)
    report.append("")

    total = 0

    for reservation in data["Reservations"]:

        for instance in reservation["Instances"]:

            total += 1
            report.append(format_instance(instance))

    report.insert(3, f"Total de instâncias: {total}")
    report.insert(4, "")

    return "\n".join(report)


# =====================================================================
# MAIN
# =====================================================================

def main():

    print("Consultando AWS...")

    data = aws_describe_instances()

    print("Gerando relatório...")

    report = build_report(data)

    Path(OUTPUT_FILE).write_text(
        report,
        encoding="utf-8"
    )

    print(f"\nRelatório salvo em {OUTPUT_FILE}")


if __name__ == "__main__":
    main()