__author__ = "Graeme Ford"
__copyright__ = "Copyright 2021, Graeme Ford"
__email__ = "graeme.ford@tuks.co.za"
__license__ = "GNU GPLv3"

import os
import json
import re
from glob import glob
from typing import List
from snakemake.rules import Wildcards

config = dict()

with open(os.path.join("config", "config.json"), "r") as f:
    config = json.load(f)

CHR = next(
    item["Value"] if item["Type"] == "NOTATION" else None
    for item in config["Operations"]
)
FILTER = next(
    item["Value"] if item["Type"] == "FILTER" else None for item in config["Operations"]
)


def getCpInput(wildcards: object = dict()) -> str:
    """A function that returns the absolute path of a file,
    given its input name and the provided paths

    Args:
        wildcards (object): The name of the file

    Returns:
        str: The relative file path
    """
    reX = r"^([A-Z]{0,1}:{1}[\\|\/]{1,2}){0,1}(.+[\\\/])*([^_\n]+)(\.vcf|\.vcf\.gz|\.vcf\.gz\.tbi)$"
    try:
        if next(item for item in config["Operations"] if item["Type"] == "FILTER"):
            input = "results/FILTERED/{}.vcf.gz".format(wildcards.filename)
    except Exception:
        try:
            if next(
                item for item in config["Operations"] if item["Type"] == "NOTATION"
            ):
                input = "results/NOTATION/{}.vcf.gz".format(wildcards.filename)
        except Exception:
            input = ""
            print(
                "Error: No VCF file Match Found for this input request. FILENAME: results/"
                + wildcards.filename
                + ".vcf.gz"
            )
    return input


def getFilterInput(wildcards: Wildcards):
    reX = r"^([A-Z]{0,1}:{1}[\\|\/]{1,2}){0,1}(.+[\\\/])*([^_\n]+)(\.vcf|\.vcf\.gz|\.vcf\.gz\.tbi)$"
    try:
        vcf = next(
            file
            for file in config["Files"]
            if re.search(reX, file).group(3) == wildcards.filename
            and re.search(reX, file).group(4) == ".vcf.gz"
        )
    except Exception:
        vcf = ""
        print(
            "Error: No VCF Match Found for this input request. FILENAME: results/"
            + wildcards.filename
            + ".vcf.gz"
        )

    try:
        tabix = next(
            file
            for file in config["Files"]
            if re.search(reX, file).group(3) == wildcards.filename
            and re.search(reX, file).group(4) == ".vcf.gz.tbi"
        )
    except Exception:
        tabix = ""
        print(
            "Error: No TABIX index Match Found for this input request. FILENAME: results/"
            + wildcards.filename
            + ".vcf.gz.tbi"
        )

    return {"vcf": vcf, "tabix": tabix}


def getNotationInput(wildcards: Wildcards):
    reX = r"^([A-Z]{0,1}:{1}[\\|\/]{1,2}){0,1}(.+[\\\/])*([^_\n]+)(\.vcf|\.vcf\.gz|\.vcf\.gz\.tbi)$"
    try:
        vcf = next(
            file
            for file in config["Files"]
            if re.search(reX, file).group(3) == wildcards.filename
            and re.search(reX, file).group(4) == ".vcf.gz"
        )
    except Exception:
        vcf = ""
        print(
            "Error: No VCF Match Found for this input request. FILENAME: results/"
            + wildcards.filename
            + ".vcf.gz"
        )
    try:
        tabix = next(
            file
            for file in config["Files"]
            if re.search(reX, file).group(3) == wildcards.filename
            and re.search(reX, file).group(4) == ".vcf.gz.tbi"
        )
    except Exception:
        tabix = ""
        print(
            "Error: No TABIX index Match Found for this input request. FILENAME: results/"
            + wildcards.filename
            + ".vcf.gz.tbi"
        )

    return {"vcf": vcf, "tabix": tabix}
