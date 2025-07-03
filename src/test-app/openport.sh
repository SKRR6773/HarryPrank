#!/bin/bash


RULE_NAME="Allow_HTTP_Inbound"


netsh advfirewall firewall add rule name="$RULE_NAME" dir=in action=allow protocol=TCP localport=6777


echo "ADD rule '$RULE_NAME'"
