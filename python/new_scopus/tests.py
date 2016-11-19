def flatten_dict(d):
    def expand(key, value):
        if isinstance(value, dict):
            return [ (key + '_' + k, v) for k, v in flatten_dict(value).items() ]
        else:
            return [ (key, value) ]

    items = [ item for k, v in d.items() for item in expand(k, v) ]

    return dict(items)

dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
wanted_keys = ['date-created', 'preferred-name']
d = { "date-created": {
                "@day": "14",
                "@month": "11",
                "@year": "2007"
            },
            "name-variant": [
                {
                    "given-name": "Athanasios",
                    "indexed-name": "Vasilakos A.",
                    "initials": "A.",
                    "surname": "Vasilakos"
                },
                {
                    "given-name": "A.",
                    "indexed-name": "Vasilakos A.",
                    "initials": "A.",
                    "surname": "Vasilakos"
                },
                {
                    "given-name": "A. V.",
                    "indexed-name": "Vasilakos A.",
                    "initials": "A.V.",
                    "surname": "Vasilakos"
                },
                {
                    "given-name": "Athanassios",
                    "indexed-name": "Vasilakos A.",
                    "initials": "A.",
                    "surname": "Vasilakos"
                },
                {
                    "given-name": "Athanasios T.",
                    "indexed-name": "Vasilakos A.",
                    "initials": "A.T.",
                    "surname": "Vasilakos"
                }
            ],
            "preferred-name": {
                "given-name": "Athanasios V.",
                "indexed-name": "Vasilakos A.",
                "initials": "A.V.",
                "surname": "Vasilakos"
            },
            "publication-range": {
                "@end": "2016",
                "@start": "1988"
            },
            "status": "update"
        }

print(flatten_dict(dictfilt(d, wanted_keys)))
