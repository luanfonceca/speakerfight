from django.test import TestCase
from django.db.models import (CharField, TextField,
                              BooleanField, ForeignKey,
                              SmallIntegerField)
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from deck.models import Event, Proposal, Vote, Jury

EVENT_DATA = {
    'title': 'RuPy',
    'slug': 'rupy',
    'description': 'A really good event.',
    'author_id': 1,
    'is_published': False,
    'slots': 30
}

PROPOSAL_DATA = {
    'title': 'Python For Zombies',
    'slug': 'python-for-zombies',
    'description': 'Brain...',
    'author_id': 1,
}

ANOTHER_PROPOSAL_DATA = {
    'title': 'A Python 3 Metaprogramming Tutorial',
    'slug': 'python-3-metaprogramming',
    'description': 'An advanced tutorial on Python 3 and Metaprogramming',
    'author_id': 1
}


class EventModelIntegrityTest(TestCase):
    def setUp(self):
        self.fields = {
            field.name: field for field in Event._meta.fields
        }

    def test_assert_event_should_have_a_verbose_name(self):
        self.assertEquals(_('Event'), Event._meta.verbose_name)

    def test_assert_event_should_have_a_verbose_name_plural(self):
        self.assertEquals(_('Events'), Event._meta.verbose_name_plural)

    def test_assert_event_should_have_a_title(self):
        self.assertIn('title', Event._meta.get_all_field_names())

    def test_assert_event_title_should_be_a_CharField(self):
        self.assertIsInstance(self.fields['title'], CharField)

    def test_assert_event_title_should_be_required(self):
        self.assertEquals(False, self.fields['title'].null)
        self.assertEquals(False, self.fields['title'].blank)

    def test_assert_event_title_should_have_at_most_200_characters(self):
        self.assertEquals(200, self.fields['title'].max_length)

    def test_assert_event_should_have_a_description(self):
        self.assertIn('description', Event._meta.get_all_field_names())

    def test_assert_event_description_should_be_a_TextField(self):
        self.assertIsInstance(self.fields['description'], TextField)

    def test_assert_event_description_should_be_nullable_but_needs_to_be_blank(self):
        self.assertEquals(False, self.fields['description'].null)
        self.assertEquals(True, self.fields['description'].blank)

    def test_assert_event_description_should_have_at_most_10000_characters(self):
        self.assertEquals(10000, self.fields['description'].max_length)

    def test_assert_event_should_allow_public_voting(self):
        self.assertIn('allow_public_voting', Event._meta.get_all_field_names())

    def test_assert_event_allow_public_voting_should_be_a_BooleanField(self):
        self.assertIsInstance(self.fields['allow_public_voting'], BooleanField)

    def test_assert_event_allow_public_voting_should_be_True_as_default(self):
        self.assertEquals(True, self.fields['allow_public_voting'].default)

    def test_assert_event_should_have_a_author(self):
        self.assertIn('author', Event._meta.get_all_field_names())

    def test_assert_event_author_should_be_an_User(self):
        self.assertEquals(User, self.fields['author'].rel.to)

    def test_assert_event_author_should_be_a_ForeignKey(self):
        self.assertIsInstance(self.fields['author'], ForeignKey)

    def test_assert_event_author_should_be_required(self):
        self.assertEquals(False, self.fields['author'].null)
        self.assertEquals(False, self.fields['author'].blank)

    def test_assert_event_author_should_have_a_related_name(self):
        self.assertEquals('events', self.fields['author'].rel.related_name)

    def test_assert_event_should_have_a_publish_flag(self):
        self.assertIn('is_published', Event._meta.get_all_field_names())

    def test_assert_event_is_published_should_be_a_BooleanField(self):
        self.assertIsInstance(self.fields['is_published'], BooleanField)

    def test_assert_event_is_published_should_be_True_as_default(self):
        self.assertEquals(True, self.fields['is_published'].default)

    def test_assert_event_should_have_a_jury(self):
        self.assertIn('jury', Event._meta.get_all_field_names())

    def test_assert_event_jury_should_be_an_Jury(self):
        self.assertEquals(Jury, self.fields['jury'].rel.to)

    def test_assert_event_jury_should_be_a_ForeignKey(self):
        self.assertIsInstance(self.fields['jury'], ForeignKey)

    def test_assert_event_jury_should_not_be_required(self):
        self.assertEquals(True, self.fields['jury'].null)
        self.assertEquals(True, self.fields['jury'].blank)

    def test_assert_event_jury_should_have_a_related_name(self):
        self.assertEquals('event', self.fields['jury'].rel.related_name)


class EventObjectTest(TestCase):
    def setUp(self):
        self.event = Event(**EVENT_DATA)

    def test_assert_event_unicode_representation(self):
        self.assertEquals(u'RuPy', unicode(self.event))

    def test_assert_event_title(self):
        self.assertEquals(u'RuPy', self.event.title)

    def test_assert_event_description(self):
        self.assertEquals(u'A really good event.', self.event.description)

    def test_assert_event_author(self):
        self.assertEquals(1, self.event.author_id)

    def test_assert_event_allow_public_voting(self):
        self.assertEquals(True, self.event.allow_public_voting)

    def test_assert_event_is_published(self):
        self.assertEquals(False, self.event.is_published)


