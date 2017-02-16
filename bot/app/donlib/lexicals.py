import re


class Lexicals(object):
    """This contains a number of text parsing methods to derive query logic
    from natural language"""
    @classmethod
    def parse(cls, message):
        """At some point, this should call two methods, one for getting
        the message type, the other for parsing targets from the message"""
        body = message["text"].replace('\'', '')
        query_type = Lexicals.get_message_type(body)
        target = Lexicals.get_target(body)
        return(query_type, target)

    @classmethod
    def get_message_type(cls, message):
        retval = ("unknown")
        matchers = [(r'\sserver\s+(?!group)(?!\")\S+', "server_report"),
                    (r'compliance\s+graph\s+server\s+', "server_compliance_graph"),  # NOQA
                    (r'\sserver\s+(?!group)\"[^\"]+\"', "server_report"),
                    (r'\s+ip\s+\S+', "ip_report"),
                    (r'\s+group\s+firewall\s+(?!\")\S+',
                     "group_firewall_report"),
                    (r'\s+group\s+firewall\s+\"[^\"]+\"',
                     "group_firewall_report"),
                    (r'list\s(all\s)*servers', "all_servers"),
                    (r'list\s(all\s)*server\s*groups', "all_groups"),
                    (r'servers\sin\sgroup\s+(?!\")\S+', "servers_in_group"),
                    (r'servers\sin\sgroup\s+\"[^\"]+\"', "servers_in_group"),
                    (r'(?!\sin)\s+group\s+(?!\")\S+', "group_report"),
                    (r'(?!\sin)\s+group\s+\"[^\"]+\"', "group_report"),
                    (r'(?P<target>tasks)', "tasks"),
                    (r'(?P<target>selfie)', "selfie"),
                    (r'(?P<target>help)', "help"),
                    (r'(?P<target>version)', "version"),
                    (r'(?P<target>config)', "config"),
                    (r'(?P<target>health)', "health")]
        for match, name in matchers:
            s = re.search(match, message)
            if s:
                retval = name
                break
        q_string = "QUERY>> " + message
        i_string = "TYPE>> " + retval
        print(q_string)
        print(i_string)
        return retval

    @classmethod
    def get_target(cls, message):
        """Gets the search target.

        Assumes that the target is at the end of the sentence.

        Args:
            message (str): String containing target

        Returns:
            str: target, or empty string if target cannot be found.

        """

        quoted = r'[^\"]+\"(?P<target>[^\"]+)\"'
        unquoted = r'^.*?(?P<target>[A-Za-z0-9_-]+)$'
        if '"' in message:
            matcher = re.match(quoted, message)
        else:
            matcher = re.match(unquoted, message)
        if matcher:
            retval = matcher.group('target')
        else:
            retval = ""
        t_string = "TARGET>> " + retval
        print(t_string)
        return retval
