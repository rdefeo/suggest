__author__ = 'robdefeo'


context = {
    "entities": [
        {
            "type": "color",
            "key": "black"
        },
        {
            "type": "theme",
            "key": "party"
        },
        {
            "type": "style",
            "key": "boots"
        }
    ]
}

import suggest.handlers.root
suggest.handlers.root.suggest(context)

import cProfile
pr = cProfile.Profile()
pr.enable()
suggest.handlers.root.suggest(context)
pr.disable()
import io
s = io.StringIO()
sortby = 'cumulative'
import pstats
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())