import re

from trac.core import *
from trac.ticket.api import ITicketChangeListener
from trac.ticket.notification import TicketNotifyEmail


class Notifications(Component):
    """Send notification to the mentioned persons"""
    implements(ITicketChangeListener)

    ping_regex = r'\B@(\w+)\b'

    def _find_mentions(self, ticket, text, newticket=False):
        recipients = re.findall(self.ping_regex, text)

        if recipients:
            pn = PingNotifyEmail(self.env, recipients=recipients)
            pn.notify(ticket, newticket, modtime=ticket.values['changetime'])

    def ticket_created(self, ticket):
        self._find_mentions(ticket, ticket.values['description'], True)

    def ticket_changed(self, ticket, comment, author, old_values):
        if comment:
            self._find_mentions(ticket, comment)

        if 'description' in old_values:
            self._find_mentions(ticket, ticket.values['description'])

    def ticket_deleted(self, ticket):
        pass

    def ticket_comment_modified(self, ticket, cdate, author, comment, old_comment):
        self._find_mentions(ticket, comment)
        pass

    def ticket_change_deleted(self, ticket, cdate, changes):
        pass


class PingNotifyEmail(TicketNotifyEmail):
    _recipients = None

    def __init__(self, env, recipients):
        self._recipients = recipients
        TicketNotifyEmail.__init__(self, env)

    def get_recipients(self, resid):
        return (self._recipients, [])
