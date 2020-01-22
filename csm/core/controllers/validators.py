#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          validators.py
 Description:       This File will serve as Command Validators for CSM

 Creation Date:     20/11/2019
 Author:            Prathamesh Rodi

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - : 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import re
from marshmallow.validate import Validator, ValidationError
from csm.core.blogic import const

class UserNameValidator(Validator):
    """
    Validator Class for Username Fields in CSM
    """
    def __call__(self, value):
        if not re.search(r"^[a-zA-Z0-9_-]{8,64}$", value):
            raise ValidationError("Username can only contain Alphanumeric, - and  _ .Length Must be between 8-64 Characters")

class CommentsValidator(Validator):
    """
    Validation Class for Comments and Strings in CSM
    """

    def __call__(self, value):
        if len(value) > const.STRING_MAX_VALUE:
            raise ValidationError(
                "Length should not be more than that of 250 characters.")

class PortValidator(Validator):
    """
    Validation Class for Ports Entered in CSM
    """

    def __call__(self, value):
        if not const.PORT_MIN_VALUE < int(value) or not const.PORT_MAX_VALUE > int(value):
            raise ValidationError(f"Port Value should be between {const.PORT_MIN_VALUE} than {const.PORT_MAX_VALUE}")

class PathPrefixValidator(Validator):
    """
    Path Prefix Validator for S3 Paths.
    """
    def __call__(self, value):
        if len(value) > const.PATH_PREFIX_MAX_VALUE:
            raise ValidationError(f"Path must not be more than {const.PATH_PREFIX_MAX_VALUE} characters.")
        if not value.startswith("/"):
            raise ValidationError("Path Must Start with '/'.")

class PasswordValidator(Validator):
    """
    Password Validator Class for CSM Passwords Fields.
    """
    def __call__(self, password):
        if len(password) < 8:
            raise ValidationError(
                "Password must be of more than 8 characters.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "Password must contain at least one Uppercase Alphabet.")
        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "Password must contain at least one Lowercase Alphabet.")
        if not re.search(r"[0-9]", password):
            raise ValidationError(
                "Password must contain at least one Numeric value.")
        if not re.search(r"[" + "\\".join(const.PASSWORD_SPECIAL_CHARACTER) + "]",
                         password):
            raise ValidationError((f"Password must include at lease one of the "
                f"{''.join(const.PASSWORD_SPECIAL_CHARACTER)} characters."))

class BucketNameValidator(Validator):
    """
        Validator Class for Bucket Name.
    """
    def __call__(self, value):
        if not re.search(r"^[a-z0-9][a-z0-9-]{1,34}[a-z0-9]$", value):
            raise ValidationError(
                ("Bucket Name should be between 3-36 Characters long." 
                 "Should contain either lowercase, numeric or '-' characters. "
                 "Not starting or ending with '-'"))

class Ipv4(Validator):
    """
    Validator class for ipv4 address validation.
    """
    @staticmethod
    def validate_ipv4(ip):
        ip_regex = ("^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.("
                    "25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.("
                    "25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.("
                    "25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$")
        return re.search(ip_regex, ip)

    def __call__(self, ip):
        if not self.validate_ipv4(ip):
            raise ValidationError(
                "Invalid IP4 address.")

class DomainName(Validator):
    """
    Validator class for domain name validation.
    """
    @staticmethod
    def validate_domain_name(domain_name):
        domain_regex = "^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,6}$"
        return re.search(domain_regex, domain_name)

    def __call__(self, domain_name):
        if len(domain_name) > 253:
            raise ValidationError(
                "Domain name should be less than 253 characters")
        if not self.validate_domain_name(domain_name):
            raise ValidationError(
                "Invalid domain name.")

class Server(Validator):
    """
    Validator class for both ipv4 address and domain name validation.
    """
    def __call__(self, server_name):
        if len(server_name) > 253:
            raise ValidationError(
                "Server name should be less than 253 characters")
        if not (Ipv4.validate_ipv4(server_name) or
                DomainName.validate_domain_name(server_name)):
            raise ValidationError(
                "Invalid server name.")
