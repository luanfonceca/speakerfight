from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.aggregates import Sum
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from django_extensions.db.fields import AutoSlugField


class DeckBaseManager(models.Manager):
    def cached_authors(self):
        return super(DeckBaseManager, self).select_related('author')

    def published_ones(self):
        return self.cached_authors().filter(is_published=True)


class DeckBaseModel(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    slug = AutoSlugField(populate_from='title', overwrite=True,
                         max_length=60, unique=True, db_index=True)
    description = models.TextField(_('Description'), max_length=400)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    is_published = models.BooleanField(_('Publish'), default=False)

    # relations
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               related_name='%(class)ss')

    # managers
    objects = DeckBaseManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.title)


class Vote(models.Model):
    ANGRY, SLEEPY, SAD, HAPPY, LAUGHING = range(-1, 4)
    VOTE_RATES = ((ANGRY, 'angry'),
                  (SLEEPY, 'sleepy'),
                  (SAD, 'sad'),
                  (HAPPY, 'happy'),
                  (LAUGHING, 'laughing'))
    rate = models.SmallIntegerField(_('Rate Index'), null=True, blank=True,
                                    choices=VOTE_RATES)

    proposal = models.ForeignKey(to='deck.Proposal', related_name='votes')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='votes')

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        unique_together = (('proposal', 'user'),)

    def __unicode__(self):
        return unicode("{0.user}: {0.rate} in {0.proposal}".format(self))

    def save(self, *args, **kwargs):
        validation_message = None
        if self.user == self.proposal.author:
            validation_message = 'You cannot Rate your own proposals.'
        if not self.proposal.event.allow_public_voting:
            validation_message = "Proposal doesn't accept Public Voting."
        if self.proposal.user_already_votted(self.user):
            validation_message = 'Proposal already Rated by you.'

        if validation_message:
            raise ValidationError(_(validation_message))

        return super(Vote, self).save(*args, **kwargs)


class Proposal(DeckBaseModel):
    # relations
    event = models.ForeignKey(to='deck.Event', related_name='proposals')

    class Meta:
        verbose_name = _('Proposal')
        verbose_name_plural = _('Proposals')

    @property
    def rate(self):
        return self.votes.aggregate(Sum('rate'))['rate__sum'] or 0

    def user_already_votted(self, user):
        if isinstance(user, AnonymousUser):
            return False
        return self.votes.filter(user=user).exists()

    def get_absolute_url(self):
        return reverse('view_event', kwargs={'slug': self.event.slug})


class Event(DeckBaseModel):
    allow_public_voting = models.BooleanField(_('Allow Public Voting'),
                                              default=True)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def get_absolute_url(self):
        return reverse('view_event', kwargs={'slug': self.slug})

    # def proposals_with_authors(self):
    #     return self.proposals.select_related('author')