class ProposalModelIntegrityTest(TestCase):
    def setUp(self):
        self.fields = {
            field.name: field for field in Proposal._meta.fields
        }

    def test_assert_proposal_should_have_a_verbose_name(self):
        self.assertEquals(_('Proposal'), Proposal._meta.verbose_name)

    def test_assert_proposal_should_have_a_verbose_name_plural(self):
        self.assertEquals(_('Proposals'), Proposal._meta.verbose_name_plural)

    def test_assert_proposal_should_have_a_title(self):
        self.assertIn('title', Proposal._meta.get_all_field_names())

    def test_assert_proposal_title_should_be_a_CharField(self):
        self.assertIsInstance(self.fields['title'], CharField)

    def test_assert_proposal_title_should_be_required(self):
        self.assertEquals(False, self.fields['title'].null)
        self.assertEquals(False, self.fields['title'].blank)

    def test_assert_proposal_title_should_have_at_most_200_characters(self):
        self.assertEquals(200, self.fields['title'].max_length)

    def test_assert_proposal_should_have_a_description(self):
        self.assertIn('description', Proposal._meta.get_all_field_names())

    def test_assert_proposal_description_should_be_a_TextField(self):
        self.assertIsInstance(self.fields['description'], TextField)

    def test_assert_proposal_description_should_be_nullable_but_needs_to_be_blank(self):
        self.assertEquals(False, self.fields['description'].null)
        self.assertEquals(True, self.fields['description'].blank)

    def test_assert_proposal_description_should_have_10000_characters(self):
        self.assertEquals(10000, self.fields['description'].max_length)

    def test_assert_proposal_should_have_a_author(self):
        self.assertIn('author', Proposal._meta.get_all_field_names())

    def test_assert_proposal_author_should_be_an_User(self):
        self.assertEquals(User, self.fields['author'].rel.to)

    def test_assert_proposal_author_should_be_a_ForeignKey(self):
        self.assertIsInstance(self.fields['author'], ForeignKey)

    def test_assert_proposal_author_should_be_required(self):
        self.assertEquals(False, self.fields['author'].null)
        self.assertEquals(False, self.fields['author'].blank)

    def test_assert_proposal_event_should_have_a_related_name(self):
        self.assertEquals('proposals', self.fields['event'].rel.related_name)

    def test_assert_proposal_should_have_a_event(self):
        self.assertIn('event', Proposal._meta.get_all_field_names())

    def test_assert_proposal_event_should_be_an_Event(self):
        self.assertEquals(Event, self.fields['event'].rel.to)

    def test_assert_proposal_event_should_be_a_ForeignKey(self):
        self.assertIsInstance(self.fields['event'], ForeignKey)

    def test_assert_proposal_event_should_be_required(self):
        self.assertEquals(False, self.fields['event'].null)
        self.assertEquals(False, self.fields['event'].blank)

    def test_assert_proposal_should_have_a_publish_flag(self):
        self.assertIn('is_published', Proposal._meta.get_all_field_names())

    def test_assert_proposal_is_published_should_be_a_BooleanField(self):
        self.assertIsInstance(self.fields['is_published'], BooleanField)

    def test_assert_proposal_is_published_should_be_True_as_default(self):
        self.assertEquals(True, self.fields['is_published'].default)

    def test_assert_proposal_is_approved_should_be_a_BooleanField(self):
        self.assertIsInstance(self.fields['is_approved'], BooleanField)

    def test_assert_proposal_is_approved_should_be_False_as_default(self):
        self.assertEquals(False, self.fields['is_approved'].default)


