from os import environ

SESSION_CONFIGS = [
    dict(
        name='economic_voting_game',
        display_name="Economic Voting Game",
        num_demo_participants=5,
        # app_sequence=['gameintroduction','ecoVotingGame', 'payment_info']
        app_sequence=['gameintroduction', 'ecoVotingGame'],
        participation_fee=150
    ),
    dict(
        name='economic_voting_game_test',
        display_name="Economic Voting Game (Testing)",
        num_demo_participants=5,
        # app_sequence=['gameintroduction','ecoVotingGame', 'payment_info']
        app_sequence=['gameintroduction', 'ecoVotingGame'],
        use_browser_bots=True,
        participation_fee=150
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4*pr2dnu)m8w71q9+pphxxl#3quad2sh-gg^r+r*%w3z(d1nic'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


def creating_session(subsession):
    print(subsession.id)
