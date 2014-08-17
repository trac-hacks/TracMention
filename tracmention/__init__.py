import re

from trac.core import Component, implements
from trac.ticket.api import ITicketChangeListener
from trac.ticket.notification import TicketNotifyEmail
from trac.perm import IPermissionRequestor, PermissionSystem


class Notifications(Component):
    """Send notification to the mentioned persons"""
    implements(ITicketChangeListener, IPermissionRequestor)

    ping_regex = r'\B@(\w+)\b'

    def _find_mentions(self, ticket, text, user, newticket=False):
        if not PermissionSystem(self.env).check_permission('MENTION_NOTIFY', user):
            return False

        recipients = re.findall(self.ping_regex, text)

        if recipients:
            pn = PingNotifyEmail(self.env, recipients=recipients)
            pn.notify(ticket, newticket, modtime=ticket.values['changetime'])

    # IPermissionRequestor method
    def get_permission_actions(self):
        return ['MENTION_NOTIFY']

    # ITicketChangeListener methods
    def ticket_created(self, ticket):
        self._find_mentions(ticket, ticket.values['description'], ticket.values['reporter'], True)

    def ticket_changed(self, ticket, comment, author, old_values):
        if comment:
            self._find_mentions(ticket, comment, author)

        if 'description' in old_values:
            self._find_mentions(ticket, ticket.values['description'], author)

    def ticket_deleted(self, ticket):
        pass

    def ticket_comment_modified(self, ticket, cdate, author, comment, old_comment):
        self._find_mentions(ticket, comment, author)
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
