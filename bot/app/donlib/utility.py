import datetime


class Utility(object):
    """This is a collection of widely-used functions"""

    @classmethod
    def date_to_iso8601(cls, date_obj):
        """Returns an ISO8601-formatted string for datetime arg"""
        retval = date_obj.isoformat()
        return retval

    @classmethod
    def iso8601_arbitrary_days_ago(cls, days_ago):
        return Utility.date_to_iso8601(datetime.date.today() -
                                       datetime.timedelta(days=days_ago))

    @classmethod
    def iso8601_now(cls):
        return Utility.date_to_iso8601(datetime.datetime.utcnow())

    @classmethod
    def iso8601_today(cls):
        return Utility.date_to_iso8601(datetime.date.today())

    @classmethod
    def iso8601_yesterday(cls):
        return Utility.iso8601_arbitrary_days_ago(1)

    @classmethod
    def iso8601_one_week_ago(cls):
        return Utility.iso8601_arbitrary_days_ago(7)

    @classmethod
    def iso8601_one_month_ago(cls):
        """In this case, we assume 30 days"""
        return Utility.iso8601_arbitrary_days_ago(30)

    @classmethod
    def event_is_critical(cls, event):
        return event["critical"]

    @classmethod
    def u_to_8601(cls, unixtime):
        try:
            ret = datetime.datetime.fromtimestamp(float(unixtime)).isoformat()
        except TypeError:
            ret = "N/A"
        return ret
