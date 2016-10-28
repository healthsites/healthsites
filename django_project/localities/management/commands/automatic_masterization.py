# -*- coding: utf-8 -*-
import difflib
import time
from django.core.management.base import BaseCommand
from localities.masterization import promote_unconfirmed_synonym
from localities.models import UnconfirmedSynonym


class Command(BaseCommand):
    candidate_score = 90
    weight = {"name": 100, "default": 1, 'what3words': 10}

    def clean_rep_dict(self, rep_dict):
        for key in rep_dict['values'].keys():
            rep_dict[key] = rep_dict['values'][key]
        del rep_dict['values']
        del rep_dict['uuid']
        del rep_dict['geom']
        return rep_dict

    def handle(self, *args, **options):
        candidates = UnconfirmedSynonym.objects.all()
        strong_candidates = []
        for candidate in candidates:
            score = 0
            master = candidate.locality
            master_dict = self.clean_rep_dict(master.repr_dict())
            synonym = candidate.synonym
            synonym_dict = self.clean_rep_dict(synonym.repr_dict())
            print "============================================================="
            print "master : %d keys" % len(master_dict.keys())
            print master_dict
            print "synonym : %d keys" % len(synonym_dict.keys())
            print synonym_dict
            print "______________________________________________________________"
            master_is_osm = False
            if 'raw-source' in master_dict and 'http://www.openstreetmap.org/' in master_dict['raw-source']:
                master_is_osm = True

            for key in master_dict.keys():
                if key in synonym_dict.keys():
                    try:
                        ratio = difflib.SequenceMatcher(
                            None, master_dict[key],
                            synonym_dict[key]).ratio()
                        print "%s = %f%%" % (key, ratio * 100)

                        if master_is_osm and key == 'raw-source' and ratio == 1:
                            score += 50
                        else:
                            if not key in self.weight:
                                score += ratio * self.weight['default']
                            else:
                                score += ratio * self.weight[key]
                    except TypeError:
                        pass

            if master.changeset.created >= synonym.changeset.created:
                print "%s is newer than %s" % (master.name, synonym.name)
                strong_candidates.append(candidate.id)
            else:
                print "%s is newer than %s" % (synonym.name, master.name)
            print "______________________________________________________________"
            print "score %f" % score

        time.sleep(10)
        print "have %d strong duplicate candidates" % len(strong_candidates)
        for unconfirmed_id in strong_candidates:
            promote_unconfirmed_synonym(unconfirmed_id)