class ProposalObjectTest(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.user = User.objects.first()
        self.event = Event(**EVENT_DATA)
        self.proposal = Proposal(**PROPOSAL_DATA)
        self.vote = Vote(user_id=self.event.author_id,
                         proposal=self.proposal, rate=3)

    def test_assert_proposal_unicode_representation(self):
        self.assertEquals(u'Python For Zombies', unicode(self.proposal))

    def test_assert_proposal_title(self):
        self.assertEquals(u'Python For Zombies', self.proposal.title)

    def test_assert_proposal_description(self):
        self.assertEquals(u'Brain...', self.proposal.description)

    def test_assert_proposal_author(self):
        self.assertEquals(1, self.proposal.author_id)

    def test_assert_proposal_rate(self):
        self.assertEquals(0, self.proposal.get_rate)

    def test_get_absolute_url(self):
        self.proposal.event = self.event
        self.assertEquals('/events/rupy/#python-for-zombies',
                          self.proposal.get_absolute_url())

    def test_assert_user_cannot_vote_multiple_times(self):
        self.event.save()
        self.proposal.event = self.event
        self.proposal.author = User.objects.get(id=2)
        self.proposal.save()
        self.vote.proposal = self.proposal
        self.vote.save()

        self.assertTrue(self.proposal.user_already_voted(self.user))

    def test_assert_proposal_is_published(self):
        self.assertEquals(True, self.proposal.is_published)

    def test_assert_proposal_approve(self):
        self.event.save()
        self.proposal.event = self.event
        self.proposal.save()

        self.assertEquals(False, self.proposal.is_approved)
        self.proposal.approve()
        self.assertEquals(True, self.proposal.is_approved)

    def test_assert_proposal_disapprove(self):
        self.event.save()
        self.proposal.event = self.event
        self.proposal.is_approved = True
        self.proposal.save()

        self.assertEquals(True, self.proposal.is_approved)
        self.proposal.disapprove()
        self.assertEquals(False, self.proposal.is_approved)

    def test_assert_proposal_get_authors_email(self):
        self.event.save()
        self.proposal.event = self.event
        self.proposal.save()
        emails = self.proposal.get_authors_email()
        self.assertEquals(emails, [self.proposal.author.email])

    def test_assert_proposal_get_all_authors_email(self):
        self.event.save()
        self.proposal.event = self.event
        self.proposal.save()
        user = User.objects.get(id=2)
        self.proposal.coauthors.add(user.id)
        emails = self.proposal.get_authors_email()
        self.assertEquals(emails, [self.proposal.author.email, user.email])

    def test_assert_proposal_should_have_coauthors_names(self):
        self.event.save()
        self.proposal.event = self.event
        self.proposal.save()
        coauthors_names = self.proposal.coauthors_names
        self.assertEquals(coauthors_names, "None")
        self.proposal.coauthors.add(2)
        self.proposal.coauthors.add(3)
        coauthors_names = self.proposal.coauthors_names
        self.assertEquals(coauthors_names, "user, another")
        


class VoteModelIntegrityTest(TestCase):
    def setUp(self):
        self.fields = {
            field.name: field for field in Vote._meta.fields
        }

    def test_assert_vote_should_have_a_verbose_name(self):
        self.assertEquals(_('Vote'), Vote._meta.verbose_name)

    def test_assert_vote_should_have_a_verbose_name_plural(self):
        self.assertEquals(_('Votes'), Vote._meta.verbose_name_plural)

    def test_assert_vote_should_have_a_unique_together_constraint(self):
        self.assertEquals((('proposal', 'user'),), Vote._meta.unique_together)

    def test_assert_vote_should_have_a_rate(self):
        self.assertIn('rate', Vote._meta.get_all_field_names())

    def test_assert_vote_rate_should_be_a_SmallIntegerField(self):
        self.assertIsInstance(self.fields['rate'], SmallIntegerField)

    def test_assert_vote_rate_should_be_required(self):
        self.assertEquals(True, self.fields['rate'].null)
        self.assertEquals(True, self.fields['rate'].blank)

    def test_assert_vote_should_have_a_proposal(self):
        self.assertIn('proposal', Vote._meta.get_all_field_names())

    def test_assert_vote_proposal_should_be_an_Proposal(self):
        self.assertEquals(Proposal, self.fields['proposal'].rel.to)

    def test_assert_vote_proposal_should_be_a_ForeignKey(self):
        self.assertIsInstance(self.fields['proposal'], ForeignKey)

    def test_assert_vote_proposal_should_be_required(self):
        self.assertEquals(False, self.fields['proposal'].null)
        self.assertEquals(False, self.fields['proposal'].blank)

    def test_assert_vote_proposal_should_have_a_related_name(self):
        self.assertEquals('votes', self.fields['proposal'].rel.related_name)

    def test_assert_vote_should_have_a_author(self):
        self.assertIn('user', Vote._meta.get_all_field_names())

    def test_assert_vote_user_should_be_an_User(self):
        self.assertEquals(User, self.fields['user'].rel.to)

    def test_assert_vote_user_should_be_a_ForeignKey(self):
        self.assertIsInstance(self.fields['user'], ForeignKey)

    def test_assert_vote_user_should_be_required(self):
        self.assertEquals(False, self.fields['user'].null)
        self.assertEquals(False, self.fields['user'].blank)

    def test_assert_vote_event_should_have_a_related_name(self):
        self.assertEquals('votes', self.fields['user'].rel.related_name)


class VoteObjectTest(TestCase):
    def setUp(self):
        self.event = Event(**EVENT_DATA)
        self.proposal = Proposal(event=self.event, **PROPOSAL_DATA)
        self.vote = Vote(user_id=self.event.author_id,
                         proposal=self.proposal, rate=3)

    def test_assert_vote_unicode_representation(self):
        self.vote.user = User(username='User')
        self.assertEquals(u'User: 3 in Python For Zombies', unicode(self.vote))

    def test_assert_vote_rate(self):
        self.assertEquals(3, self.vote.rate)

    def test_assert_vote_proposal(self):
        self.assertEquals(self.proposal, self.vote.proposal)

    def test_assert_vote_author(self):
        self.assertEquals(1, self.vote.user_id)
