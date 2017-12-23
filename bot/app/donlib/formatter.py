from string import Template as T


class Formatter(object):
    """All the message formatting happens in this class."""
    lib = {"issue": T("  ----------------------------------------\n" +
                      "  Issue $rule_key\n" +
                      "    Status $status\n" +
                      "    Type     $issue_type\n" +
                      "    Created  $created_at\n"),
           "event": T("  ----------------------------------------\n" +
                      "  Event $type\n" +
                      "    Critical $critical\n" +
                      "    Created  $created_at\n" +
                      "    Message  $message\n"),
           "server_facts": T("---------------------------\n" +
                             "Server Hostname     $hostname\n" +
                             "  Server ID         $id\n" +
                             "  Platform          $platform\n" +
                             "  Platform version  $platform_version\n" +
                             "  OS version        $os_version\n" +
                             "  Group             $group_name\n" +
                             "  Primary IP        $primary_ip_address\n" +
                             "  Connecting IP     $connecting_ip_address\n" +
                             "  State             $state\n" +
                             "  State Change      $last_state_change\n"),
           "server_ec2": T("---------------------------\n" +
                           "Server Hostname     $hostname\n" +
                           "  Server ID         $id\n" +
                           "  Platform          $platform\n" +
                           "  Platform version  $platform_version\n" +
                           "  OS version        $os_version\n" +
                           "  Group             $group_name\n" +
                           "  Primary IP        $primary_ip_address\n" +
                           "  Connecting IP     $connecting_ip_address\n" +
                           "  State             $state\n" +
                           "  State Change      $last_state_change\n" +
                           "  EC2:\n" +
                           "    Instance ID:    $ec2_instance_id\n" +
                           "    Account ID:     $ec2_account_id\n" +
                           "    Kernel ID:      $ec2_kernel_id\n" +
                           "    Image ID:       $ec2_image_id\n" +
                           "    Avail. Zone:    $ec2_availability_zone\n" +
                           "    Region:         $ec2_region\n" +
                           "    Private IP:     $ec2_private_ip\n" +
                           "    Instance Type:  $ec2_instance_type\n" +
                           "    Security Grps:  $ec2_security_groups\n"),
           "policy_meta": T("    ---------------------------------------\n" +
                            "    Policy name $name\n" +
                            "      Policy type   $poltype \n" +
                            "      Policy ID     $id\n" +
                            "      Description   $description\n"),
           "group_facts": T("---------------------------\n" +
                            "Group name $name\n" +
                            "  Group ID      $id\n" +
                            "  Description   $description\n" +
                            "  Tag           $tag\n"),
           "task": T("---------------------------\n" +
                     "Task ID: $id\n" +
                     "  Task Name:      $name\n" +
                     "  Task Args:      $args\n" +
                     "  Task Kwargs:    $kwargs\n" +
                     "  Task Started:   $started\n" +
                     "  Task Timestamp: $tstamp\n" +
                     "  Task State:     $state\n" +
                     "  Exception:      $exception\n")}

    @classmethod
    def format_list(cls, items, item_type):
        retval = ""
        for item in items:
            retval = retval + Formatter.format_item(item, item_type)
        return retval

    @classmethod
    def format_item(cls, item, item_type):
        t = Formatter.lib[item_type]
        retval = t.safe_substitute(item)
        return retval

    @classmethod
    def policy_meta(cls, body, poltype):
        """Return one policy in friendly text"""
        body["poltype"] = poltype
        t = Formatter.lib["policy_meta"]
        return t.safe_substitute(body)
