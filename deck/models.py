from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models import Count
from django.db.models.aggregates import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.utils import timezone

from django_extensions.db.fields import AutoSlugField

from allauth.account.signals import user_signed_up

from textwrap import dedent

from jury.models import Jury


class DeckBaseManager(models.QuerySet):
    def cached_authors(self):
        return super(DeckBaseManager, self).select_related('author')

    def published_ones(self):
        return self.cached_authors().filter(is_published=True)

    def order_by_never_voted(self, user_id):
        if self.model != Proposal:
            raise AttributeError(
                "%s object has no attribute %s" % (
                    self.model, 'order_by_never_voted'))

        order_by_criteria = dedent("""
            SELECT 1
              FROM deck_vote
             WHERE deck_vote.user_id = %s AND
                   deck_vote.proposal_id = deck_proposal.activity_ptr_id
             LIMIT 1
        """)

        new_ordering = ['-never_voted']
        if settings.DATABASES['default'].get('ENGINE') == 'django.db.backends.sqlite3':
            new_ordering = ['never_voted']
        new_ordering.extend(Proposal._meta.ordering)
        return self.extra(
            select=dict(never_voted=order_by_criteria % user_id),
            order_by=new_ordering
        )


class DeckBaseModel(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    slug = AutoSlugField(populate_from='title', overwrite=True,
                         max_length=200, unique=True, db_index=True)
    description = models.TextField(
        _('Description'), max_length=10000, blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    is_published = models.BooleanField(_('Publish'), default=True)

    # relations
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               related_name='%(class)ss')

    # managers
    objects = DeckBaseManager.as_manager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.title)


class Vote(models.Model):
    ANGRY, SLEEPY, SAD, HAPPY, LAUGHING = range(-1, 4)
    VOTE_TITLES = dict(
        angry=_('Angry'), sad=_('Sad'),
        sleepy=_('Sleepy'), happy=_('Happy'),
        laughing=_('Laughing')
    )
    VOTE_RATES = ((ANGRY, 'angry'),
                  (SAD, 'sad'),
                  (SLEEPY, 'sleepy'),
                  (HAPPY, 'happy'),
                  (LAUGHING, 'laughing'))
    rate = models.SmallIntegerField(_('Rate Index'), null=True, blank=True,
                                    choices=VOTE_RATES)

    # relations
    proposal = models.ForeignKey(to='deck.Proposal', related_name='votes')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='votes')

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        unique_together = (('proposal', 'user'),)

    def __unicode__(self):
        return u"{0.user}: {0.rate} in {0.proposal}".format(self)

    def save(self, *args, **kwargs):
        validation_message = None

        user_is_in_jury = self.proposal.event.jury.users.filter(
            pk=self.user.pk).exists()
        if (self.user.is_superuser or user_is_in_jury):
            pass
        elif self.user == self.proposal.author:
            validation_message = _(u'You cannot Rate your own proposals.')
        elif not self.proposal.event.allow_public_voting:
            validation_message = _(u"Proposal doesn't accept Public Voting.")
        elif self.proposal.user_already_voted(self.user):
            validation_message = _(u'Proposal already Rated by you.')

        if validation_message:
            raise ValidationError(_(validation_message))

        return super(Vote, self).save(*args, **kwargs)


class Activity(DeckBaseModel):
    PROPOSAL = 'proposal'
    WORKSHOP = 'workshop'
    OPENNING = 'openning'
    COFFEEBREAK = 'coffee-break'
    LUNCH = 'lunch'
    LIGHTNINGTALKS = 'lightning-talks'
    ENDING = 'ending'
    ACTIVITY_TYPES = (
        (PROPOSAL, _('Proposal')),
        (WORKSHOP, _('Workshop')),
        (OPENNING, _('Openning')),
        (COFFEEBREAK, _('Coffee Break')),
        (LUNCH, _('Lunch')),
        (LIGHTNINGTALKS, _('Lightning Talks')),
        (ENDING, _('Ending')),
    )
    start_timetable = models.TimeField(
        _('Start Timetable'), null=True, blank=False)
    end_timetable = models.TimeField(
        _('End Timetable'), null=True, blank=False)
    track_order = models.SmallIntegerField(_('Order'), null=True, blank=True)
    activity_type = models.CharField(
        _('Type'), choices=ACTIVITY_TYPES, default=PROPOSAL, max_length=50)

    # relations
    track = models.ForeignKey(to='deck.Track', related_name='activities',
                              null=True, blank=True)

    class Meta:
        ordering = ('track_order', 'start_timetable', 'pk')
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    @property
    def timetable(self):
        if all([self.start_timetable is None, self.end_timetable is None]):
            return '--:--'

        return '{0} - {1}'.format(
            self.start_timetable.strftime('%H:%M'),
            self.end_timetable.strftime('%H:%M')
        )


