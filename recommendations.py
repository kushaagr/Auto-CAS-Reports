CATEGORIES      = [
'Variables',
    'Anxiety (AN)',
    'Depression (DP)',
    'Suicidal Ideation (SI)',
    'Substance Abuse (SA)',
    'Self-esteem Problems (SE)',
    'Interpersonal Problems (IP)',
    'Family Problems (FP)',
    'Academic Problems (AP)',
    'Career Problems (CP)'
]

RECOMMENDATIONS = [
[
    """"""
],
    [
        """Practice mindfulness use stress management and relaxation techniques.""",
        """Keep a journal of your anxiety - when it happens, what triggers it, and how you reacted."""
        ],
    [
        """Get 6-8 hours sleep.""",
        """Take at least 30 minutes brisk walk daily, eat healthy food and drink plenty of water."""
        ],
    [
        """Count blessings in life and talk to your family or other supportive people.""",
        """Realize that suicidal feelings are the result of treatable problems""",
        """Act as if there are other options instead of suicide, even if you may not see them right now."""
    ],
    [   """Manage Stress""",
        """Learn to accept the things you can't change."""
        ], 
    [   """Do something that makes you feel good.""",
        """Spend time with people who make you feel good about yourself."""
        ],
    [   """Talk it out, face to face.""",
        """Work on your communication skills and apologize when necessary."""
        ],
    [   """Actively listen to what your family members are saying and what they mean.""",
        """Communicate your side of the story clearly and honestly."""
        ],
    [   """Make a schedule and manage your time accordingly.""",
        """Take notes in class and review them later, ask questions and participate in class discussions."""
        ],
    [   """Read related books & interact with learned ones in the field/subjects especially those having experiences.""",
        """Try to find out where your aptitude and interest lies; accordingly make choices."""
        ]
]

crpair  = dict(zip(CATEGORIES[1:], RECOMMENDATIONS[1:]))

if __name__ == '__main__':
    from pprint import pprint
    # crpair  = { CATEGORIES[i]:RECOMMENDATIONS[i] for i in range(1, len(CATEGORIES)) }
    pprint(crpair)