class Proposal(Activity):
    is_approved = models.BooleanField(_('Is approved'), default=False)
    more_information = models.TextField(
        _('More information'), max_length=10000, null=True, blank=True)

    # relations
    event = models.ForeignKey(to='deck.Event', related_name='proposals')
    coauthors = models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = _('Proposal')
        verbose_name_plural = _('Proposals')

    def save(self, *args, **kwargs):
        if not self.pk and self.event.due_date_is_passed:
            raise ValidationError(
                _("This Event doesn't accept Proposals anymore."))
        return super(Proposal, self).save(*args, **kwargs)

    @property
    def get_rate(self):
        rate = None
        try:
            rate = self.votes__rate__sum
        except AttributeError:
            rate = self.votes.aggregate(Sum('rate'))['rate__sum']
        finally:
            return rate or 0

    def rate(self, user, rate):
        rate_int = [r[0] for r in Vote.VOTE_RATES if rate in r][0]
        with transaction.atomic():
            self.votes.create(user=user, rate=rate_int)

    def user_already_voted(self, user):
        if isinstance(user, AnonymousUser):
            return False
        return self.votes.filter(user=user).exists()

    def user_can_vote(self, user):
        can_vote = False
        if self.user_already_voted(user) or \
           (self.author == user and not self.event.author == user):
            pass
        elif self.event.allow_public_voting:
            can_vote = True
        elif user.is_superuser:
            can_vote = True
        elif self.event.jury.users.filter(pk=user.pk).exists():
            can_vote = True
        return can_vote

    def user_can_approve(self, user):
        can_approve = False
        if user.is_superuser:
            can_approve = True
        elif self.event.jury.users.filter(pk=user.pk).exists():
            can_approve = True
        return can_approve

    def get_absolute_url(self):
        return reverse('view_event', kwargs={'slug': self.event.slug}) + \
            '#' + self.slug

    def approve(self):
        if self.is_approved:
            raise ValidationError(_("This Proposal was already approved."))
        self.is_approved = True
        self.save()

    def disapprove(self):
        if not self.is_approved:
            raise ValidationError(_("This Proposal was already disapproved."))
        self.is_approved = False
        self.save()

    @property
    def coauthors_names(self):
        coauthors = self.coauthors.values_list('username', flat=True)
        if not coauthors:
            return _("None")
        return ", ".join(coauthors)

    def get_authors_email(self):
        emails = [self.author.email]
        for coauthor in self.coauthors.all():
            emails.append(coauthor.email)
        return emails


class Track(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    slug = AutoSlugField(populate_from='title', overwrite=True,
                         max_length=200, unique=True, db_index=True)

    # relations
    event = models.ForeignKey(to='deck.Event', related_name='tracks')

    class Meta:
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')

    def __unicode__(self):
        return 'Track for: "%s"' % self.event.title

    @property
    def proposals(self):
        return Proposal.objects.filter(
            pk__in=self.activities.values_list('pk', flat=True)
        )


class Event(DeckBaseModel):
    allow_public_voting = models.BooleanField(_('Allow Public Voting'),
                                              default=True)
    due_date = models.DateTimeField(null=True, blank=True)
    slots = models.SmallIntegerField(_('Slots'), default=10)

    # relations
    jury = models.OneToOneField(to='jury.Jury', related_name='event',
                                null=True, blank=True)
    anonymous_voting = models.BooleanField(_('Anonymous Voting?'), default=False)

    class Meta:
        ordering = ['-due_date', '-created_at']
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    @property
    def due_date_is_passed(self):
        if not self.due_date:
            return False
        return timezone.now() > self.due_date

    def get_absolute_url(self):
        return reverse('view_event', kwargs={'slug': self.slug})

    def user_can_see_proposals(self, user):
        can_see_proposals = False
        if user.is_superuser or self.author == user:
            can_see_proposals = True
        elif self.allow_public_voting:
            can_see_proposals = True
        elif (not user.is_anonymous() and
              self.jury.users.filter(pk=user.pk).exists()):
            can_see_proposals = True
        return can_see_proposals

    def get_proposers_count(self):
        return self.proposals.values_list(
            'author', flat=True).distinct().count()

    def get_votes_count(self):
        return self.proposals.values_list('votes', flat=True).count()

    def get_votes_to_export(self):
        return self.proposals.values(
            'id', 'title', 'author__username', 'author__email'
        ).annotate(
            Sum('votes__rate')
        ).annotate(Count('votes'))

    def get_schedule(self):
        schedule = Activity.objects.filter(track__event=self)\
            .cached_authors()\
            .annotate(Sum('proposal__votes__rate'))\
            .extra(select=dict(track_isnull='track_id IS NULL'))\
            .order_by('track_isnull', 'track_order',
                      '-proposal__votes__rate__sum')
        return schedule

    def get_not_approved_schedule(self):
        not_approved_schedule = self.proposals\
            .cached_authors()\
            .filter(models.Q(is_approved=False) |
                    models.Q(track__isnull=True))\
            .annotate(Sum('votes__rate'))\
            .order_by('-is_approved', '-votes__rate__sum')
        return not_approved_schedule


@receiver(user_signed_up)
def send_welcome_mail(request, user, **kwargs):
    if not settings.SEND_NOTIFICATIONS:
        return
    message = render_to_string('mailing/welcome.txt')
    subject = _(u'Welcome')
    recipients = [user.email]
    send_mail(subject, message, settings.NO_REPLY_EMAIL, recipients)


@receiver(post_save, sender=Event)
def create_initial_jury(sender, instance, signal, created, **kwargs):
    if not created:
        return
    jury = Jury()
    jury.save()
    jury.users.add(instance.author)
    instance.jury = jury
    instance.save()


@receiver(post_save, sender=Event)
def create_initial_track(sender, instance, signal, created, **kwargs):
    if not created:
        return
    Track.objects.create(event=instance)


@receiver(post_delete, sender=Proposal)
def send_proposal_deleted_mail(sender, instance, **kwargs):
    if not settings.SEND_NOTIFICATIONS:
        return
    context = {'event_title': instance.event.title,
               'proposal_title': instance.title}
    message = render_to_string('mailing/jury_deleted_proposal.txt', context)
    subject = _(u'Proposal from %s just got deleted' % instance.event.title)
    recipients = instance.event.jury.users.values_list('email', flat=True)
    send_mail(subject, message, settings.NO_REPLY_EMAIL, recipients)
